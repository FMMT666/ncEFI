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

F900

(rapid to: no name)
G00 Z20
G00 X10.000000 Y30.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X20.000000 Y-20.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X20.000000 Y-70.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X60.000000 Y30.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X70.000000 Y-20.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X70.000000 Y-70.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X-10.000000 Y30.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X-20.000000 Y-20.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X-20.000000 Y-70.000000
G00 Z0.000000
(rapid to: no name)
G00 Z20
G00 X55.000000 Y-90.000000
G00 Z0.000000
(END)
G00 Z20

M02
