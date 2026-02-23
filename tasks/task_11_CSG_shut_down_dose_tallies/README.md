# Task Introduction

Please allow 45 minutes for this task.

In this task you will simulate shutdown dose rates on CSG (Constructive Solid Geometry) models using two methods: R2S (Rigorous 2-Step) and D1S (Direct 1-Step). Both methods calculate the photon dose field that results from activated materials after a neutron irradiation period.

The D1S method is the recommended approach. It folds decay photon production directly into a single neutron transport run and computes dose rates as a post-processing step, making it fast to vary the irradiation schedule without re-running the simulation.

The R2S examples in this task (Python scripts) run a neutron transport simulation, perform material activation/depletion, construct gamma source terms from the activated materials, then run a separate photon transport simulation. These examples are planned to be improved and converted to notebooks in a future update.

**Learning Outcomes**

- The D1S method computes shutdown dose rates in a single simulation, with the irradiation schedule applied in post-processing.
- D1S is generally faster than R2S when the pulse schedule needs to be changed, as no re-simulation is required.
- The R2S method uses a two-step workflow: neutron transport followed by photon transport using activated material as a gamma source.
- Shutdown dose rate maps can be produced on regular meshes for CSG geometries.
- Multiple neutron pulses cause long-lived activation products to accumulate, leading to higher dose rates over time.
- Individual isotope contributions to the total dose rate can be identified and plotted separately.
