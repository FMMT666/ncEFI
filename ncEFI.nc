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
(rapid to: no name)
G00 Z20
G00 X-5.000000 Y0.000000
G00 Z0.000000
(no name)
G02 X5.000000 Y0.000000 Z0.000000 R5.000000
  X-5.000000 Y0.000000 Z0.000000 R5.000000
G03 X-5.833333 Y0.000000 Z0.000000 R0.416667
G02 X-6.666667 Y0.000000 Z0.000000 R0.416667
  X6.666667 Y0.000000 Z0.000000 R6.666667
  X-6.666667 Y0.000000 Z0.000000 R6.666667
G03 X-7.500000 Y0.000000 Z0.000000 R0.416667
G02 X-8.333333 Y0.000000 Z0.000000 R0.416667
  X8.333333 Y0.000000 Z0.000000 R8.333333
  X-8.333333 Y0.000000 Z0.000000 R8.333333

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
