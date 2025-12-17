/**********************************************************************/
/* mass & momentum source udfs for mass bleed through a wall.         */
/* These udfs compute the mass and momentum sources due to the        */
/* fluid bleed.  The direction of the infusion is normal to the wall. */
/**********************************************************************/

/* All constants must be in SI units                                  */

#include "udf.h"

#define mflux_ref -825.0   /* reference Massflux, kg/(sec*m2), though inlet */
#define p_ref     101325.0 /* reference static pressure at inlet, Pa        */ 
#define sigma     0.01     /* bleed plate factor                            */
#define h         4e-06    /* Height of the bleed layer cell, m             */
#define At        0.05	   /* Total area of the bleed plate, m2             */
#define Ah        0.025    /* Total area of the bleed plate holes, m2       */
#define zoneid    8        /* Zone id of the infusion wall                  */

#define mflux mflux_ref*sigma  /* mass flux rate through seed plate */
#define prs  -(At/Ah)/h


DEFINE_ADJUST(adjust_infusion_wall,d)
{
  real mass_source, xmom_source, ymom_source, zmom_source;
  real p_stat, dp;
  real mscr, snrm;
  real nx, ny, nz;
  real area;

#if !RP_HOST
  Thread *t=Lookup_Thread(d,zoneid);
  Thread *tc0;
  cell_t c0;
  face_t f;
  real A[ND_ND];
  
  begin_f_loop(f,t) {
    
    if (PRINCIPAL_FACE_P(f,t)) {
      
      tc0=THREAD_T0(t);
      c0=F_C0(f,t);
      
      p_stat = C_P(c0,tc0);   
      dp = p_stat/p_ref-1.0;
      mass_source = mflux/h*dp;
      
      mscr = mflux*dp;
      snrm = pow(mscr,2.0)*prs/C_R(c0,tc0);
      
      F_AREA(A,f,t);
      area = NV_MAG(A);
      nx = -A[0]/area;
      ny = -A[1]/area;
      nz = -A[2]/area;
      
      xmom_source = snrm*nx;
      ymom_source = snrm*ny;
      zmom_source = snrm*nz;
      
      C_UDMI(c0,tc0,0)=c0;
      C_UDMI(c0,tc0,1)=mass_source;
      C_UDMI(c0,tc0,2)=xmom_source;
      C_UDMI(c0,tc0,3)=ymom_source;
      C_UDMI(c0,tc0,4)=zmom_source;
      
    };
  } end_f_loop(f,t);
	
#endif 

}

DEFINE_SOURCE(mass_source,c,t,dS,eqn)
{ 
#if !RP_HOST
  real source=0.0;
  dS[eqn]=0;
  if((C_UDMI(c,t,0)==c)&&(c>0)){
    source = C_UDMI(c,t,1);
    /*    Message0("Applying ms = %10.3e at cell %i\n",source,c);*/
  }

  return source;
#endif 
}

DEFINE_SOURCE(xmom_source,c,t,dS,eqn)
{
#if !RP_HOST
  real source=0.0;
  dS[eqn]=0;
  if((C_UDMI(c,t,0)==c)&&(c>0)){
    source = C_UDMI(c,t,2);
    /*    Message0("Applying xs = %10.3e at cell %i\n",source,c);*/
  }

  return source;
#endif  
}

DEFINE_SOURCE(ymom_source,c,t,dS,eqn)
{
#if !RP_HOST
  real source=0.0;
  dS[eqn]=0;
  if((C_UDMI(c,t,0)==c)&&(c>0)){
    source = C_UDMI(c,t,3);
    /*    Message0("Applying ys = %10.3e at (%f,%f)\n",source,xc[0],xc[1]);*/
  }

  return source;
#endif  
}

DEFINE_SOURCE(zmom_source,c,t,dS,eqn)
{
#if !RP_HOST
  real source=0.0;
  dS[eqn]=0;
  if((C_UDMI(c,t,0)==c)&&(c>0)){
    source = C_UDMI(c,t,4);
    /*    Message0("Applying zs = %10.3e at cell %i\n",source,c);*/
  }

  return source;
#endif  
}

