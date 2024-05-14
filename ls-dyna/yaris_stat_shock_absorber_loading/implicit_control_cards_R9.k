*KEYWORD
*CONTROL_ACCURACY
         1         4         0         1
*CONTROL_BULK_VISCOSITY
       0.0       0.0        -1         0
$*CONTROL_CONTACT
$       0.1       1.0         2         0         1         0         1         0
$         0         0         0         0       0.0         0         0         0
$       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
$         2         0         0         0         0         0       0.0
*CONTROL_CONTACT
$:  slsfac    rwpnal    islchk    shlthk    penopt    thkchg     orien    enmass
                 1.0         2         2
$:  usrstr    usrfrc     nsbcs    interm     xpene     ssthk      ecdt   tiedprj
                                                  
$:   sfric     dfric       edc       vfc        th     th_sf    pen_sf
                                                                      
$:  ignore    frceng   skiprwg    outseg   spotstp   spotdel   spothin
         2                             1         2         1       0.5
$:    isym    nserod    rwgaps    rwgdth     rwksf      icov    swradf    ithoff

$:  shledg    pstiff    ithcnt    tdcnof     ftall              shltrw
                                                 1                    
*CONTROL_ENERGY
         2         2         2         2
*CONTROL_HOURGLASS
         0       0.0
*CONTROL_IMPLICIT_GENERAL
         1      0.01         0         0         0         0         0         0
*CONTROL_IMPLICIT_SOLUTION
        12         6        15   2.5e-3        0.0       0.0       0.0     1e-13
         1         0         0         1         0         0         0
*CONTROL_IMPLICIT_SOLVER
         5         1         0         0         0       0.0         0       0.0
*CONTROL_MPP_IO_NODUMP
*CONTROL_OUTPUT
         1         3         0         1       0.0         0       100         0
*CONTROL_SHELL
      70.0         1        -1         1         2         2         1         1
*CONTROL_SOLID
         1         0         0         0         0       0.0         0
*CONTROL_SOLUTION
         0         0         1         0
*CONTROL_TIMESTEP
       0.0       0.0         0       0.0   -1.0E-3         0         0         0
*CONTROL_TERMINATION
&tend
$
*DATABASE_ABSTAT
      0.01         0         0         0
*DATABASE_DEFORC
      0.01         0         0         0
*DATABASE_ELOUT
      0.01         0         0         0
*DATABASE_GLSTAT
      0.01         0         0         0
*DATABASE_JNTFORC
      0.01         0         0         0
*DATABASE_MATSUM
      0.01         0         0         0
*DATABASE_NODOUT
      0.01         0         0         0       0.0         0
*DATABASE_RBDOUT
      0.01         0         0         0
*DATABASE_RCFORC
      0.01         0         0         0
*DATABASE_SBTOUT
      0.01         0         0         0
*DATABASE_SLEOUT
      0.01         0         0         0
*DATABASE_BINARY_D3PLOT
    1.0E-1         0         0         0         0
*DATABASE_BINARY_D3DUMP
        30
*DATABASE_EXTENT_BINARY
         0         0         0         0         1         1         1         1
         0         1         0         0         0         0         0         0
         0         0       0.0         0         0         0                    
         0         1         0
*DATABASE_FORMAT
         0         1
$
*END
