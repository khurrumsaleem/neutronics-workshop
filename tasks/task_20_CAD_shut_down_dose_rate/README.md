# Task Introduction

Please allow 45 minutes for this task.

In this task you will simulate shutdown dose rates on CAD geometry using the R2S (Rigorous 2-Step) method with unstructured meshes. This extends the shutdown dose rate concepts from task 11 to more realistic CAD-based geometries.

The unstructured mesh approach overlays a tetrahedral mesh on the DAGMC geometry, allowing material activation to be computed per mesh element. This enables spatially resolved gamma source terms that reflect the local neutron flux experienced by each region of the geometry.

**Learning Outcomes**

- CAD geometry can be used for shutdown dose rate simulations via the R2S method with unstructured meshes.
- An unstructured mesh tally provides spatially resolved flux and activation data across complex geometry.
- Each mesh element is individually activated and converted into a gamma source term for the photon transport step.
- The R2S workflow separates neutron transport, activation, and photon transport into distinct steps.
- Multiple materials can be handled simultaneously, each accumulating different activation products depending on their composition and local neutron flux.
