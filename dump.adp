
 ===================================================
  Athena Vortex Lattice  Program      Version  3.36
  Copyright (C) 2002   Mark Drela, Harold Youngren

  This software comes with ABSOLUTELY NO WARRANTY,
    subject to the GNU General Public License.

  Caveat computor
 ===================================================

 ==========================================================
   Quit    Exit program

  .OPER    Compute operating-point run cases
  .MODE    Eigenvalue analysis of run cases
  .TIME    Time-domain calculations

   LOAD f  Read configuration input file
   MASS f  Read mass distribution file
   CASE f  Read run case file

   CINI    Clear and initialize run cases
   MSET i  Apply mass file data to stored run case(s)

  .PLOP    Plotting options
   NAME s  Specify new configuration name

 AVL   c>  
 Reading file: test.avl  ...

 Configuration: Advanced                                                    

   Building surface: Wing                                    
     Reading airfoil from file: nlf0215f-il.dat
     Reading airfoil from file: nlf0215f-il.dat
     Reading airfoil from file: sd7062.dat
     Reading airfoil from file: sd7062.dat
     Reading airfoil from file: sd7062.dat
  
   Building duplicate image-surface: Wing (YDUP)                             

 Mach =    0.0000  (default)

    0 Bodies
    2 Solid surfaces
   40 Strips
  400 Vortices

    1 Control variables
    0 Design parameters

 Initializing run cases...

 AVL   c>  
 Operation of run case 1/1:   -unnamed-                              
 ==========================================================

  variable          constraint              
  ------------      ------------------------
  A lpha        ->  alpha       =   0.000         
  B eta         ->  beta        =   0.000         
  R oll  rate   ->  pb/2V       =   0.000         
  P itch rate   ->  qc/2V       =   0.000         
  Y aw   rate   ->  rb/2V       =   0.000         
  D1  Aileron   ->  Aileron     =   0.000         
  ------------      ------------------------

  C1  set level or banked  horizontal flight constraints
  C2  set steady pitch rate (looping) flight constraints
  M odify parameters                                    

 "#" select  run case          L ist defined run cases   
  +  add new run case          S ave run cases to file   
  -  delete  run case          F etch run cases from file
  N ame current run case       W rite forces to file     

 eX ecute run case             I nitialize variables     

  G eometry plot               T refftz Plane plot       

  ST  stability derivatives    FT  total   forces        
  SB  body-axis derivatives    FN  surface forces        
  RE  reference quantities     FS  strip   forces        
  DE  design changes           FE  element forces        
  O ptions                     FB  body forces           
                               HM  hinge moments         
                               VM  strip shear,moment    

 .OPER (case 1/1)   c>  
       constraint            value     
      - - - - - - - - - - - - - - - - -
   ->  A    alpha       =   0.000    
       B    beta        =   0.000    
       R    pb/2V       =   0.000    
       P    qc/2V       =   0.000    
       Y    rb/2V       =   0.000    
       C    CL          =   0.000    
       S    CY          =   0.000    
       RM   Cl roll mom =   0.000    
       PM   Cm pitchmom =   0.000    
       YM   Cn yaw  mom =   0.000    
       D1   Aileron     =   0.000    

      Select new  constraint,value  for alpha          c>  