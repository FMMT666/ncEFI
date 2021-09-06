(G-code start)
(The contents of this file can be used for the tool path creation)
(if the file name is used as a parameter for the toolCreateSimpleHeader)
(or the toolFullAuto function.)
(The file name must end with '_start.nc' and yes, these comments will)
(appear in the output file too :)

G21       (units are millimeters)
G94       (feedrate in 'units' per minute)
G17       (working in/on xy-plane)
G64 P0.05 (LinuxCNC, continuous mode with 'p' as tolerance)

G54       (use first WCS)

T1 M6     (select first tool)
S8000 M03
G04 P3    (wait for 3 seconds)

G43 H1    (set tool offset)

F900
(rapid to: zig)
G00 Z20
G00 X91.000000 Y0.000000
G00 Z-0.500000
(zig)
G01 X30.000000  
G02 X30.000000 Y1.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y3.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y4.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y6.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y7.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y9.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y10.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y12.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y13.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y15.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y16.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y18.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y19.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y21.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y22.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y24.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y25.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y27.000000 Z-0.500000 R0.750000
G01 X30.000000  
G02 X30.000000 Y28.500000 Z5.000000 R0.750000
G00 X91.000000  
G03 X91.000000 Y30.000000 Z-0.500000 R0.750000
G01 X30.000000  
(rapid to: zig)
G00 Z20
G00 X-50.000000 Y-50.000000
G00 Z1.000000
(zig)
G01 X10.000000  
G03 X10.000000 Y-48.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-47.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-45.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-44.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-42.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-41.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-39.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-38.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-36.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-35.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-33.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-32.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-30.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-29.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-27.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-26.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-24.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-23.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-21.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-20.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-18.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-17.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-15.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-14.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-12.500000 Z2.000000 R0.750000
G00 X-50.000000  
G02 X-50.000000 Y-11.000000 Z1.000000 R0.750000
G01 X10.000000  
G03 X10.000000 Y-9.500000 Z2.000000 R0.750000
G00 X-50.000000  

(G-code end)
(The contents of this file can be used for the tool path creation)
(if the file name is used as a parameter for the toolCreateSimpleFooter)
(or the toolFullAuto function.)
(The file name must end with '_end.nc' and yes, these comments will)
(appear in the output file too :)

(SPECIAL VARIABLES IN THIS FILE:)
( - GCODE_OP_SAFEZ in parenthesis will be replaced with the safeZ height)

G00 Z20

M02
