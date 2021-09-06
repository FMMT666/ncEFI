
(G-code end)
(The contents of this file can be used for the tool path creation)
(if the file name is used as a parameter for the toolCreateSimpleFooter)
(or the toolFullAuto function.)
(The file name must end with '_end.nc' and yes, these comments will)
(appear in the output file too :)

(SPECIAL VARIABLES IN THIS FILE:)
( - GCODE_OP_SAFEZ in parenthesis will be replaced with the safeZ height)

G00 Z(GCODE_OP_SAFEZ)

M02
