*KEYWORD
$
$
$
$ ===============
$ PARAMETER cards
$ ===============
$
*PARAMETER
R tend           2.0
$
$
$ ===========================
$ DEFINE_TRANSFORMATION cards
$ ===========================
$
*DEFINE_TRANSFORMATION
         1
TRANSL           0.0       0.0      50.0
$
$
$ ==================
$ INCLUDE_PATH cards
$ ==================
$
$
$
$
$ =============
$ INCLUDE cards
$ =============
$
*INCLUDE_TRANSFORM
YarisD_V2g_shock_abs_load_01_nodes.k
         0         0         0         0         0         0         0
         0
       0.0       0.0       0.0                   0
         1
$
*INCLUDE_TRANSFORM
YarisD_V2g_shock_abs_load_01.k
         0         0         0         0         0         0         0
         0
       0.0       0.0       0.0                   0
         1
$
*INCLUDE
fixed_ground.k
$
*INCLUDE
implicit_control_cards_R9.k
$
$
$
$ =============
$ CONTROL cards
$ =============
$
*CONTROL_IMPLICIT_AUTO
         1        25         5    1.0E-2       -99       0.0         0         0
*CONTROL_IMPLICIT_DYNAMICS
         0      0.55      0.28       0.0       0.0       0.0         0
$
$
$ ============
$ DEFINE cards
$ ============
$
$
*DEFINE_CURVE
$
$: Cross-reference summary for Load-curve 99
$: -----------------------------------------------
$
$: Control card <No label>: Max allowable timestep vs time
$: X axis : Time                       (Units: Time)
$: Y axis : Maximum allowable timestep  (Units: Time)
$
$: Usage: Transient analysis
$
        99         0       0.0       0.0       0.0       0.0         0
                 0.0        5.0000001E-2
           1.0000000        5.0000001E-2
           2.0000000        2.0000001E-2
           3.0000000        5.0000001E-2
$
$
*DEFINE_CURVE
$
$: Cross-reference summary for Load-curve 100
$: -----------------------------------------------
$
$: Boundary Prescribed Motion <No label>: Displacement vs time
$: X axis : Time                       (Units: Time)
$: Y axis : Prescribed displacement    (Units: Displacement)
$:    :
$: (To a total of 5 unlabelled Boundary Prescribed Motion entries)
$
$: Usage: Transient analysis
$
       100         0       0.0       0.0       0.0       0.0         0
                 0.0                 0.0
           100.00000                 0.0
$
$
*DEFINE_CURVE
$
$: Cross-reference summary for Load-curve 101
$: -----------------------------------------------
$
$: Boundary Prescribed Motion <No label>: Displacement vs time
$: X axis : Time                       (Units: Time)
$: Y axis : Prescribed displacement    (Units: Displacement)
$
$: Usage: Transient analysis
$
       101         0       0.0       0.0       0.0       0.0         0
                 0.0                 0.0
           1.0000000           1.0000000
           100.00000           1.0000000
$
$
*DEFINE_CURVE
$
$: Cross-reference summary for Load-curve 102
$: -----------------------------------------------
$
$: Body load definition <No label>: Base Z acceleration vs time
$: X axis : Time                       (Units: Time)
$: Y axis : Base Z acceleration        (Units: Acceleration)
$
$: Usage: Transient analysis
$
       102         0       0.0       0.0       0.0       0.0         0
                 0.0                 0.0
           1.0000000                 0.0
           2.0000000           1.0000000
           100.00000           1.0000000
$
$
$
$ ==============
$ BOUNDARY cards
$ ==============
$
*BOUNDARY_PRESCRIBED_MOTION_SET
       100         1         2       100       0.0         0       2.0       0.0
$
$: SET_NODE 100 is in include file Camry_V1_ag06a_einfedern.k
       100         2         2       100       0.0         0       2.0       0.0
$
$: SET_NODE 100 is in include file Camry_V1_ag06a_einfedern.k
       100         3         2       101      -5.0         0       1.1       0.0
$
$: SET_NODE 100 is in include file Camry_V1_ag06a_einfedern.k
       100         5         2       100       0.0         0       0.8       0.0
$
$: SET_NODE 100 is in include file Camry_V1_ag06a_einfedern.k
       100         6         2       100       0.0         0       0.9       0.0
$
$: SET_NODE 100 is in include file Camry_V1_ag06a_einfedern.k
       100         7         2       100       0.0         0       0.7       0.0
$
$: SET_NODE 100 is in include file Camry_V1_ag06a_einfedern.k
$
$
$ ==========
$ LOAD cards
$ ==========
$
*LOAD_BODY_Z
       102    9810.0         0
$
$
$ =============
$ CONTACT cards
$ =============
$
*CONTACT_AUTOMATIC_SURFACE_TO_SURFACE_MORTAR_ID
       100tires2ground                                                          
   2000008  10000001         2         3         0         0         1         1
       0.3       0.0       0.0       0.0       0.0         0       0.0       0.0
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
$
$
$: Cross-reference summary for SET_PART 2000008
$:---------------------------------------------
$: CONTACT 2
$
*SET_PART_LIST
   2000008       0.0       0.0       0.0       0.0
   2000487   2000211   2000490   2000367   2000488   2000360   2000363   2000489
$
$
$
$ =========
$ SET cards
$ =========
$
$
$
$ =============
$ INCLUDE cards
$ =============
$
$
*TITLE
CCSA TOYOTA Yaris STATIC shock absorber loading
$
$
*END
