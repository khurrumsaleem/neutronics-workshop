"""
Silicon dose in a simple tokamak using a mesh tally.

Builds a simplified tokamak with:
  - Central column (tungsten)
  - First wall (iron)
  - Blanket (lithium)
  - Plasma region (void)
  - Outer vessel region (void)
  - Concrete slab below the tokamak

A 14.1 MeV D-T ring source sits at the plasma midplane. A mesh tally scores
Si absorbed dose (KERMA) across the geometry without adding Si to the geometry
and compares it to biological effective dose. This is useful for estimating
Si dose in detectors that might be placed in the tokamak, without having to
add Si to the geometry.

This relies on the ability to score microscopic cross sections for nuclides
not present in the local material (equivalent to OpenMC PR #3771).
"""

import math
from pathlib import Path

from matplotlib import colormaps
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import openmc
# Setting the cross section path to the correct location in the docker image.
# If you are running this outside the docker image you will have to change this path to your local cross section path.
openmc.config['cross_sections'] = Path.home() / 'nuclear_data' / 'endf-b8.0-hdf5' / 'cross_sections.xml'

# ---- materials (none of these are silicon — that's the point) --------------
iron = openmc.Material(name='iron')
iron.add_element('Fe', 1.0)
iron.set_density("g/cm3", 7.874)

lithium = openmc.Material(name='lithium')
lithium.add_element('Li', 1.0)
lithium.set_density("g/cm3", 0.534)

tungsten = openmc.Material(name='tungsten')
tungsten.add_element('W', 1.0)
tungsten.set_density("g/cm3", 19.3)

concrete = openmc.Material(name='concrete')
concrete.add_element('O', 0.532)
concrete.add_element('Si', 0.337)
concrete.add_element('Ca', 0.044)
concrete.add_element('Al', 0.034)
concrete.add_element('Fe', 0.014)
concrete.add_element('H', 0.023)
concrete.add_element('Na', 0.016)
concrete.set_density("g/cm3", 2.3)

# ---- geometry (simple tokamak) ---------------------------------------------
R0 = 500.0              # major radius [cm]
FW_THICK = 20.0         # first-wall thickness [cm]
BLK_THICK = 80.0        # blanket thickness [cm]
CC_RADIUS = 150.0       # center-column cylinder radius [cm]
CC_EXTEND = 10.0        # center column extends beyond blanket [cm]

inner_r = R0
fw_r = R0 + FW_THICK
outer_r = R0 + FW_THICK + BLK_THICK
half_height = outer_r + CC_EXTEND

# surfaces
inner_sphere = openmc.Sphere(r=inner_r)
fw_sphere = openmc.Sphere(r=fw_r)
outer_sphere = openmc.Sphere(r=outer_r)
center_cyl = openmc.ZCylinder(r=CC_RADIUS)
top_plane = openmc.ZPlane(z0=half_height, boundary_type='vacuum')
bot_plane = openmc.ZPlane(z0=-half_height)
slab_bot_plane = openmc.ZPlane(z0=-half_height - 100, boundary_type='vacuum')
outer_cyl = openmc.ZCylinder(r=outer_r, boundary_type='vacuum')

# regions
plasma_region = -inner_sphere & +center_cyl
fw_region = +inner_sphere & -fw_sphere & +center_cyl
blanket_region = +fw_sphere & -outer_sphere & +center_cyl
center_col_region = -center_cyl & -top_plane & +bot_plane
outer_region = +outer_sphere & +center_cyl & -top_plane & +bot_plane & -outer_cyl

# concrete slab below the tokamak (100 cm thick)
slab_region = -bot_plane & +slab_bot_plane & -outer_cyl

# cells
plasma_cell = openmc.Cell(region=plasma_region, name='plasma')           # void
fw_cell = openmc.Cell(region=fw_region, name='first_wall', fill=iron)
blanket_cell = openmc.Cell(region=blanket_region, name='blanket', fill=lithium)
cc_cell = openmc.Cell(region=center_col_region, name='center_column', fill=tungsten)
outer_cell = openmc.Cell(region=outer_region, name='outer_vessel')       # void
slab_cell = openmc.Cell(region=slab_region, name='concrete_slab', fill=concrete)

geometry = openmc.Geometry([plasma_cell, fw_cell, blanket_cell, cc_cell, outer_cell, slab_cell])

# ---- source: D-T ring at plasma midplane -----------------------------------
source_r = CC_RADIUS + (R0 - CC_RADIUS) / 2.0   # halfway between CC and FW
source = openmc.IndependentSource(
    space=openmc.stats.CylindricalIndependent(
        r=openmc.stats.Discrete([source_r], [1.0]),
        phi=openmc.stats.Uniform(0.0, 2 * math.pi),
        z=openmc.stats.Discrete([0.0], [1.0]),
    ),
    energy=openmc.stats.Discrete([14.1e6], [1.0]),    # 14.1 MeV
    angle=openmc.stats.Isotropic(),
)

settings = openmc.Settings(
    run_mode='fixed source',
    photon_transport=True,
    particles=50_000,
    batches=10,
    source=source,
    seed=42,
)

# ---- tallies ---------------------------------------------------------------
mesh = openmc.RegularMesh.from_domain(geometry, dimension=500_000)
mesh_filter = openmc.MeshFilter(mesh)

print(f"Mesh: {mesh.dimension} = {math.prod(mesh.dimension)} voxels")
print(f"  lower_left  = {mesh.lower_left}")
print(f"  upper_right = {mesh.upper_right}")
print(f"  width       = {mesh.width}")

# Biological dose tallies (neutron + photon)
#   score: "flux" weighted by ICRP-116 dose coefficients via EnergyFunctionFilter
#   dose_coefficients() returns (energy_bins [eV], coefficients [pSv·cm²])
#   The EnergyFunctionFilter multiplies the flux by these coefficients at each energy.
#   Mesh flux score gives track_length / V_voxel [1/cm²/source-particle].
#   After the filter: result is in [pSv / source-particle] per voxel.
#   To get Sv/s: multiply by source_rate [n/s] and convert pSv→Sv (×1e-12).
neutron_filter = openmc.ParticleFilter("neutron")
photon_filter = openmc.ParticleFilter("photon")

energy_bins_n, dose_coeffs_n = openmc.data.dose_coefficients(
    particle="neutron", geometry="AP"
)
efilter_n = openmc.EnergyFunctionFilter(energy_bins_n, dose_coeffs_n)
efilter_n.interpolation = "cubic"

energy_bins_p, dose_coeffs_p = openmc.data.dose_coefficients(
    particle="photon", geometry="AP"
)
efilter_p = openmc.EnergyFunctionFilter(energy_bins_p, dose_coeffs_p)
efilter_p.interpolation = "cubic"

bio_n_tally = openmc.Tally(name="bio_dose_neutron")
bio_n_tally.filters = [mesh_filter, neutron_filter, efilter_n]
bio_n_tally.scores = ["flux"]

bio_p_tally = openmc.Tally(name="bio_dose_photon")
bio_p_tally.filters = [mesh_filter, photon_filter, efilter_p]
bio_p_tally.scores = ["flux"]

# Si absorbed dose (KERMA) tallies (neutron + photon)
#   score: "heating" gives total energy deposited to target nuclei [eV].
#   nuclides=["Si28"] restricts to Si28 reactions only.
#   multiply_density=False sets the atom density to 1 atom/barn-cm internally.
#
#   IMPORTANT: 1 atom/barn-cm = 1e24 atoms/cm³ (NOT 1 atom/cm³).
#   The mesh tally divides by voxel volume, so the result is a volumetric
#   heating rate: [eV/cm³/source-particle] assuming N = 1e24 atoms/cm³.
#
#   To convert to Gy/s (= J/kg/s):
#     1. Multiply by source_rate [n/s]          → eV/cm³/s
#     2. Multiply by 1.602e-19 [J/eV]           → J/cm³/s  (= W/cm³)
#     3. Divide by ρ_fictional [kg/cm³]          → J/kg/s   (= Gy/s)
#   where ρ_fictional = 1e24 × A_Si / N_A × 1e-3 [kg/cm³] ≈ 0.0466 kg/cm³
#   is the mass density corresponding to 1 atom/barn-cm of Si28.
#
#   Note: the actual Si density cancels out — both the number of interactions
#   and the target mass scale linearly with density, so Gy is independent of
#   what density you assume for the silicon detector.
si_n_tally = openmc.Tally(name="si_dose_neutron")
si_n_tally.filters = [mesh_filter, neutron_filter]
si_n_tally.scores = ["heating"]
si_n_tally.nuclides = ["Si28"]
si_n_tally.multiply_density = False

si_p_tally = openmc.Tally(name="si_dose_photon")
si_p_tally.filters = [mesh_filter, photon_filter]
si_p_tally.scores = ["heating"]
si_p_tally.nuclides = ["Si28"]
si_p_tally.multiply_density = False

# ---- run -------------------------------------------------------------------
model = openmc.Model(
    geometry=geometry,
    settings=settings,
    tallies=[bio_n_tally, bio_p_tally, si_n_tally, si_p_tally],
)

print(f"\nRunning: {settings.particles} particles x {settings.batches} batches")
model.run(openmc_exec='/home/jon/openmc/build/bin/openmc', apply_tally_results=True)
print("Done.\n")

# ---- results ---------------------------------------------------------------
SOURCE_RATE = 1e20  # neutrons per second

# Si dose conversion: [eV/cm³/source] → [Gy/s]
#   Gy/s = score × SOURCE_RATE × eV_to_J / ρ_fictional
#   The 1e24 in ρ_fictional is critical — it accounts for the fact that
#   multiply_density=False uses 1 atom/barn-cm = 1e24 atoms/cm³, not 1 atom.
#   Omitting it gives results ~1e24 too high.
A_SI = 28.085   # g/mol (Si atomic mass)
N_A = 6.022e23  # mol^-1 (Avogadro)
eV_TO_J = 1.602e-19  # J/eV
rho_fictional = 1e24 * A_SI / N_A * 1e-3  # kg/cm³ ≈ 0.0466 kg/cm³

si_n = si_n_tally.mean * SOURCE_RATE * eV_TO_J / rho_fictional   # Gy/s
si_p = si_p_tally.mean * SOURCE_RATE * eV_TO_J / rho_fictional   # Gy/s
si_total = si_n + si_p                                            # Gy/s

# Biological dose conversion: [pSv/source] → [Sv/s]
#   The EnergyFunctionFilter already folded in the dose coefficients [pSv·cm²],
#   so the tally result is directly in pSv per source particle.
#   Just scale by source rate and convert pico-sieverts to sieverts.
bio_n = bio_n_tally.mean * SOURCE_RATE * 1e-12   # Sv/s
bio_p = bio_p_tally.mean * SOURCE_RATE * 1e-12   # Sv/s
bio_total = bio_n + bio_p                         # Sv/s

print(f"Biological dose (neutron) range: {bio_n.min():.3e} to {bio_n.max():.3e} Sv/s")
print(f"Biological dose (photon)  range: {bio_p.min():.3e} to {bio_p.max():.3e} Sv/s")
print(f"Biological dose (total)   range: {bio_total.min():.3e} to {bio_total.max():.3e} Sv/s")
print(f"Silicon dose    (neutron) range: {si_n.min():.3e} to {si_n.max():.3e} Gy/s")
print(f"Silicon dose    (photon)  range: {si_p.min():.3e} to {si_p.max():.3e} Gy/s")
print(f"Silicon dose    (total)   range: {si_total.min():.3e} to {si_total.max():.3e} Gy/s")

# ---- plot: 2×3 XZ slices at y=0 -------------------------------------------
nx, ny, nz = mesh.dimension
y_mid = ny // 2  # index closest to y=0

x_extent = [mesh.lower_left[0], mesh.upper_right[0]]
z_extent = [mesh.lower_left[2], mesh.upper_right[2]]
extent = x_extent + z_extent

# tally data is ordered (nz, ny, nx) — reversed from mesh.dimension
# XZ slice at y=0: rows=z, cols=x — already correct for imshow with origin='lower'
def xz_slice(data):
    return data.reshape(nz, ny, nx)[:, y_mid, :]

cmap = colormaps.get_cmap('inferno').resampled(12)

# rows: [biological, silicon], cols: [neutron, photon, total]
plot_data = [
    [xz_slice(bio_n), xz_slice(bio_p), xz_slice(bio_total)],
    [xz_slice(si_n),  xz_slice(si_p),  xz_slice(si_total)],
]
titles = [
    ['Biological neutron (Sv/s)', 'Biological photon (Sv/s)', 'Biological total (Sv/s)'],
    ['Silicon neutron (Gy/s)',    'Silicon photon (Gy/s)',    'Silicon total (Gy/s)'],
]
units = ['Sv/s', 'Sv/s', 'Sv/s', 'Gy/s', 'Gy/s', 'Gy/s']

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

for row in range(2):
    for col in range(3):
        ax = axes[row, col]
        im = ax.imshow(
            plot_data[row][col], origin='lower', extent=extent,
            aspect='equal', norm=mcolors.LogNorm(), cmap=cmap,
        )
        geometry.plot(basis='xz', outline='only', axes=ax, pixels=1_000_000)
        ax.set_title(titles[row][col])
        ax.set_xlabel('X (cm)')
        ax.set_ylabel('Z (cm)')
        fig.colorbar(im, ax=ax, label=units[row * 3 + col])

fig.tight_layout()
plt.savefig('si_vs_bio_dose_xz.png', dpi=150)
plt.show()
print("Saved si_vs_bio_dose_xz.png")