#include "udf.h"

DEFINE_SDOF_PROPERTIES(store, prop, dt, time, dtime)
{

/* Define the mass matrix */
	prop[SDOF_MASS] = 5000.;
	prop[SDOF_IZZ] = 5000.;

/* add ejector forces, moments */
	if (time <= 0.3)
	{	
		prop[SDOF_LOAD_F_X] = -10000;
		prop[SDOF_LOAD_F_Y] = -80000;
		prop[SDOF_LOAD_M_Z] = -2200.0;
	}
	Message0("\nUpdated 6DOF properties\n");
}


