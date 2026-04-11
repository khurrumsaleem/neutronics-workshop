# Task Introduction

Please allow 20 minutes for this task.

Expected outputs from this task are also in the [presentation](https://slides.com/neutronics_workshop/neutronics_workshop#/15).

In this task you will use OpenMC to simulate transmutation, activation and depletion of materials under neutron irradiation. The examples progress from a simple flux-spectrum-based depletion (no transport required) through to coupled transport-depletion simulations with pulsed irradiation schedules.

**Learning Outcomes**

- OpenMC can perform depletion using a precomputed multigroup flux spectrum, similar to inventory codes like FISPACT, ORIGEN and ALARA. This is fast and requires no geometry.
- OpenMC can also perform coupled transport-depletion where the neutron flux is recalculated as the material composition evolves.
- Activation products build up during irradiation and start to saturate at around five half-lives, when the rate of creation approaches the rate of decay.
- Activity, decay heat and contact dose rate can be extracted from depleted materials.
- Material evolution during irradiation affects tally results. For example, Tritium Breeding Ratio decreases as lithium-6 is burnt up.
- Pulsed irradiation schedules can be modelled to simulate realistic reactor operating conditions.