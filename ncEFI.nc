G21       (units are millimeters)
G94       (feedrate in 'units' per minute)
G17       (working in/on xy-plane)
G64 P0.05 (LinuxCNC, continuous mode with 'p' as tolerance)

G54       (use first WCS)

(DEBUG,CHECK WCS NOW!)
M0        (pause and display message)
G4 P1     (wait for 1 second)

T1 M6     (select first tool)
S8000 M03
G04 P3    (wait for 3 seconds)

G43 H1    (set tool offset)

(DEBUG,CHECK TOOL OFFSET NOW!)
M0        (pause and display message)
G4 P1     (wait for 1 second)

F4444      (base feed rate, set in code)

(rapid to: no name)
G00 Z10.0
G00 X-25.811388 Y57.434165
G00 Z10.000000
(no name)
(TODO: add new feed rate here: Fxyz)
G03 X5.811388 Y-37.434165 Z6.882697 R50.000000
G01 X95.811388 Y-7.434165 Z5.000000
G03 X64.188612 Y87.434165 Z1.882697 R50.000000
G01 X-25.811388 Y57.434165 Z0.000000
G03 X5.811388 Y-37.434165 Z-3.117303 R50.000000
G01 X95.811388 Y-7.434165 Z-5.000000
G03 X64.188612 Y87.434165 Z-8.117303 R50.000000
G01 X-25.811388 Y57.434165 Z-10.000000
(TEST COMMENT: NOW MILLING; millmillmillmill)
(TODO: add new feed rate here: Fxyz)
G03 X5.811388 Y-37.434165 Z-10.000000 R50.000000
G01 X95.811388 Y-7.434165 
G03 X64.188612 Y87.434165 Z-10.000000 R50.000000
G01 X-25.811388 Y57.434165 
G02 X-28.446620 Y65.339859 Z-10.000000 R4.166667
G03 X-31.081851 Y73.245553 Z-10.000000 R4.166667
  X11.081851 Y-53.245553 Z-10.000000 R66.666667
G01 X101.081851 Y-23.245553 
G03 X58.918149 Y103.245553 Z-10.000000 R66.666667
G01 X-31.081851 Y73.245553 
G02 X-33.717082 Y81.151247 Z-10.000000 R4.166667
G03 X-36.352314 Y89.056942 Z-10.000000 R4.166667
  X16.352314 Y-69.056942 Z-10.000000 R83.333334
G01 X106.352314 Y-39.056942 
G03 X53.647686 Y119.056942 Z-10.000000 R83.333334
G01 X-36.352314 Y89.056942 
(TODO: add new feed rate here: Fxyz)
G03 X-31.081851 Y73.245553 Z-7.500000 R8.333334
G02 X-25.811388 Y57.434165 Z-5.000000 R8.333333
(TODO: add new feed rate here: Fxyz)
G03 X5.811388 Y-37.434165 Z-8.117303 R50.000000
G01 X95.811388 Y-7.434165 Z-10.000000
G03 X64.188612 Y87.434165 Z-13.117303 R50.000000
G01 X-25.811388 Y57.434165 Z-15.000000
G03 X5.811388 Y-37.434165 Z-18.117303 R50.000000
G01 X95.811388 Y-7.434165 Z-20.000000
G03 X64.188612 Y87.434165 Z-23.117303 R50.000000
G01 X-25.811388 Y57.434165 Z-25.000000
(TEST COMMENT: NOW MILLING; millmillmillmill)
(TODO: add new feed rate here: Fxyz)
G03 X5.811388 Y-37.434165 Z-25.000000 R50.000000
G01 X95.811388 Y-7.434165 
G03 X64.188612 Y87.434165 Z-25.000000 R50.000000
G01 X-25.811388 Y57.434165 
G02 X-28.446620 Y65.339859 Z-25.000000 R4.166667
G03 X-31.081851 Y73.245553 Z-25.000000 R4.166667
  X11.081851 Y-53.245553 Z-25.000000 R66.666667
G01 X101.081851 Y-23.245553 
G03 X58.918149 Y103.245553 Z-25.000000 R66.666667
G01 X-31.081851 Y73.245553 
G02 X-33.717082 Y81.151247 Z-25.000000 R4.166667
G03 X-36.352314 Y89.056942 Z-25.000000 R4.166667
  X16.352314 Y-69.056942 Z-25.000000 R83.333334
G01 X106.352314 Y-39.056942 
G03 X53.647686 Y119.056942 Z-25.000000 R83.333334
G01 X-36.352314 Y89.056942 
(TODO: add new feed rate here: Fxyz)
G03 X-31.081851 Y73.245553 Z-22.500000 R8.333334
G02 X-25.811388 Y57.434165 Z-20.000000 R8.333333
(TODO: add new feed rate here: Fxyz)
G03 X5.811388 Y-37.434165 Z-23.117303 R50.000000
G01 X95.811388 Y-7.434165 Z-25.000000
G03 X64.188612 Y87.434165 Z-28.117303 R50.000000
G01 X-25.811388 Y57.434165 Z-30.000000
G03 X5.811388 Y-37.434165 Z-33.117303 R50.000000
G01 X95.811388 Y-7.434165 Z-35.000000
G03 X64.188612 Y87.434165 Z-38.117303 R50.000000
G01 X-25.811388 Y57.434165 Z-40.000000
(TEST COMMENT: NOW MILLING; millmillmillmill)
(TODO: add new feed rate here: Fxyz)
G03 X5.811388 Y-37.434165 Z-40.000000 R50.000000
G01 X95.811388 Y-7.434165 
G03 X64.188612 Y87.434165 Z-40.000000 R50.000000
G01 X-25.811388 Y57.434165 
G02 X-28.446620 Y65.339859 Z-40.000000 R4.166667
G03 X-31.081851 Y73.245553 Z-40.000000 R4.166667
  X11.081851 Y-53.245553 Z-40.000000 R66.666667
G01 X101.081851 Y-23.245553 
G03 X58.918149 Y103.245553 Z-40.000000 R66.666667
G01 X-31.081851 Y73.245553 
G02 X-33.717082 Y81.151247 Z-40.000000 R4.166667
G03 X-36.352314 Y89.056942 Z-40.000000 R4.166667
  X16.352314 Y-69.056942 Z-40.000000 R83.333334
G01 X106.352314 Y-39.056942 
G03 X53.647686 Y119.056942 Z-40.000000 R83.333334
G01 X-36.352314 Y89.056942 
(TODO: add new feed rate here: Fxyz)
G03 X-31.081851 Y73.245553 Z-15.000000 R8.333334
G02 X-25.811388 Y57.434165 Z10.000000 R8.333333
(END)
G00 Z10.0   (the default safe-z position, set in code)

M02
