G21 (units are millimeters)
G94 (feedrate in 'units' per minute)
G64P0.05 (continuous mode with 'p' as tolerance)
G17 (working in/on xy-plane)
T1M06
G00X0Y0 S6000 M03
F900
(rapid to: pups)
G00Z10
G00X0Y0
G00Z0
(pups)
G01X50Y50
G02X57.071067811865476Y42.928932188134524Z0R5.001
G01X7.0710678118654755Y-7.0710678118654755
(rapid to endposition)
G00Z10
G00X0Y0
M02
