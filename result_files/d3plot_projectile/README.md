Result files of an LS-DYNA projectile-plate impact simulation with element erosion and return the download paths available on the server side.

The dataset is the LSTC "Projectile Penetrating Plate" example (units: gram, cm, microsecond). 

A tungsten-alloy projectile impacts a steel plate at an angle. 

Both parts use ``*MAT_PLASTIC_KINEMATIC`` with a failure strain of 0.8, so elements are progressively eroded on impact.

The simulation uses ``*CONTACT_ERODING_SURFACE_TO_SURFACE``, which causes LS-DYNA to write the per-step element deletion flag to d3plot - exposed by DPF as the ``erosion_flag`` result.

The d3plot sequence contains 16 output states written to individual files (``ieverp=1``) at approximately 5 µs intervals up to a total simulation time of 70 µs.
