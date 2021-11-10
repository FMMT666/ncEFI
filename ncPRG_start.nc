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

F(GCODE_OP_BFEED)      (base feed rate, set in code)
