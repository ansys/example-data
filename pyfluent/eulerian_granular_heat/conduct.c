#include "udf.h"


#define OMEGA 7.26E-3
#define K_F0 0.0257
#define K_S0 1.0

real 
k_solid(real e_gas)
{
  real k_sol;
  real a = K_S0/K_F0;
  real b = 1.25*pow((1.-e_gas)/e_gas, 10./9.);
  real t1 = (a-1.)/pow((1.-b/a),2.0)*(b/a)*log(a/b);
  real t2 = -((b-1.)/(1.-b/a))-0.5*(b+1.);
  real gm = (2./(1.-b/a))*(t1+t2);
  real k_bs = K_F0*(OMEGA*a + (1.-OMEGA)*gm);
  k_sol = k_bs/sqrt(1.-e_gas);
  return (k_sol);
}

DEFINE_PROPERTY(conduct_gas,cell,thread)
{
  real k_bf, k_gas;
  k_bf = K_F0*(1.-sqrt(1.-C_VOF(cell,thread)));
  k_gas = k_bf/C_VOF(cell, thread);
  return (k_gas);
}


DEFINE_PROPERTY(conduct_solid,cell,thread)
{
  real k_sol;
  real epsi_max = 1.-10*SD_EPS;
  real epsi = MIN( epsi_max, (1.-C_VOF(cell,thread)));
  k_sol = k_solid(epsi);
  return (k_sol);
}

