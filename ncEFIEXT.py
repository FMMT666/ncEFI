#!/usr/bin/python


#import ncEFITEST
from ncEFITEST import *




#  AVAILABLE FUNCTIONS:
# ======================
#
#  ELEMENTS (basic elements):
# ----------------------------
#
#  e=elemCreateVertex( (0, 0, 0) )
#                       x1 y1 z1
#
#  e=elemCreateArc180( (0, 50, 0), (-50, 30, 0 ), 40, 'cc')
#                       x1 y1  z1   x2   y2  z2  rad   dir
#
#  e=elemCreateLine( (-50, 30, 0),   (0, 0, 0))
#                     x1   y1  z1     x2 y2 z2
#
#  FUNCTIONS
#
#   e2=elemCopy(e1)
#   e=elemRotate(e, ang)
#   e=elemMove(e, vec)
#   e=elemReverse(e)
#
#   hits=elemIntersectsElemXY(e1,e2)
#   ang =elemNextAngle(e1,e2)
#   
#
#  GEOMS (complex geometry built of elements):
# ---------------------------------------------
#
#  g=geomCreateHelix( (50, 50, 0), 5,   10,   10,  'cw',<basNr=0>, <finish='finish'>)
#                      x1  y1  z1  dia depth steps dir    basNr     Finish/nofinish
#    
#  g=geomCreateConcentricCircles( (0, 0, 0),   30,    10,       5,    'cc')
#                                  x1 y1 z1 diastart diaend diasteps  dir
#
#  g=geomCreateCircRingHole( (0, 0, 0),    1,    50,     49,   5,     3,      2,    2,       5,  'cw')
#                             x1 y1 z1 diastart diaend diaSt depth depthst hdepth hdepthst clear dir
#
#
#  FUNCTIONS:
#
#  g = geomCreateContour(p,<distance>)
#  g = geomCreateSlotContour(p,<dist>,<basNr=0>)
#  g = geomCreateSlotContourFromElement(e,<dist>,<basNr=0>)
#  e = geomTrimPointsStartToEnd(e,<isClosed='notClosed'>)
#  g = geomCreateLeftContour(p,<dist>,<basNr=0>)
#  


#
#
#
#
#  PARTS:
# --------
#
# - creating a part 'p'
#     p = partCreate('name')
#
# - adding an element 'e' to part 'p'
#     p = partAddElement(p, element, <number>)
#
# - adding geoms 'g' to part 'p':
#     p = partAddElements(p,g)
#
#  OTHER FUNCTIONS:
#
#  p    = partDeleteNumbers(p)
#  nums = partGetFreeNumber(p)
#  e    = partGetElement(p, <number>)
#  bool = partCheckNumber(p, <number>)
#  bool = partCheckUniqueNumbers(p)
#  nums = partGetNumbers(p)
#  ???? = partGetLastPositionFromElements(<elements>)
#  pos  = partGetLastPosition(p)
#  pos  = partGetFirstPosition(p)
#  p    = partRenumber(p)
#  p    = partSortByNumber(p)
#  bool = partCheckContinuous(p)
#  bool = partCheckClosed(p)
#  
#              
#
#  GCODE OUTPUT
# --------------
#
# sample programming:
#
#
#  f=open('gcode.nc','w+t')
#  for i in toolCreateSimpleHeader():
#    f.write(i+'\n')
#  for i in toolRapidToNextPart(p1):
#    f.write(i+'\n')
#  for i in toolCreateFromPart(p1):
#    f.write(i+'\n')
#  for i in toolRapidToNextPart(p6):
#    f.write(i+'\n')
#  ...
#  for i in toolCreateSimpleFooter():
#    f.write(i+'\n')
#  f.close()



p1=partCreate('Schneidi')
g1=geomCreateConcentricCircles((0,0,0),10,20,10,'cw')
p1=partAddElements(p1,g1)


p2=partCreate('Huepfi')
g2=geomCreateHelix( (0, 0, 0), 5,   10,   10,  'cw',0, 'finish')
p2=partAddElements(p2,g2)


f=open('gcode.nc','w+t')
for i in toolCreateSimpleHeader():
  f.write(i+'\n')
for i in toolRapidToNextPart(p1):
  f.write(i+'\n')
for i in toolCreateFromPart(p1):
  f.write(i+'\n')
for i in toolRapidToNextPart(p2):
  f.write(i+'\n')
for i in toolCreateFromPart(p2):
  f.write(i+'\n')
for i in toolCreateSimpleFooter():
  f.write(i+'\n')
f.close()

