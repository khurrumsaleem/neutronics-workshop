#!/usr/bin/env python3
"""
Sync workshop folders with source notebooks.
Keeps half-day and full-day workshop content in sync with source task folders.

Run with: python sync_workshops.py
"""

from pathlib import Path
import shutil
import nbformat

# Define workshop mappings: source notebook -> target name
WORKSHOPS = {
    'half-day-university-workshop': [
        ('task_01_cross_sections/1_isotope_xs_plot.ipynb', 'task_01.ipynb'),
        ('task_01_cross_sections/2_element_xs_plot.ipynb', 'task_02.ipynb'),
        ('task_01_cross_sections/3_material_xs_plot.ipynb', 'task_03.ipynb'),
        ('task_02_making_materials/1_example_materials_from_isotopes.ipynb', 'task_04.ipynb'),
        ('task_02_making_materials/2_example_materials_from_elements.ipynb', 'task_05.ipynb'),
        ('task_03_making_CSG_geometry/1_simple_csg_geometry.ipynb', 'task_06.ipynb'),
        ('task_04_make_sources/1_point_source_plots.ipynb', 'task_07.ipynb'),
        ('task_04_make_sources/2_ring_source.ipynb', 'task_08.ipynb'),
        ('task_04_make_sources/3_plasma_source_plots.ipynb', 'task_09.ipynb'),
        ('task_05_CSG_cell_tally_TBR/1_example_tritium_production.ipynb', 'task_10.ipynb'),
        ('task_06_CSG_cell_tally_DPA/1_find_dpa.ipynb', 'task_11.ipynb'),
        ('task_07_CSG_cell_tally_spectra/2_example_neutron_spectra_on_cell.ipynb', 'task_12.ipynb'),
        ('task_07_CSG_cell_tally_spectra/4_example_photon_spectra.ipynb', 'task_13.ipynb'),
        ('task_08_CSG_mesh_tally/1_example_2d_regular_mesh_tallies.ipynb', 'task_14.ipynb'),
        ('task_14_variance_reduction/2_shielded_room_single_ww.ipynb', 'task_15.ipynb'),
        ('task_14_variance_reduction/3_sphere_iterative_per_run_ww.ipynb', 'task_16.ipynb'),
        ('task_10_activation_transmutation_depletion/5_full_pulse_schedule.ipynb', 'task_17.ipynb'),
        ('task_21_design_task/1_optimal_design.ipynb', 'task_18.ipynb'),
    ],
    'half-day-conference-workshop': [
        # Add conference workshop tasks here
        ('task_02_making_materials/1_example_materials_from_isotopes.ipynb', 'task_01.ipynb'),
        ('task_01_cross_sections/1_isotope_xs_plot.ipynb', 'task_02.ipynb'),
        ('task_03_making_CSG_geometry/1_simple_csg_geometry.ipynb', 'task_03.ipynb'),
        ('task_04_make_sources/1_point_source_plots.ipynb', 'task_04.ipynb'),
        ('task_04_make_sources/2_ring_source.ipynb', 'task_05.ipynb'),  
        ('task_05_CSG_cell_tally_TBR/1_example_tritium_production.ipynb', 'task_06.ipynb'),
        ('task_07_CSG_cell_tally_spectra/2_example_neutron_spectra_on_cell.ipynb', 'task_07.ipynb'),
        ('task_09_CSG_instantaneous_dose_tallies/3_cell_dose_from_neutron.ipynb', 'task_08.ipynb'),
        ('task_09_CSG_instantaneous_dose_tallies/5_mesh_dose_from_neutrons.ipynb', 'task_09.ipynb'),
        ('task_14_variance_reduction/5_shielded_room_fw_cadis.ipynb', 'task_10.ipynb'),
        ('task_16_converting_CAD_geometry_to_DAGMC/2_converting_cad_in_memory.ipynb', 'task_11.ipynb'),
        ('task_17_using_DAGMC_models_in_openmc/1_cad_model_simulation_minimal.ipynb', 'task_12.ipynb'),
        ('task_18_CAD_mesh_fast_flux/1_simulate_fast_neutron_flux_on_cad.ipynb', 'task_13.ipynb'),
        ('task_10_activation_transmutation_depletion/1_depletion_with_flux_spectra.ipynb', 'task_14.ipynb'),
        ('task_10_activation_transmutation_depletion/3_example_transmutation_isotope_build_up.ipynb', 'task_15.ipynb'),
        ('task_11_CSG_shut_down_dose_tallies/4_D1S_regularmesh_shutdown_dose_rate.ipynb', 'task_16.ipynb'),
    ],
    'full-day-workshop': [
        ('task_02_making_materials/1_example_materials_from_isotopes.ipynb', 'task_01.ipynb'),
        ('task_02_making_materials/2_example_materials_from_elements.ipynb', 'task_02.ipynb'),
        ('task_01_cross_sections/1_isotope_xs_plot.ipynb', 'task_03.ipynb'),
        ('task_01_cross_sections/2_element_xs_plot.ipynb', 'task_04.ipynb'),
        ('task_01_cross_sections/3_material_xs_plot.ipynb', 'task_05.ipynb'),
        ('task_03_making_CSG_geometry/1_simple_csg_geometry.ipynb', 'task_06.ipynb'),
        ('task_03_making_CSG_geometry/2_intermediate_csg_geometry.ipynb', 'task_07.ipynb'),
        ('task_03_making_CSG_geometry/3_viewing_the_geometry_as_vtk.ipynb', 'task_08.ipynb'),
        ('task_04_make_sources/1_point_source_plots.ipynb', 'task_09.ipynb'),
        ('task_04_make_sources/2_ring_source.ipynb', 'task_10.ipynb'),
        ('task_04_make_sources/4_neutron_tracks.ipynb', 'task_11.ipynb'),
        ('task_04_make_sources/5_gamma_source_example.ipynb', 'task_12.ipynb'),
        ('task_05_CSG_cell_tally_TBR/1_example_tritium_production.ipynb', 'task_13.ipynb'),
        ('task_07_CSG_cell_tally_spectra/2_example_neutron_spectra_on_cell.ipynb', 'task_14.ipynb'),
        ('task_09_CSG_instantaneous_dose_tallies/3_cell_dose_from_neutron.ipynb', 'task_15.ipynb'),
        ('task_09_CSG_instantaneous_dose_tallies/5_mesh_dose_from_neutrons.ipynb', 'task_16.ipynb'),
        ('task_14_variance_reduction/5_shielded_room_fw_cadis.ipynb', 'task_17.ipynb'),
        ('task_16_converting_CAD_geometry_to_DAGMC/1_converting_cad_files.ipynb', 'task_18.ipynb'),
        ('task_16_converting_CAD_geometry_to_DAGMC/2_converting_cad_in_memory.ipynb', 'task_19.ipynb'),
        ('task_17_using_DAGMC_models_in_openmc/1_cad_model_simulation_minimal.ipynb', 'task_20.ipynb'),
        ('task_18_CAD_mesh_fast_flux/1_simulate_fast_neutron_flux_on_cad.ipynb', 'task_21.ipynb'),
        ('task_10_activation_transmutation_depletion/1_depletion_with_flux_spectra.ipynb', 'task_22.ipynb'),
        ('task_10_activation_transmutation_depletion/3_example_transmutation_isotope_build_up.ipynb', 'task_23.ipynb'),
        ('task_11_CSG_shut_down_dose_tallies/4_D1S_regularmesh_shutdown_dose_rate.ipynb', 'task_24.ipynb'),
    ],
}


def clear_notebook_outputs(nb):
    """Blank outputs and execution counts in a notebook object."""
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None
    return nb


def sync_workshops():
    """Sync all workshop folders with source notebooks."""
    tasks_dir = Path(__file__).parent / 'tasks'
    
    for workshop_name, mappings in WORKSHOPS.items():
        workshop_dir = tasks_dir / workshop_name
        workshop_dir.mkdir(exist_ok=True)
        
        print(f"\nSyncing {workshop_name}...")
        
        for source_rel, target_name in mappings:
            source = tasks_dir / source_rel
            target = workshop_dir / target_name
            
            if not source.exists():
                print(f"  ⚠️  MISSING: {source_rel}")
                continue
            
            if source.suffix == '.ipynb':
                notebook = nbformat.read(source, as_version=4)
                notebook = clear_notebook_outputs(notebook)
                nbformat.write(notebook, target)
            else:
                shutil.copy2(source, target)
            print(f"  ✓ {target_name}")
        
        print(f"  Completed {workshop_name}")


if __name__ == '__main__':
    sync_workshops()
    print("\n✅ All workshops synced successfully!")
