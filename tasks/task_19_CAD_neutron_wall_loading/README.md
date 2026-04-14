# Task Introduction

This task computes neutron wall loading (NWL) on a CAD-based elliptical torus shell geometry using particle tracks.

NWL is the neutron power per unit area on the first wall, a key design parameter for fusion reactors. It is computed from uncollided flux, so the geometry between the source and wall must be void.

The example uses `dagmc_h5m_file_inspector` to identify surfaces and set boundary conditions, and post-processes OpenMC particle tracks to extract the spatial distribution of wall loading on the inner torus surface.
