from cad_to_dagmc import CadToDagmc
import cadquery as cq
import openmc
from matplotlib.colors import LogNorm
import openmc.deplete

# makes a CAD geometry to use for the neutronics geometry
s = cq.Workplane("XY")
sPnts = [
    (2.75, 1.5),
    (2.5, 1.75),
    (2.0, 1.5),
    (1.5, 1.0),
    (1.0, 1.25),
    (0.5, 1.0),
    (0, 1.0),
]
r = s.lineTo(3.0, 0).lineTo(3.0, 1.0).spline(sPnts, includeCurrent=True).close()
result = r.extrude(0.5)

my_model = CadToDagmc()

my_model.add_cadquery_object(result)

# this makes the tet mesh used for the unstructured mesh tally which is overlaid on the geometry
my_model.export_unstructured_mesh_file(filename="umesh.h5m", max_mesh_size=1, min_mesh_size=0.1)

# this makes the surface mesh used for the material volume
my_model.export_dagmc_h5m_file(filename="dagmc.h5m", max_mesh_size=1, min_mesh_size=0.1, material_tags=['mat1'])

# the unstructured mesh to overlay on the DAGMC geometry
umesh = openmc.UnstructuredMesh("umesh.h5m", library="moab")

# filters for use inf the tally
mesh_filter = openmc.MeshFilter(umesh)
neutron_particle_filter = openmc.ParticleFilter(['neutron'])
energy_filter = openmc.EnergyFilter.from_group_structure('CCFE-709')

# sets up a neutron spectra tally on the unstructured mesh 
tally = openmc.Tally(name="unstructured_mesh_neutron_spectra_tally")
tally.filters = [mesh_filter, energy_filter, neutron_particle_filter]
tally.scores = ["flux"]
tally.estimator = "tracklength"
my_tallies = openmc.Tallies([tally])

my_material = openmc.Material(name='mat1')
my_material.add_nuclide("H1", 1, percent_type="ao")
my_material.set_density("g/cm3", 0.001)
my_materials = openmc.Materials([my_material])

universe = openmc.DAGMCUniverse("dagmc.h5m").bounded_universe()
my_geometry = openmc.Geometry(universe)

my_settings = openmc.Settings()
my_settings.batches = 10
my_settings.inactive = 0
my_settings.particles = 5000
my_settings.run_mode = "fixed source"

# Create a DT point source
my_source = openmc.IndependentSource()
my_source.space = openmc.stats.Point((0, 0, 0))
my_source.angle = openmc.stats.Isotropic()
my_source.energy = openmc.stats.Discrete([14e6], [1])
my_settings.source = my_source

model = openmc.model.Model(my_geometry, my_materials, my_settings, my_tallies)
sp_filename = model.run()


sp = openmc.StatePoint(sp_filename)

tally_result = sp.get_tally(name="unstrucutred_mesh_tally")

# normally with regular meshes I would get the mesh from the tally
# but with unstrucutred meshes the tally does not contain the mesh
# however we can get it from the statepoint file
# umesh = tally_result.find_filter(openmc.MeshFilter)
umesh_from_sp = sp.meshes[1]

# these trigger internal code in the mesh object so that its centroids and volumes become known.
# centroids and volumes are needed for the get_values and write_data_to_vtk steps
centroids = umesh_from_sp.centroids
mesh_vols = umesh_from_sp.volumes

flux_in_each_group_for_each_voxel = tally_result.get_values(scores=["flux"], value="mean")

all_sources = []

for flux_in_each_group, mesh_vol in zip(flux_in_each_group_for_each_voxel, mesh_vols):
    micro_xs = openmc.deplete.MicroXS.from_multigroup_flux(
        energies='CCFE-709',
        multigroup_flux=flux_in_each_group,
        temperature=294, # endf 8.0 has ['1200K', '2500K', '250K', '294K', '600K', '900K']
        chain_file= openmc.config['chain_file'],
        nuclides=my_material.get_nuclides()
    )

    # constructing the operator, note we pass in the flux and micro xs
    operator = openmc.deplete.IndependentOperator(
        materials=my_materials,
        fluxes=[sum(flux_in_each_group)*my_material.volume],  # Flux in each group in [n-cm/src] for each domain
        micros=[micro_xs],
        reduce_chain=True,  # reduced to only the isotopes present in depletable materials and their possible progeny
        reduce_chain_level=5,
        normalization_mode="source-rate"
    )

    integrator = openmc.deplete.PredictorIntegrator(
        operator=operator,
        timesteps=[5, 60, 60],
        source_rates=[1e20, 0 , 0], # a 5 second pulse of neutrons followed by 120 seconds of decay
        timestep_units='s'
    )

    integrator.integrate()

    results = openmc.deplete.Results.from_hdf5("depletion_results.h5")
    last_time_step=result[-1]
    activated_material = last_time_step.get_material(my_material.id)

    activated_material.volume = mesh_vol

    energy = activated_material.get_decay_photon_energy(
        clip_tolerance = 1e-6,  # cuts out a small fraction of the very low energy (and hence negligible dose contribution) photons
        units = 'Bq',
    )
    strength = energy.integral()


mesh_source = openmc.MeshSource(
    mesh=umesh_from_sp,
    sources=all_sources,
)

my_gamma_settings = openmc.Settings()
my_gamma_settings.run_mode = "fixed source"
my_gamma_settings.batches = 100
my_gamma_settings.particles = 100000
my_gamma_settings.source = mesh_source

energies, pSv_cm2 = openmc.data.dose_coefficients(particle="photon", geometry="AP")
dose_filter = openmc.EnergyFunctionFilter(
    energies, pSv_cm2, interpolation="cubic"  # interpolation method recommended by ICRP
)

regularmesh = openmc.RegularMesh().from_domain(
    my_geometry,
    dimension=[10, 10, 10],  # 10 voxels in each axis direction (x, y, z)
)

particle_filter = openmc.ParticleFilter(["photon"])
mesh_filter = openmc.MeshFilter(regularmesh)
dose_tally = openmc.Tally()
dose_tally.filters = [mesh_filter, dose_filter, particle_filter]
dose_tally.scores = ["flux"]
dose_tally.name = "photon_dose_on_mesh"
tallies = openmc.Tallies([dose_tally])


model_gamma = openmc.Model(my_geometry, my_materials, my_gamma_settings, tallies)

model_gamma.run(cwd="photons")

# You may wish to plot the dose tally on a mesh, this package makes it easy to include the geometry with the mesh tally
from openmc_regular_mesh_plotter import plot_mesh_tally
with openmc.StatePoint('photons/statepoint.100.h5') as statepoint:
    photon_tally = statepoint.get_tally(name="photon_dose_on_mesh")

    # normalising this tally is a little different to other examples as the source strength has been using units of photons per second.
    # tally.mean is in units of pSv-cm3/source photon.
    # as source strength is in photons_per_second this changes units to pSv-/second

    # multiplication by pico_to_micro converts from (pico) pSv/s to (micro) uSv/s
    # dividing by mesh voxel volume cancles out the cm3 units
    # could do the mesh volume scaling on the plot and vtk functions but doing it here instead
    pico_to_micro = 1e-6
    seconds_to_hours = 60*60
    scaling_factor = (seconds_to_hours * pico_to_micro) / regularmesh.volumes[0][0][0]

    plot = plot_mesh_tally(
            tally=photon_tally,
            basis="xz",
            # score='flux', # only one tally so can make use of default here
            value="mean",
            colorbar_kwargs={
                'label': "Decay photon dose [µSv/h]",
            },
            norm=LogNorm(),
            volume_normalization=False,  # this is done in the scaling_factor
            scaling_factor=scaling_factor,
        )
    plot.figure.savefig(f'shut_down_dose_map_timestep.png')