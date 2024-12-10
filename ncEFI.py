#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ncEFI
# Some stupid G-Code ideas I had about 27 years ago.
# Yes, really, really stupid.
# FMMT666/ASkr 1995..2024 lol

# This code uses tabs. Best viewed with four of them.


# TODO:
#
# >>> Okay, the "feed rate vertices" are now built-in. Now:
# >>>  - DONE: make the "continous" checks and toolpath creation ignore them
# >>>  - DONE: add 'tFeed_xyz' keys to the part dict
# >>>    - DONE: if they are missing, the toolpath will not create any feed rate commands
# >>>    - DONE: add a global base feedrate; also in header file
# >>>    - TODO: add a local base feedrate to parts, overriding the global one
# >>>            YO SHIT: Very clever to allow geoms to be passed to ToolFullAuto().
# >>>                     The planned feed rates _ENGAGE, _BASE, and _RERACT would now need to
# >>>                     to be in the geoms too - and that's not possible because a geom is
# >>>                     just a list, which may contain an unlimited amount of other geoms.
# >>>
# >>>                 No wait, that's not true. Each of the geoms is a single entry in a list.
# >>>                 That could and should be treated as a part.
# >>>           
# >>>      >>>   ANYWAY, THIS NEEDS A NEW STRATEGY
# >>>            Same keys in geoms, for example??
# >>>
# >>>      >>>   No. That would not be okay.
# >>>      >>>   Actually, the toolFullAuto() is the limiting element.
# >>>      >>>   Without it, the part functions _Create or _AddElelemnts
# >>>      >>>   or something new like _AddFeed could be used. 
# >>>
# >>>    - TODO: add at least two, the ENGAGE and RETRACT feedrates or percentage markers to parts
# >>>    - TODO: This should create a warning bc the feed rate might have been changed
# >>>            in the previous (part) operation!
# >>>    - TODO: if they contain numbers (already replaced by another function): put these in the G-code
# >>>    - TODO: if they contain the 'FEED_ENGAGE', 'FEED_BASE', 'FEED_RETRACT' markers, put the default values in
# >>> 
# >>>  - algorithm for contours of closed polygons:
# >>>    - DONE: calc points between half angles; in- and outside
# >>>    - TODO: method to identify crossing half-angle vectors (ncVec.py)
# >>>    - TODO: outer contours with arcs
# >>>    - TODO: algorithm for arcs in inner contour possible?
# >>>
# >>>  - TODO: add debug-color to elements in extras
# >>>  - TODO: type annotations would be helpful; even testing became a pita
# >>>  - TODO: docstrings for all functions
# >>>  - TODO: pylint stopped working; wasn't able to make flake8 work in VSCode
# >>>  - DONE: the segmentation fault upon exit is caused by a (now fixed in git) bug; will self-heal someday
# >>>
# >>>
# - toolFeedRateSet() in the test file
# - Maybe the global safe-Z variable should be handled like the feed rate,
#   so that the default value, without overriding it, causes an error? 
#   Would be safer.
# - shall there be a function to set the safe-Z postion accordingly to the global feed rate? Would make sense
# - toolFullAuto() might set the global base feed rate too
# - toolCreateSimpleHeader() should be able to return an error, in case the new base feed rate is invalid
#
# These should be removed. Theoretically, they're not required, but built-in everywhere (CHECK THIS FIRST! Might break everything!)
#   pNr     <- number of element in part
#   pNext   <- if chained -> number of next element
#   pPrev   <- if chained -> number of previous element
#
#  - allow RAPID in 'tMove' for G2/3 (set feed rate to a predefined, high value)
#  - geomCreateSlotHole, geomCreateConcentricSlots, geomCreateCircRingHole, geomCreateConcentricCircles:
#      - the "diaSteps" should be replaced by a "diaInc" for better usage
#  - maybe renaming the hole functions would make sense?
#      - geomCreateCircRingHole  -> geomCreateHoleRingCircle (CircleRing? ConcentricCircles?)
#      - geomCreateSlotHole[...] -> geomCreateHoleRingSlot   (SlotRing?   ConcentricSlots?)
#  - geomCreateSlotSpiral:
#      - sth like a "doNotRotate" option, for usage in geomCreateSlotHole??
#      - add more error checks
#  - what's with this "basNr" stuff? Remove that completely?
#  - geomCreateSlotHole:
#      - add geomCreateSlotSpiral as entry movement
#      - add depth
#      - add retract movement
#      - rotate geom to final position
#  - add proper "ERR:" prints in ncVec
#  - ncVec's rotate and vecAngle functions handle angles in the opposite direction (ugh)
#    rotate is right-handed, vecAngle is left-handed; for positive angles
#  - add arcLength for z changes (half helix)
#  - geomCreateConcentricRects
#      - implement depth (if not already done)
#      - implement correct amount of Bezier line segments
#      - implement helix (if that makes sense)
#  - geomCreateRadial
#      - add the 'arc' operation
#      - add rapid retracts (requires the "feed-rate-in-vertices" idea)
#  - geomCreatePoly
#  - geomCreatePolyHelix
#  - geomCreateRectSpiral       REALLY?
#  - geomCreateRectSpiralHelix  REALLY?
#  - improve geomCreateCircRingHole:
#      - arguments' names
#      - 'clear' does (yet) nothing
#      - the new retract movement should be an arc
#      - ...
#  - after implementing the possibility to read nc header and footer a file, the variables do not make sense any more
#  - geomCreateSpiralToCircle() needs more error checks
#  - geomCreateHelix() uses 'finish' for 'finish' (lol), but shold have sth likr "clearBottom=True"#  - more error checks for 'dir' (almost everywhere)
#  - option needed to use different feed rates in multi-geom functions like geomCreateCircRingHole
#  - the 'turns' geomCreateSpiralHelix could be a float instead of an int, allowing less than 360° turns
#  - add retract movement or at least a "retractPt" to all the geom functions; last move to move the tool out
#  - toolRapidToNextPart needs a better and valid solution to determine the really necessary height. Now just fixed.
#  - avoid putting out arc z moves in toolCreate if z didn't change
#  - add ncEFIDisp2 support for circle    ??? Häh?
#  - add tool support for circle
#  - add IJK circle and arcs
#  - add geomCreateSlotArc
#  - add geomCreateSlotBezier
#  - add geomMoveTo; should be a 3-liner (theoretically :)
#  - add spiral pocket geom (using SpiralHelix and Circle)
#  - split ncEFI into several files, maybe elem, geom, part, tool?
#  - change geomCreateConcentricCircles
#      - rename to geomCreateConcentricCirclesConnected
#      - add another approach to connect the circles via a spiral
#      - make use of the new geomCreateCircle() function
#  - whatever the 'basNr' parameter in some geom function shall do - it doesn't; purpose??


import os       # only for 'debugShowViewer()'
import sys      # only for 'debugShowViewer()'

import math
import pickle

from ncVec import *

# some tolerances and precision things
TOOL_CONTINUOUS_TOLERANCE = 0.001                # checks for tool path continuity; if mm, this makes 1um...
MINLEN_BEZIER             = 0.1                  # minimum length of Bezier interpolation segment; for some createGeom
DEFLEN_BEZIER             = 0.5                  # default length of Bezier interpolation segment; for some createGeom
MAXLEN_BEZIER             = 2.0                  # maximum length of Bezier interpolation segment; for some createGeom
MINOFFSETANGLE            = 2.0 * math.pi / 365  # minimum allowed angle for offsetting calcs; see: vn = ( offset / math.sin( ad / 2.0 ), 0, 0)
RAYCAST_POINTS            = [ (+9965, +210, 0),  # raycast test points
                              (-7434,-6234, 0),
                              ( -320,-9764,0) ]

# default G-codes also used as "state markers" during the tool path creation
GCODE_COMMENT        = "()"
GCODE_FEED           = "F"
GCODE_RAPID          = "G00"
GCODE_LINE           = "G01"
GCODE_ARC_CW         = "G02"
GCODE_ARC_CC         = "G03"

# default safe-Z height
GCODE_OP_SAFEZ     = 10.0  # the default, safe z-height if nothing else is given or overridden
GCODE_OP_BFEED     = 0     # the base feed rate; needs to be set by code; via toolFeedRateSet()

# default G-code end for when no "start G-code" file is given
GCODE_PRG_START = [\
'G21       (units are millimeters)',\
'G94       (feedrate in \'units\' per minute)',\
'G17       (working in/on xy-plane)',\
'G64 P0.05 (LinuxCNC, continuous mode with \'p\' as tolerance)',\
'',\
'G54       (use first WCS)',\
'',\
'(DEBUG,CHECK WCS NOW!)',\
'M0        (pause and display message)',\
'G4 P1     (wait for 1 second)',\
'',\
'T1 M6     (select first tool)',\
'S8000 M03',\
'G04 P3    (wait for 3 seconds)',\
'',\
'G43 H1    (set tool offset)',\
'',\
'(DEBUG,CHECK TOOL OFFSET NOW!)',\
'M0        (pause and display message)',\
'G4 P1     (wait for 1 second)',\
'',\
'F(GCODE_OP_BFEED)      (base feed rate, set in code)',\
'']

# default G-code end for when no "end G-code" file is given
GCODE_PRG_END = [\
'G00 Z(GCODE_OP_SAFEZ)   (the default safe-z position, set in code)',\
'',\
'M02']

# looks like a very clever thing, lol
EXTRA_MOVE_RAPID   = "RAPID"         # for 'tMove' in line extras; creates G00 instead of G01




#############################################################################
# elements
# a directory containing basic geometry; vertex, line or arc
# vertex
#   v1 = {'type':'v','p1':(0,0,0)}
#
# line
#   l1 = {'type':'l','p1':(0,0,0),'p2':(100,0,0)}
#   l2 = {'type':'l','p1':(100,0,0),'p2':(100,50,0)}
#   l3 = {'type':'l','p1':(100,50,0),'p2':(0,50,0)}
#   l4 = {'type':'l','p1':(0,50,0),'p2':(0,0,0)}
#
# arc 180° max
#   a1 = {'type':'a','p1':(0,0,0),'p2':(100,0,0),'rad':70,'dir':'cw'}
#   a2 = {'type':'a','p1':(100,50,0),'p2':(0,50,0),'rad':70,'dir':'cw'}
#
# allowed extensions, aka "extras"
#   pNr     <- number of element in part
#   pNext   <- if chained -> number of next element
#   pPrev   <- if chained -> number of previous element
#   tMove   <- only for lines: if set to 'RAPID', a G0 rapid move will be created instead of a G1
#   tFeed   <- only for vertices, mark the beginning of a new feed rate here.
#               tFeed can either be a string:
#                 'FEED_ENGAGE'
#                 'FEED_BASE'
#                 'FEED_RETRACT'
#               or a number (integers only):
#                 900
#   tMsg    <- only for vertices, so far; a string that will appear as a comment in the G-code file

#############################################################################
# geometry
# just a list of multiple elements; can directly be added to parts
#   [ v1, l1, l2, a1 ... l21 ]
#   [ {'type':'v','p1':(0,0,0)}, {'type':'l','p1':(100,0,0),'p2':(100,50,0)}, ... ]

#############################################################################
# parts
# basically geometry in a directory; the geoms are in the 'elements' list.
# Can be used to create toolpaths.
#   p1={'type':'p', 'name':'outer','elements':[l1,l2,l3,l4]}
#   p2={'type':'p', 'name':'altc1','elements':[a1,l2,l3,l4]}
#   p3={'type':'p', 'name':'altc2','elements':[l1,l2,a2,l4]}
#
# allowed extensions, aka "extras"
#   tFeed_Engage  <-+
#   tFeed_Base    <-+
#   tFeed_Retract <-+
#                   |
#                   For all of the three feed rate specifiers:
#                     - a number > 0           : an absolute feed rate, e.g. "300"
#                     - a string 'nnn%'        : a percentage of the local or global (GCODE_OP_BFEED) base feed rate, e.g. '50%'
#                     - a 0 (zero) or '0%'     : no feed rate output in the G-Code for this operation
#                   For "tFeed_Base" specials:
#                     - if 0 (zero) or 'nnn%', the _global_ feed rate (GCODE_OP_BFEED, parsed from the last valid Fnnn value in
#                       GCODE_PRG_START or set by 'toolFeedRateSet()') or a percentage of it, is used as a base feed rate for this part.
#                     - if > 0, then this ("local") value will be used as a base feed rate for tFeed_Base and tFeed_Retract



#############################################################################
### elemAddExtra
###
#############################################################################
def elemAddExtra(elem,extra):
	for i in extra:
		if i == 'pNr':
			elem['pNr'] = extra['pNr']
		if i == 'pNext':
			elem['pNext'] = extra['pNext']
		if i == 'pPrev':
			elem['pPrev'] = extra['pPrev']
		if i == 'tMove':
			elem['tMove'] = extra['tMove']

		# TESTING TESTING TESTING
		if i == 'tFeed':
			elem['tFeed'] = extra['tFeed']

		# TESTING TESTING TESTING
		if i == 'tMsg':
			elem['tMsg'] = extra['tMsg']



#############################################################################
### elemCreateVertex
###
#############################################################################
def elemCreateVertex(p1,extra={}):
	if isinstance(p1,tuple) == False:
		return {}
	ret={'type':'v','p1':p1}
	elemAddExtra(ret,extra)
	return ret



#############################################################################
### elemCreateLine
###
#############################################################################
def elemCreateLine(p1,p2,extra={}):

	if isinstance(p1, tuple) == False or isinstance(p2,tuple) == False:
		print( "ERR: elemCreateLine: p1 or p2 not tuples" )
		return {}
	if p1 == p2:
		print( "ERR: elemCreateLine: p1 == p2: ",p1 )
		return {}
	ret={'type':'l','p1':p1,'p2':p2}
	elemAddExtra(ret,extra)
	return ret



#############################################################################
### elemCreateLineTo
###
#############################################################################
def elemCreateLineTo(e1,p2,extra={}):

	if not 'type' in e1:
		print( "ERR: elemCreateLineTo: element 'e1' has no 'type'" )
		return {}

	if   e1['type'] == 'v':
		pt = e1['p1']
	elif e1['type'] == 'l' or e1['type'] == 'a':
		pt = e1['p2']
	else:
		print( "ERR: elemCreateLineTo: unknown 'type' in 'e1':", e1['type'] )
		return {}

	if isinstance(p2,tuple) == False:
		print( "ERR: elemCreateLine: p2 not tuple" )
		return {}

	if pt == p2:
		print( "ERR: elemCreateLine: pt == p2: ",pt )
		return {}

	ret={'type':'l','p1':pt,'p2':p2}
	elemAddExtra(ret,extra)
	return ret



#############################################################################
### elemCreateLineBetween
###
#############################################################################
def elemCreateLineBetween(e1,e2,extra={}):

	if not 'type' in e1:
		print( "ERR: elemCreateLineTo: element 'e1' has no 'type'" )
		return {}

	if not 'type' in e2:
		print( "ERR: elemCreateLineTo: element 'e2' has no 'type'" )
		return {}

	if   e1['type'] == 'v':
		p1 = e1['p1']
	elif e1['type'] == 'l' or e1['type'] == 'a':
		p1 = e1['p2']
	else:
		print( "ERR: elemCreateLineTo: unknown 'type' in 'e1':", e1['type'] )
		return {}

	if e2['type'] == 'v' or e2['type'] == 'l' or e1['type'] == 'a':
		p2 = e2['p1']
	else:
		print( "ERR: elemCreateLineTo: unknown 'type' in 'e2':", e2['type'] )
		return {}

	if p1 == p2:
		print( "ERR: elemCreateLine: e1 and e2 share same coordinates: ", p1 )
		return {}

	ret={'type':'l','p1':p1,'p2':p2}
	elemAddExtra(ret,extra)
	return ret



#############################################################################
### elemCreateArc180
###
### While rad is taken from a projection to the xy-plane, z may vary but
### will be stepped through linear.
### If 'rad' is below the possible minimum to create an arc, it is set to
### the minimum value, half of the distance between p1 and p2.
### TODO: Is the 'dir' parameter actually useful? Have p1 and p2 already!?
#############################################################################
def elemCreateArc180(p1,p2,rad,dir,extra={}):
	if isinstance(p1,tuple) == False or isinstance(p2,tuple) == False:
		print( "ERR: elemCreateArc180: no tuples" )
		return {}
	if p1 == p2:
		print( "ERR: elemCreateArc180: p1==p2: ", p1,p2 )
		return {}
	if isinstance(dir,str) == False:
		print( "ERR: elemCreateArc180: invalid dir format: ",dir )
		return {}
	if dir != 'cw' and dir != 'cc':
		print( "ERR: elemCreateArc180: invalid dir command: ",dir )
		return {}
	dist=vecLength((p1[0],p1[1],0),(p2[0],p2[1],0))
	if rad < dist/2.0:
		rad = dist/2.0
		if rad + RADTOL > dist / 2.0:
			rad = dist/2.0
		else:
			print( "ERR: elemCreateArc180: rad less than dist/2: rad, dist/2",rad,dist/2.0 )
			return {}
	ret={'type':'a','p1':p1,'p2':p2,'rad':rad,'dir':dir}
	elemAddExtra(ret,extra)
	return ret



#############################################################################
### elemCreateArc180To
###
### Just calls elemCreateArc180 with an already known element position.
#############################################################################
def elemCreateArc180To(elem1,p2,rad,dir,extra={}):
	if isinstance(elem1['p2'],tuple) == False:
		print( "ERR: elemCreateArc180To: elem1 has no tuple in p2" )
		return {}
	return elemCreateArc180(elem1['p2'],p2,rad,dir,extra)



#############################################################################
### elemCreateArc180by3Pts
###
### Creates a (max 180°) arc from p1 to p2, "through pm".
### Notice that 'pm' might not be on the visible part of the arc, but
### either behind 'p1' or 'p2'. Invalid arcs, which might occur if 'pm'
### (or the resulting center of the arc) is on the wrong side of the
### vector p1->p2, will not be allowd.
### Z will be stepped through linear from p1 to p2, ignoring any z value
### specified for point pm.
### It is an error if pm is too far away, resulting in an arc >180°.
#############################################################################
def elemCreateArc180by3Pts(p1,p2,pm,dir,extra={}):
	if not isinstance(p1,tuple) or not isinstance(p2,tuple) or not isinstance(pm,tuple):
		print( "ERR: elemCreateArc180by3Pts: no tuples" )
		return {}
	if p1 == p2 or p1 == pm or p2 == pm:
		print( "ERR: elemCreateArc180by3Pts: same coords for p1, p2, pm: ", p1,p2,pm )
		return {}
	if not isinstance(dir,str):
		print( "ERR: elemCreateArc180by3Pts: invalid dir format: ",dir )
		return {}
	if dir != 'cw' and dir != 'cc':
		print( "ERR: elemCreateArc180by3Pts: invalid dir command: ",dir )
		return {}
	# As "elemCreateArc180()" requires a radius to create an arc, we obtain it
	# from the from the length of any of the points-to-center vectors.
	# Depending on the situation, a wrong center might be calculated here, considering
	# that we also specify the direction of the arc.
	# Here are two situations (ommitted z-values):
	# A) p1=(2,1) to p2=(3,5) via pm=(4,3)  'cc' -> center=(1.83, 3.17), possible and okay
	# B) p1=(2,1) to p2=(3,5) via pm=(8,3)  'cc' -> center=(4.86, 2.41), impossible for this arc, but a valid center, now on the right
	# This "flipping" center, depending on whether stupid things are being asked for or not, will
	# result in a wrong arc, because we draw it from p1 to p2, but with the wrong radius, because the length of
	# center->p1, center->p2, center->pm refer to a wrong position (for this arc). As a result, only p1 and p2 will
	# be on the arc. pm is (obviously) somwhere else.
	# Solution: Check the correct location of the center point instead.
	# For a 'cc' arc, the center point should be to the left of the p1->p2 vector and on the right side for 'cw'.
	center = arcCenter180XY3P( p1, p2, pm )
	if center == None:
		print( "ERR: elemCreateArc180by3Pts: no 180° arc possible with ", p1, p2, pm )
		return {}
	else:
		# get 2D length (z=0) from mid to any point to obtain the radius
		rad = abs(vecLength( (center[0],center[1],0), (p1[0],p1[1],0) ))
		if rad < RADTOL:
			print( "ERR: elemCreateArc180by3Pts: radius almost zero: ", rad )
			return {}
		pos = vecHasPointLeftOrRight( p1, vecSub(p2,p1), center )
		if pos < 0 and dir == 'cc' or pos > 0 and dir == 'cw':
			return elemCreateArc180(p1,p2,rad,dir,extra)
		else:
			print( "ERR: elemCreateArc180by3Pts: point pm not on arc: ", pm )
			return {}



#############################################################################
### elemCreateArc180To
###
### Just calls elemCreateArc180 with an already known element position.
#############################################################################
def elemCreateArc180by3PtsTo(e1,p2,pm,dir,extra={}):

	if not 'type' in e1:
		print( "ERR: elemCreateArc180by3PtsTo: element 'e1' has no 'type'" )
		return {}

	if   e1['type'] == 'v':
		pt = e1['p1']
	elif e1['type'] == 'l' or e1['type'] == 'a':
		pt = e1['p2']
	else:
		print( "ERR: elemCreateArc180by3PtsTo: unknown 'type' in 'e1':", e1['type'] )
		return {}

	return elemCreateArc180by3Pts(pt,p2,pm,dir,extra)


#############################################################################
### elemGetPts
###
### Returns a list of the elements points.
#############################################################################
def elemGetPts(el):
	if   el['type'] == 'v':
		return [ el['p1'] ]
	elif el['type'] == 'l' or el['type'] == 'a':
		return [ el['p1'], el['p2'] ]

	print( "ERR: elemGetPts: unknown 'type' in 'el':", el['type'] )
	return []



#############################################################################
### elemCopy
###
### Returns a new instance of the given element
#############################################################################
def elemCopy(el):
	en={}
	for i in el:
		en[i]=el[i]
	return en



#############################################################################
### elemRotateZ
###
### Rotates an element around the z-axis at (0,0). Angle 'ang' in degrees.
### (or physically correct (0,0,1) :-)
### Returns a new instance.
#############################################################################
def elemRotateZ(elem, ang):
	# TODO: probably not necessary to copy the element here
	elemn={}
	ang = math.radians( ang )
	for i in elem:
		elemn[i]=elem[i]
	if   elemn['type'] == 'v':
		elemn['p1']=vecRotateZ(elemn['p1'],ang)
		return elemn
	elif elemn['type'] == 'l':
		elemn['p1']=vecRotateZ(elemn['p1'],ang)
		elemn['p2']=vecRotateZ(elemn['p2'],ang)
		return elemn
	elif elemn['type'] == 'a':
		elemn['p1']=vecRotateZ(elemn['p1'],ang)
		elemn['p2']=vecRotateZ(elemn['p2'],ang)
		return elemn



#############################################################################
### elemRotateZAt
###
### Rotates an element around the z-axis at a given center point.
### Angle 'ang' in degrees.
### Returns a new instance.
#############################################################################
def elemRotateZAt(elem, ang, center):
	# TODO: probably not necessary to copy the element here
	elemn={}
	for i in elem:
		elemn[i] = elem[i]
	vec = vecReverse( center )
	elemn = elemTranslate( elemn, vec )
	elemn = elemRotateZ( elemn, ang )
	elemn = elemTranslate( elemn, center )
	return elemn 



#############################################################################
### elemTranslate
###
### Moves an element into the directions specified by a vector (tuple)
### Returns a new instance.
#############################################################################
def elemTranslate(elem, vec):
	# TODO: probably not necessary to copy the element here
	elemn={}
	for i in elem:
		elemn[i]=elem[i]
	# every element has 'p1':
	p1=vecAdd(elemn['p1'],vec)
	elemn['p1']=p1

	if 'p2' in elem:
		p2=vecAdd(elemn['p2'],vec)
		elemn['p2']=p2

	return elemn



#############################################################################
### elemMoveTo
###
### Moves an element to a specific position. Reference is either 'p1' (default),
### 'p2' or the midpoint between 'p1' and 'p2'.
### Returns a new instance.
#############################################################################
def elemMoveTo(elem, pos, ref='p1'):
	# TODO: probably not necessary to copy the element here
	elemn={}
	for i in elem:
		elemn[i]=elem[i]
	if   elemn['type'] == 'v':
		elemn['p1'] = pos
		return elemn
	elif elemn['type'] == 'l' or elemn['type'] == 'a':
		if ref == 'p1':
			elemn['p1'] = pos
			elemn['p2'] = vecAdd( elemn['p1'], vecExtract(  elem['p1'], elem['p2']  )  )
		elif ref == 'p2':
			elemn['p2'] = pos
			elemn['p1'] = vecAdd( elemn['p2'], vecExtract(  elem['p2'], elem['p1']  )  )
		elif ref == 'p1p2':
			pm = vecExtractMid( elem['p1'], elem['p2'] ) 
			elemn['p1'] = vecAdd( pos, vecReverse( pm ) )
			elemn['p2'] = vecAdd( pos, pm )
		return elemn



#############################################################################
### elemReverse
###
### Reverses the direction of an element, swapping 'p1' and 'p2'
### Returns a new instance.
#############################################################################
def elemReverse(elem):
	elemn={}
	for i in elem:
		elemn[i]=elem[i]

	if elem['type']=='v':
		return elemn

	# future upgrades may require changes...
	p1=elemn['p1']
	p2=elemn['p2']

	if elem['type']=='l':
		elemn['p1']=p2
		elemn['p2']=p1

	if elem['type']=='a':
		elemn['p1']=p2
		elemn['p2']=p1
		if elemn['dir']=='cw':
			elemn['dir']='cc'
		else:
			elemn['dir']='cw'
	return elemn



#############################################################################
### elemIntersectsElemXY
###
### Returns a list of intersection points, sorted by distance from el1['p1'].
### z is ignored
### return value(s) is/are:
### [ [<dist>,(<x>,<y>,<z>)],[<dist>, ...] ]
#############################################################################
def elemIntersectsElemXY(e1,e2):
	hits=[]

	# line on line
	if e1['type']=='l' and e2['type']=='l':
		isp=vecIntersectXY(e1['p1'],e1['p2'],e2['p1'],e2['p2'])
		if isp == None:
			return []
		di=vecDistPointOnLineXY(e1['p1'],e1['p2'],isp)
		if di == None:
			return []
		if 0.0 <= di <= 1.0:
			di2=vecDistPointOnLineXY(e2['p1'],e2['p2'],isp)
			if di2 is not None:
				if 0.0 <= di2 <= 1.0:
					return [[di,isp]]
		return []

	# line on arc
	if e1['type']=='l' and e2['type']=='a':
		pm=arcCenter180XY(e2['p1'],e2['p2'],e2['rad'],e2['dir'])
		if pm == None:
			return []
		isp=vecArcIntersectXY(e1['p1'],e1['p2'],pm,e2['rad'])
#    print( "l on a hits: ",isp )
		if isp == None:
			return []
		for i in isp:
			if arcHasPointInSegmentXY(e2['p1'],e2['p2'],e2['rad'],e2['dir'],i):
				di=vecDistPointOnLineXY(e1['p1'],e1['p2'],i)
				if 0.0 <= di <= 1.0:
					hits.append([di,i])
		return hits

	# arc on line
	if e1['type']=='a' and e2['type']=='l':
		pm=arcCenter180XY(e1['p1'],e1['p2'],e1['rad'],e1['dir'])
		if pm == None:
			return []
		isp=vecArcIntersectXY(e2['p1'],e2['p2'],pm,e1['rad'])
#    print( "a on l hits: ",isp )
		if isp == None:
			return []
		for i in isp:
			if arcHasPointInSegmentXY(e1['p1'],e1['p2'],e1['rad'],e1['dir'],i):
					di=vecDistPointOnLineXY(e2['p1'],e2['p2'],i)
					if 0.0 <= di <= 1.0:
						di=arcDistPointOnBowXY(e1['p1'],e1['p2'],e1['rad'],e1['dir'],i)
						hits.append([di,i])
		return hits

	# arc on arc
	if e1['type']=='a' and e2['type']=='a':
		pm1=arcCenter180XY(e1['p1'],e1['p2'],e1['rad'],e1['dir'])
		if pm1 == None:
			return []
		pm2=arcCenter180XY(e2['p1'],e2['p2'],e2['rad'],e2['dir'])
		if pm2 == None:
			return []
		isp=arcIntersectXY(pm1,e1['rad'],pm2,e2['rad'])
#    print( "a on a hits: ",isp )
		if isp == None:
			return []
		for i in isp:
			if  arcHasPointInSegmentXY(e1['p1'],e1['p2'],e1['rad'],e1['dir'],i) \
			and arcHasPointInSegmentXY(e2['p1'],e2['p2'],e2['rad'],e2['dir'],i):
				di=arcDistPointOnBowXY(e1['p1'],e1['p2'],e1['rad'],e1['dir'],i)
				hits.append([di,i])
		return hits

	return []



#############################################################################
### elemNextAngle
###
### Returns the angle to the initial vector of the next element.
#############################################################################
def elemNextAngle(e1,e2):

	if e1['type'] == 'l':
		v1=(e1['p2'][0]-e1['p1'][0],e1['p2'][1]-e1['p1'][1],0)
		
	if e1['type'] == 'a':
		v1=arcVectorAtPx(e1['p1'],e1['p2'],e1['rad'],e1['dir'],'p2')

	if v1 == None:
		return None
	
	if e2['type'] == 'l':
		v2=(e2['p2'][0]-e2['p1'][0],e2['p2'][1]-e2['p1'][1],0)
		
	if e2['type'] == 'a':
		v2=arcVectorAtPx(e2['p1'],e2['p2'],e2['rad'],e2['dir'],'p1')

	if v2 == None:
		return None
	
	a=vecAngleDiffXY(v1,v2)

	return a



#############################################################################
### elemDebugPrint
###
#############################################################################
def elemDebugPrint(e1):
	prt=''

	if 'pNr' in e1:
		pNr = e1['pNr']
	else:
		pNr = -1

	if e1['type'] == 'l':
		print( "LINE   %4d: (%8.3f %8.3f %8.2f) (%8.3f %8.3f %8.3f)" % (pNr, \
			e1['p1'][0],e1['p1'][1],e1['p1'][2],e1['p2'][0],e1['p2'][1],e1['p2'][2]) )
		return

	if e1['type'] == 'a':
		print( "ARC    %4d: (%8.3f %8.3f %8.2f) (%8.3f %8.3f %8.3f) %8.3f %s" % (pNr, \
			e1['p1'][0],e1['p1'][1],e1['p1'][2],e1['p2'][0],e1['p2'][1],e1['p2'][2],e1['rad'],e1['dir']) )
		return

	if e1['type'] == 'v':
		print( "VERTEX %4d: (%8.3f %8.3f %8.2f)" % (pNr, \
			e1['p1'][0],e1['p1'][1],e1['p1'][2] ) )
		return

	print( "UEO    %4d of type %c " % (e1['pNr'],e1['type']) )




#############################################################################
### elemFindLinked
###
#############################################################################
def elemFindLinked(elem):
	pass
	



#############################################################################
### partCreate
###
#############################################################################
def partCreate( name="", elems = None, extras={} ):
	# if elems == None:
	# 	elems = []

	# TODO: check what to do if the part creation fails; return {} or an empty part??

	if not isinstance( elems, list ):
		print( "ERR: partCreate: elems is not a list; ignoring: ", type(elems) )
		elems = []
	
#	part = { 'name':name, 'type':'p', 'elements':elems }
	part = { 'name':name, 'type':'p', 'elements':[] }

	if elems is not None:
		partAddElements( part, elems )

	# TODO: Do we need these "extras" and why aren't the others labeled "extra"?
	for i in extras:
		part[i] = extras[i]

	return part



#############################################################################
### partDeleteNumbers
###
#############################################################################
def partDeleteNumbers(part):
	for i in range(0,len(part['elements'])):
		if 'pNr' in part['elements'][i]:
			del(part['elements'][i]['pNr'])
	return part



#############################################################################
### partGetFreeNumber
###
### Returns the next free number in a part or -1 if not a single number
### was found.
#############################################################################
def partGetFreeNumber( part ):
	nr = []
	for i in part['elements']:
		if 'pNr' in i:
			nr.append( i['pNr'] )
	if nr != []:
		nr.sort()
		return nr[ len(nr) - 1 ] + 1
	else:
		return 0



#############################################################################
### partAddElement
###
### Adds an element to a part
### number = 0 -> auto numbering
### number < 0 -> no numbering
#############################################################################
def partAddElement( part, elem, number=0 ):
	for i in part['elements']:
		if 'pNr' in i:
			if i['pNr'] == number:
				number = 0
				continue
	nelem = elem
	if number == 0:
		nelem['pNr'] = partGetFreeNumber( part )
	else:
		if number > 0:
			nelem['pNr'] = number
	part['elements'].append( nelem )
	return part



#############################################################################
### partAddElements
###
#############################################################################
def partAddElements(part, elems):
	if elems is None:
		print( "ERR: partAddElements: 'elems' is None" )
		return part

	if not isinstance( elems, list):
		print( "ERR: partAddElements: 'elems' is not a list" )
		return part

	for i in elems:
		# TODO: TOCHK: changed 8/2021, auto numbering for AddElements
		# part=partAddElement( part, i, -1 )
		part = partAddElement( part, i, 0 )
	return part



#############################################################################
### partGetElement
###
#############################################################################
def partGetElement(part, number):
	for i in range(0,len(part['elements'])):
		if 'pNr' in part['elements'][i]:
			if part['elements'][i]['pNr'] == number:
				return part['elements'][i]
	return {}



#############################################################################
### partCheckNumber
###
#############################################################################
def partCheckNumber(part, number):
	for i in range(0,len(part['elements'])):
		if 'pNr' in part['elements'][i]:
			if part['elements'][i]['pNr'] == number:
				return True
	return False


	
#############################################################################
### partCheckUniqueNumbers
###
#############################################################################
def partCheckUniqueNumbers( part ):
	nrFound = []
	for i in range( 0, len(part['elements']) ):
		if 'pNr' in part['elements'][i]:
			if part['elements'][i]['pNr'] in nrFound:
				print( "ERR: partCheckUniqueNumbers: already found nr: ",part['elements'][i]['pNr'] )
				return False
			else:
				nrFound.append(part['elements'][0]['pNr'])
		else:
			print( "ERR: partCheckUniqueNumbers: element without \'pNr\' tag found!" )
			return False
	return True



#############################################################################
### partGetNumbers
###
#############################################################################
def partGetNumbers(part):
	li = []
	for i in range( 0, len(part['elements']) ):
		li.append( part['elements'][i]['pNr'] )
	li.sort()
	return li



#############################################################################
### partGetLastPositionFromElements
###
#############################################################################
def partGetLastPositionFromElements(elems):
	nr = 0
	el = {}
	for i in elems:
		if 'pNr' in i:
			if i['pNr'] > nr:
				nr=i['pNr']
				el=i
	if len(el) == 0:
		return None
	if 'p2' in el:
		return el['p2']
	if 'p1' in el:
		return el['p1']  
	return None



#############################################################################
### partGetLastPosition
###
#############################################################################
def partGetLastPosition(part):
	li=partGetNumbers(part)
	if len(li) == 0:
		return None
	el=partGetElement(part,li[len(li)-1])
	if 'p2' in el:
		return el['p2']
	if 'p1' in el:
		return el['p1']  
	return None



#############################################################################
### partGetFirstPosition
###
#############################################################################
def partGetFirstPosition(part):
	li=partGetNumbers(part)
	if len(li) == 0:
		return None
	el=partGetElement(part,li[0])
	if 'p1' in el:
		return el['p1']
	return None



#############################################################################
### partRenumber
###
#############################################################################
def partRenumber( part ):
	if not partCheckUniqueNumbers( part ):
		return part
	li = []
	for i in range( 0, len(part['elements']) ):
		li.append( [part['elements'][i]['pNr'], i] )
	li.sort()
	for i in range( 0, len(li) ):
		part['elements'][li[i][1]]['pNr'] = i + 1
	return part



#############################################################################
### partSortByNumber
###
#############################################################################
def partSortByNumber( part ):
	if not partCheckUniqueNumbers( part ):
		return part
	li = []
	for i in range( 0, len(part['elements']) ):
		li.append( [part['elements'][i]['pNr'], i] )
	li.sort()
	oldelems = part['elements']
	part['elements'] = []
	for i in range( 0, len(li) ):
		part = partAddElement( part, oldelems[ li[i][1] ], li[i][0] )
	return part



#############################################################################
### partCheckContinuous
###
#############################################################################
def partCheckContinuous( part ):
	if not partCheckUniqueNumbers( part ):
		return False
	li = partGetNumbers( part )
	if len(li) == 0:
		print( "ERR: partCheckContinuous: no elements in part!" )
		return False
	if len(li) == 1:
		return True

	# Because of the new "feedrate vertices", we now will ignore them, rather
	# than throwing out an error message.
	# Needs to be tested thought ...

	# find the first element that is not a vertex
	for eStart in range( 0, len(li) ):
		e1 = partGetElement( part, li[eStart] )

		if e1['type']=='v':
			print( "INF: partCheckContinuous: vertex found!" )
		else:
			break

	eStart += 1

	# Er, yes. If it's only one element, for whatever reason, it for
	# sure can be seen as "continuous", lol.
	if eStart == len(li):
		print( "INF: partCheckContinuous: only one non-vertex element found" )
		return True

	# start with the element after the one we just found
	for i in range( eStart, len(li) ):

		e2 = partGetElement( part, li[i] )

		# let's hope it's not another vertex
		if e2['type'] == 'v':
			print( "INF: partCheckContinuous: vertex found!" )
			continue

		if not e1['p2'] == e2['p1']:
			ez = math.fabs( vecLength( e1['p2'], e2['p1'] ) )
			if ez > TOOL_CONTINUOUS_TOLERANCE:
				print( "ERR: partCheckContinuous: p2!=p1 at number: ", i )
				print( "                        : e1['p2']: ", e1['p2'] )
				print( "                        : e2['p1']: ", e2['p1'] )
				return False
		e1 = e2
	return True
		
	

#############################################################################
### partCheckClosed
###
#############################################################################
def partCheckClosed( part ):
	if not partCheckContinuous( part ): 
		return False
	li = partGetNumbers( part )

	if len(li) == 0:
		return False

	e1 = partGetElement( part, li[0] )

	# This hurts a bit, but yes - if it's only one vertex, then it can be considered as "closed", lol.
	if len(li) == 1:
		if e1['type'] == 'v':
			return True

	e2 = partGetElement( part, li[-1] )

	# let's update this for the new feedrate vertices
	if e2['type'] == 'v':
		if e2['p1'] == e1['p1']:
			return True

	if e2['p2'] == e1['p1']:
		return True

	return False



#############################################################################
### partTranslate
###
### Moves the part into the direction specified by a vector.
### Returns a new instance
#############################################################################
def partTranslate( part, vec ):
	partn = {}
	for i in part:
		# do not copy the elements; they are what wee need to translate in here
		if i == 'elements':
			partn['elements'] = []
		else:
			partn[i] = part[i]
	if not isinstance( part, dict ):
		print( "ERR: partTranslate: not a dict ", type(part) )
		return []
	if 'type' not in part:
		print( "ERR: partTranslate: no 'type' in part" )
		return []
	if part['type'] != 'p':
		print( "ERR: partTranslate: wrong 'type' in part:", part['type'] )
		return []
	if 'elements' not in part:
		print( "ERR: partTranslate: no 'elements' in part" )
		return []
	# could also pass the list to 'geomTranslate()', but ok ...
	for elem in part['elements']:
		partn['elements'].append(  elemTranslate( elem, vec)  )
	
	return partn



#############################################################################
### partRotateZ
###
### Rotates the part around the center of the z-axis, vec(0,0,1)
### Angle 'ang' in degrees.
### Returns a new instance
#############################################################################
def partRotateZ( part, ang ):
	partn = {}
	for i in part:
		# do not copy the elements; they are what wee need to translate in here
		if i == 'elements':
			partn['elements'] = []
		else:
			partn[i] = part[i]
	if not isinstance( part, dict ):
		print( "ERR: partRotateZ: not a dict ", type(part) )
		return []
	if 'type' not in part:
		print( "ERR: partRotateZ: no 'type' in part" )
		return []
	if part['type'] != 'p':
		print( "ERR: partRotateZ: wrong 'type' in part:", part['type'] )
		return []
	if 'elements' not in part:
		print( "ERR: partRotateZ: no 'elements' in part" )
		return []
	# could also pass the list to 'geomRotateZ()', but ok ...
	for elem in part['elements']:
		partn['elements'].append(  elemRotateZ( elem, ang)  )
	
	return partn



#############################################################################
### partRotateZAt
###
### Rotates the part around the z-axis specified by a 'center' point.
### Angle 'ang' in degrees.
### Returns a new instance
#############################################################################
def partRotateZAt( part, ang, center ):
	partn = {}
	for i in part:
		# do not copy the elements; they are what wee need to translate in here
		if i == 'elements':
			partn['elements'] = []
		else:
			partn[i] = part[i]
	if not isinstance( part, dict ):
		print( "ERR: partRotateZAt: not a dict ", type(part) )
		return []
	if 'type' not in part:
		print( "ERR: partRotateZAt: no 'type' in part" )
		return []
	if part['type'] != 'p':
		print( "ERR: partRotateZAt: wrong 'type' in part:", part['type'] )
		return []
	if 'elements' not in part:
		print( "ERR: partRotateZAt: no 'elements' in part" )
		return []
	# could also pass the list to 'geomRotateZ()', but ok ...
	for elem in part['elements']:
		partn['elements'].append(  elemRotateZAt( elem, ang, center )  )
	
	return partn



#############################################################################
### partPrintInfo
###
#############################################################################
def partPrintInfo( part ):

	#	part = { 'name':name, 'type':'p', 'elements':[] }

	if not isinstance( part, dict ):
		print( "ERR: partPrintInfo: not a part:", type(part) )
		return
	
	if not 'type' in part:
		print( "ERR: partPrintInfo: part misses 'type' key" )
		return
	
	if part['type'] != 'p':
		print( "ERR: partPrintInfo: not a part or wrong 'type': ", type( part['type'] ) )
		return

	if not 'elements' in part:
		print( "ERR: partPrintInfo: part misses 'elements' list" )
		return

	if not isinstance( part['elements'], list ):
		print( "ERR: partPrintInfo: part's 'elements' value is not a list: ", type( part['elements'] ) )
		return

	if not 'name' in part:
		print( "ERR: partPrintInfo: part misses 'name' key" )
		return

	if not isinstance( part['name'], str ):
		print( "ERR: partPrintInfo: part's 'name' value is not a string: ", type( part['name'] ) )
		return

	# should be safe to output some infos now :)
	if len( part['name'] ) == 0:
		strName = '<no name>'
	else:
		strName = part['name']
	print( "-----" )
	print( "  PART: " + strName + ' with ' + str( len( part['elements'] ) ) + ' elements' )
	for k,v in part:
		if k in ['name', 'type', 'elements']:
			continue
		print( "    " + str(k) + " = " + str(v))




#############################################################################
### geomCreateCircle
###
### Creates a full circle at 'center' with a diameter of 'dia' and a
### direction as specified by 'dir'. The start of the circle can be specified
### by 'startAngle' (float 0-360): 0=right (xmax), 90=up (ymax), 180=left(xmin),
### 270=down. Values > 360 or < -360 are "modulus'ed down", negative values
### are hopefully converted right :)
#############################################################################
def geomCreateCircle( center, startAngle, dia, dir ):
	geom = []

	if dia <= 0:
		print( "ERR: geomCreateCircle: invalid diameter: ", dia )
		return []
	
	if dir != 'cc' and dir != 'cw':
		print( "ERR: geomCreateCircle: invalid direction: ", dir )
		return []

	# check for special dir parameters
	while startAngle > 360:
		startAngle = startAngle % 360
	while startAngle < -360:
		startAngle = startAngle % -360
	if startAngle < 0:
		startAngle = 360 - startAngle

	# calculate this for circle center at (0,0)
	pts = vecArcIntersectXY( (0,0,0), vecRotateZ( (999999999.9,0,0), -math.radians(startAngle)), (0,0,0), dia/2.0 )

	if len( pts ) != 2:
		print( "ERR: geomCreateCircle: cannot calculate intersections" )
		return []

	# move the coords to mathch the center
	pts[0] = vecAdd( pts[0], center )
	pts[1] = vecAdd( pts[1], center )
	geom.append( elemCreateArc180( pts[0], pts[1], 0, dir) )
	geom.append( elemCreateArc180( pts[1], pts[0], 0, dir) )

	return geom



#############################################################################
### geomCreateBezier
### 
### Creates a three points 2.5D Bézier curve through p1, p2 and p3 with lines.
### Z is linearly interpolated from p1 to p3. The z value of p2 is ignored.
### The amount of lines can be specified by 'steps".
### With steps set to 1, a line is drawn.
#############################################################################
def geomCreateBezier( p1, p2, p3, steps, basNr=0 ):
	# uses code from
	# https://rosettacode.org/wiki/Bitmap/B%C3%A9zier_curves/Cubic#Python

	if steps < 1:
		print( "ERR: geomCreateBezier: 'steps' must be > 0: ", steps ) 
		return []
	
	geom = []

	x0 = p1[0]
	y0 = p1[1]
	x1 = p2[0]
	y1 = p2[1]
	x2 = p3[0]
	y2 = p3[1]

	zSteps = ( p3[2] - p1[2] ) / steps

	firstOne = True
	for i in range( steps + 1 ):
		t  = i / steps
		t1 = 1.0 - t
		a  = t1 ** 2
		b  = 2.0 * t * t1
		c  = t ** 2
 
		x = a * x0 + b * x1 + c * x2
		y = a * y0 + b * y1 + c * y2
		z = p1[2] + ( i * zSteps ) 

		if firstOne == True:
			firstOne = False
		else:
			geom.append( elemCreateLine( (xold,yold,zold), (x,y,z) ) )

		xold = x
		yold = y
		zold = z

	return geom



#############################################################################
### geomCreateBezier4P
### 
### Creates a four points 2.5D Bézier curve through p1..p4 with lines.
### Z is linearly interpolated from p1 to p4. The z value of p2 and p3 are ignored.
### The amount of lines can be specified by 'steps".
### With steps set to 1, a line is drawn.
#############################################################################
def geomCreateBezier4P( p1, p2, p3, p4, steps, basNr=0 ):
	# uses code from
	# https://rosettacode.org/wiki/Bitmap/B%C3%A9zier_curves/Cubic#Python

	if steps < 1:
		print( "ERR: geomCreateBezier4P: 'steps' must be > 0: ", steps ) 
		return []

	geom = []

	x0 = p1[0]
	y0 = p1[1]
	x1 = p2[0]
	y1 = p2[1]
	x2 = p3[0]
	y2 = p3[1]
	x3 = p4[0]
	y3 = p4[1]

	zSteps = ( p4[2] - p1[2] ) / steps

	firstOne = True
	for i in range( steps + 1 ):
		t = i / steps
		a = (1.0 - t) ** 3
		b = 3.0 * t * (1. - t) ** 2.0
		c = 3.0 * t ** 2.0 * (1.0 - t)
		d = t ** 3.0
 
		x = a * x0 + b * x1 + c * x2 + d * x3
		y = a * y0 + b * y1 + c * y2 + d * y3
		z = p1[2] + ( i * zSteps ) 

		if firstOne == True:
			firstOne = False
		else:
			geom.append( elemCreateLine( (xold,yold,zold), (x,y,z) ) )

		xold = x
		yold = y
		zold = z

	return geom



#############################################################################
### geomCreateHelix
### 
### p1's position is the axial center of the helix (xy-plane) (*NEW 8/2021*).
### Endpoint is p1's (x,y)-position with the z-pos of "depth".
### "depth" is positive for negative z-axis values (milling a hole usually
### is done by milling "down", not "up").
#############################################################################
def geomCreateHelix( p1, dia, depth, depthSteps, dir, basNr=0, finish='finish' ):
	hel = []
	if depth == 0.0:
		print( "ERR: geomCreateHelix: depth == 0" )
		return []
	if depthSteps < 1.0:
		print( "ERR: geomCreateHelix: steps < 0" )
		return []
	if dia <= 0.0:
		print( "ERR: geomCreateHelix: dia <= 0" )
		return []
	depthPerHalfRev = depth / (2 * depthSteps)
	x1 = p1[0] - dia/2.0
	x2 = p1[0] + dia/2.0
	p1 = ( x1, p1[1], p1[2] )
	p2 = ( x2, p1[1], p1[2] - depthPerHalfRev )
	if basNr == 0:
		nr = 1
	else:
		nr = basNr
	for i in range( 0, depthSteps ):
		el=elemCreateArc180( p1, p2, dia/2.0, dir, {'pNr':nr} )
		nr += 1
		hel.append( el )
		p1 = p2
		p2 = ( x1, p1[1], p1[2]-depthPerHalfRev )
		el = elemCreateArc180( p1, p2, dia/2.0, dir, {'pNr':nr} )
		nr += 1
		hel.append( el )
		p1 = p2
		if not i == depthSteps - 1:
			p2 = ( x2, p1[1], p1[2] - depthPerHalfRev )
		else:
			p2 = ( x2, p1[1], p1[2] )
	# end for all depthSteps

	if not len(hel) == 2 * depthSteps:
		print( "ERR: geomCreateHelix: skipped one or more arcs (helix)" )
		return[]

	if finish == 'finish':
		el = elemCreateArc180( p1, p2, dia/2.0, dir, {'pNr':nr} )
		nr += 1
		if el == []:
			print( "ERR: geomCreateHelix: skipped first finishing arc" )
			return []
		hel.append(el)

		el = elemCreateArc180( p2, p1, dia/2.0, dir, {'pNr':nr} )
		nr += 1
		if el == []:
			print( "ERR: geomCreateHelix: skipped second finishing arc" )
			return []
		hel.append(el)
	# end if 'finish'

	return hel



#############################################################################
### geomCreateRadial
### 
### Creates a radial line pattern between two circles, specified by p1, dia1,
### p2 and dia2. The beginning and end of the radial lines can be controlled
### with the start angle 'angleStart' (0-360°), the angle bweteen the lines
### 'angleInc' (°) and the number of lines 'angleSteps' (int). Additinal angular
### offsets can be set by 'angleOffset1/2' (0-360°).
### 'connect1' specifies the connection type of the lines on the first circle
### and 'connect2' the type of the 2nd circle. Supported are:
###   'none' or None  -> no connection, just radial lines; not for milling
###   'line'          -> a direct connection between two top or two bottom lines;
###                      mills in both Z directions
###   'arcflat'       -> an arc with no change in Z height between two top or
###                      two bottom lines; mills in both Z directions
###   'arc'           -> TODO TODO TODO
###   'back'          -> a cross connection from circle 2 "back" to the first;
###                      will scratch the surface; mills in both Z directions
###   'zup'           -> a Bezier curve from circle 2, with a lifted Z-axis;
###                      will not touch the surface; mills only in the direction
###                      towards the 2nd circle
### The operations 'line', 'arc' and 'arcflat' can be used in any combination,
### in any of the 'connect1/2' arguments. The two ops 'back' and 'zup' can
### not be combined at all. If one of the 'connect1/2' arguments has either
### a 'back' or a 'zup' op, then this will override all other arguments.
### Notice that a 'back' AND a 'zup' together will result in an error, as this
### combination does not make sense at all.
### The number of line segemnts for the Bezier interpolation is length-adapted
### automatically, via DEFLEN_BEZIER, MINLEN_BEZIER and MAXLEN_BEZIER.
### This can be overridden by 'bezierSteps'. Notice that this setting is then
### valid for all 'zup-lines'.
##############################################################################
def geomCreateRadial( p1, dia1, p2, dia2,
					angleStart, angleInc, angleSteps,
					connect1='line', connect2='line',
					angleOffset1 = 0, angleOffset2 = 0,
					bezierSteps = None,
					basNr=0 ):

	if angleSteps < 1:
		print( "ERR: geomCreateRadial: 'angleSteps' must be > 0: ", angleSteps )
		return []

	if dia1 == dia2:
		print( "ERR: geomCreateRadial: dia1 and dia2 must not be equal: ", dia1 )
		return []

	if p1 == p2 and dia1 == dia2:
		print( "ERR: geomCreateRadial: same coords and diameters for p1 and p2 not possible" )
		return []
	
	if angleInc == 0:
		print( "ERR: geomCreateRadial: 'angleInc' must not be 0" )
		return []

	if connect1 == 'back' or connect2 == 'back':
		if connect1 == 'zup' or connect2 == 'zup':
			print( "ERR: geomCreateRadial: 'back' AND 'zup' mode cannot be combined" )
			return []
		print( "INF: geomCreateRadial: mode mismatch, using 'back'" )
		connect1 = connect2 = 'back'

	if connect1 == 'zup' or connect2 == 'zup':
		print( "INF: geomCreateRadial: mode mismatch, using 'zup'" )
		connect1 = connect2 = 'zup'

	while angleStart > 360:
		angleStart = angleStart % 360
	while angleStart < -360:
		angleStart = angleStart % -360
	if angleStart < 0:
		angleStart = 360 - angleStart

	while angleInc > 360:
		angleInc = angleInc % 360
	while angleInc < -360:
		angleInc = angleInc % -360
	if angleInc < 0:
		angleInc = 360 - angleInc

	lines = []

	# rotated vectors to easily calculate the point coordinates
	vec1 = ( dia1 / 2.0, 0, 0 )
	vec2 = ( dia2 / 2.0, 0, 0 )
	vec1 = vecRotateZ( vec1, math.radians(angleStart + angleOffset1) )
	vec2 = vecRotateZ( vec2, math.radians(angleStart + angleOffset2) )

	for n in range( angleSteps ):
		v1 = vecRotateZ( vec1, math.radians( n * angleInc) )
		v2 = vecRotateZ( vec2, math.radians( n * angleInc) )
		np1 = vecAdd( v1, p1 )
		np2 = vecAdd( v2, p2 )

		e = elemCreateLine( np1, np2 )

		# reverse every 2nd line for correct directions
		if n%2:
			e = elemReverse( e )

		lines.append( e )

	# okay; lines are done, now on to the connections
	numLines = len(lines)

	if numLines < 2:
		return lines

	geom = []
	n = 0
	lastLine = None

	for line in lines:

		if n > 0:
			# these are the lines ending at the 2nd point ("towards")
			if n % 2:
				# -----
				if connect2 is None or connect2 == 'none':
					pass
				# -----
				elif connect2 == 'line':
					geom.append( elemCreateLineBetween( lastLine, line ) )
				# -----
				elif connect2 == 'back':
					line = elemReverse( line )
					geom.append( elemCreateLineBetween( lastLine, line ) )
				# -----
				elif connect2 == 'zup':
					line = elemReverse( line )

					np1 = elemGetPts( lastLine )[1]
					np3 = elemGetPts( line )[0]
					if np3[2] > np1[2]:
						# if we "mill down", move up here then mode to target
						np2 = ( np1[0], np1[1], np3[2] )
					else:
						# if we "mill up", first move to the xy target, then down
						np2 = ( np3[0], np3[1], np1[2] )

					if bezierSteps is None:
						bezSteps = int( vecLength( np1, np3 ) / DEFLEN_BEZIER )
						if bezSteps < 5:
							bezSteps = int( vecLength( np1, np3 ) / MINLEN_BEZIER )
					else:
						bezSteps = bezierSteps
					if bezSteps < 2:
						bezSteps = 2

					geom += geomCreateBezier( np1, np2, np3, bezSteps )
				# -----
				elif connect2 == 'arcflat':
					[np11,np12] = elemGetPts( lastLine )
					[np21,np22] = elemGetPts( line )

					if angleInc < 0:
						dir = 'cw'
					else:
						dir = 'cc'

					revDir = False
					if dia2 > dia1:
						# target dia > start dia
						if p2[2] <= p1[2]:
							# bigger dia at bottom; swap!
							revDir = True
					else:
						# target dia < start dia
						if p2[2] >= p1[2]:
							# bigger dia at top; swap!
							revDir = True
					if revDir:
						if dir == 'cw':
							dir = 'cc'
						else:
							dir = 'cw'

					geom.append( elemCreateArc180( np12, np21, 0, dir) )
				# -----
				else:
					pass

			# These are the lines ending at the 1nd point ("backwards"),
			else:
				# -----
				if connect1 is None or connect1 == 'none':
					pass
				# -----
				elif connect1 == 'line':
					geom.append( elemCreateLineBetween( lastLine, line ) )
				# -----
				elif connect1 == 'back':
					geom.append( elemCreateLineBetween( lastLine, line ) )
				# -----
				elif connect1 == 'zup':
					np1 = elemGetPts( lastLine )[1]
					np3 = elemGetPts( line )[0]
					if np3[2] > np1[2]:
						# if we "mill down", move up here then mode to target
						np2 = ( np1[0], np1[1], np3[2] )
					else:
						# if we "mill up", first move to the xy target, then down
						np2 = ( np3[0], np3[1], np1[2] )

					if bezierSteps is None:
						bezSteps = int( vecLength( np1, np3 ) / DEFLEN_BEZIER )
						if bezSteps < 5:
							bezSteps = int( vecLength( np1, np3 ) / MINLEN_BEZIER )
					else:
						bezSteps = bezierSteps
					if bezSteps < 2:
						bezSteps = 2

					geom += geomCreateBezier( np1, np2, np3, bezSteps )
				# -----
				elif connect2 == 'arcflat':
					[np11,np12] = elemGetPts( lastLine )
					[np21,np22] = elemGetPts( line )

					if angleInc < 0:
						dir = 'cw'
					else:
						dir = 'cc'

					revDir = False
					if dia2 > dia1:
						# target dia > start dia
						if p2[2] <= p1[2]:
							# bigger dia at bottom; swap!
							revDir = True
					else:
						# target dia < start dia
						if p2[2] >= p1[2]:
							# bigger dia at top; swap!
							revDir = True
					if revDir:
						if dir == 'cw':
							dir = 'cc'
						else:
							dir = 'cw'

					geom.append( elemCreateArc180( np12, np21, 0, dir) )

				# -----
				else:
					pass

		geom.append( line )
		lastLine = line
		n += 1


	return geom




#############################################################################
### geomCreateRect
###
### Creates a rectangle between points 'p1' and 'p2' with the direction 'dir'
### and a linear z-change of 'depth'.
### If 'depth' is zero, a "flat" rectangle is created.
### The algorithm always starts at 'p1'; the z-component of 'p2' is ignored.
### If 'p1' and 'p2' share either the same x or y value, then the algorithm
### will always return to 'p1'.
#############################################################################
def geomCreateRect( p1, p2, depth, dir, basNr=0 ):

	if dir != 'cc' and dir != 'cw':
		print( "ERR: geomCreateRect: invalid direction: ", dir )
		return []
	
	if p1[0] == p2[0] and p1[1] == p2[1]:
		print( "ERR: geomCreateRect: p1 and p2 have identical x and y values: ", p1, p2 )
		return []

	geom = []

	# create a list of point coordinates
	p2 = ( p2[0], p2[1], p1[2] )
	xvec = ( p2[0] - p1[0], 0, 0 )
	# moved to the bottom
	pts = [ p1, vecAdd(p1,xvec), p2, vecSub(p2,xvec), p1 ]

	# modify the depths of the points in the list we just created
	yvec = ( p2[1] - p1[1], 0, 0 )
	xlen = vecLength( xvec )
	ylen = vecLength( yvec )
	# should not be zero; already checked if p1 equals p2 above
	nomDepth = depth / ( 2 * xlen + 2 * ylen )
	zvecX = nomDepth * xlen
	zvecY = nomDepth * ylen
	depths = [ p1[2], p1[2] - zvecX, p1[2] - zvecX - zvecY, p1[2] - 2*zvecX - zvecY, p1[2]-depth ]

	# create a list with the points including the correct z-depth
	lstPts = []
	n = 0
	for pt in pts:
		lstPts.append(  (pt[0], pt[1], depths[n] )  )
		n += 1

	if dir == 'cw':
		lstPts.reverse()

	lastPt = p1
	for pt in lstPts[1:]:
		# only create a line if there's really a difference between the points
		if pt != lastPt:
			geom.append( elemCreateLine( lastPt, pt ) )
		lastPt = pt

	return geom



#############################################################################
### geomCreateConcentricRects
###
### TODO: Ugh. Seriously?
#############################################################################
def geomCreateConcentricRects( p1, p2, xdiff, ydiff, stepOver, dir, basNr=0 ):

	if xdiff < 0 and ydiff > 0 or xdiff > 0 and ydiff < 0:
		print( "ERR: geomCreateConcentricRects: xdiff and ydiff must have same sign: ", xdiff, ydiff )
		return []

	if xdiff == 0 and ydiff == 0:
		print( "INF: geomCreateConcentricRects: xdiff and ydiff zero; auto stop on middle" )
		xdiff = (p2[0] - p1[0]) / 2.0
		ydiff = (p2[1] - p1[1]) / 2.0

	if xdiff == 0 or ydiff == 0:
		print( "ERR: geomCreateConcentricRects: either xdiff or ydiff is zero: ", xdiff, ydiff )
		return []

	if stepOver == 0:
		print( "INF: geomCreateConcentricRects: stepOver is zero; creating a simple rect ")
		return geomCreateRect( p1, p2, 0, dir )

	if stepOver < 0:
		# Shh, it must not, but this makes things easier below :)
		print( "INF: geomCreateConcentricRects: stepOver must be > 0: ", stepOver )
		return []

	geom = []

	# make stepOver match the direction
	if xdiff < 0:
		stepOver *= -1

	depth = p1[2]
	p11 = p1
	p22 = p2
	xDone = yDone = False
	p1old = p2old = None
	while True:

		if p1old is not None:

			# TODO -> Z-height
			# TODO -> amount of Bezier points 

			if dir == 'cw':
				pmx = p11[0]
				pmy = p1old[1]
			else:
				pmx = p1old[0]
				pmy = p11[1]
			pmz = 0
			pmid = ( pmx, pmy, pmz )
			ebez = geomCreateBezier( p1old, pmid, p11, 10 )
			geom += ebez


		e = geomCreateRect( p11, p22, depth, dir )

		if e == []:
			print( "ERR: geomCreateConcentricRects: unable to create rect: ", p11, p22, dir )
			return []

		# geoms need to be _added_ to geoms, not appended
		geom += e

		if xDone == True and yDone == True:
			break

		# next point set
		if stepOver > 0 and p11[0] + stepOver >= p1[0] + xdiff   or   stepOver < 0 and p11[0] + stepOver <= p1[0] + xdiff:
			xnew = p1[0] + xdiff - p11[0]
			xDone = True
		else:
			xnew = stepOver

		if stepOver > 0 and p11[1] + stepOver >= p1[1] + ydiff   or   stepOver < 0 and p11[1] + stepOver <= p1[1] + ydiff:
			ynew = p1[1] + ydiff - p11[1]
			yDone = True
		else:
			ynew = stepOver

		p1old = p11
		p2old = p22

		p11 = ( p11[0] + xnew, p11[1] + ynew, p11[2] )
		p22 = ( p22[0] - xnew, p22[1] - ynew, p22[2] )

	return geom






#############################################################################
### geomCreateRectHelix
###
### Creates a rectangular helix between points 'p1' and 'p2', the direction
### 'dir' and a linear z-change of 'depth' per turn. 'depthSteps' specifies
### the amount of turns.
### The algorithm always starts at 'p1'; the z-component of 'p2' is ignored.
### If 'p1' and 'p2' share either the same x or y value, then the algorithm
### will always return to 'p1'. If 'finish'
### Useful for finishing and smoothening things.
#############################################################################
def geomCreateRectHelix( p1, p2, depth, depthSteps, dir, clearBottom=True, basNr=0 ):
	if depth == 0:
		print( "ERR: geomCreateRectHelix: depth is zero" )
		return []
	if depthSteps < 1:
		print( "ERR: geomCreateRectHelix: depthSteps < 1:", depthSteps )
		return []
	
	geom = []

	for i in range( depthSteps ):
		e = geomCreateRect( p1, p2, depth, dir )
		if e == []:
			print( "ERR: geomCreateRectHelix: error creating rect at step i ", i )
			return []

		# geoms need to be added to geoms, not appended
		geom += e

		# new z start position
		p1 = ( p1[0], p1[1], p1[2] - depth )

	if clearBottom:
		e = geomCreateRect( p1, p2, 0, dir )
		if e == []:
			print( "ERR: geomCreateRectHelix: error creating bottom rect" )
			return []
		geom += e

	return geom



#############################################################################
### geomCreateRectSpiral
###
### TODO: Does this make sense at all?
#############################################################################
def geomCreateRectSpiral( p1, p2, stepOver, steps, dir, basNr=0 ):
	if stepOver == 0:
		print( "ERR: geomCreateRectSpiral: stepOver is zero" )
		return []
	if steps < 1:
		print( "ERR: geomCreateRectSpiral: steps < 1:", steps )
		return []
	
	geom = []

	return geom



#############################################################################
### geomCreateConcentricCircles
###
### p1 is the center position of the circles.
### If diaStart < diaEnd, the circular pocket is "milled" from the inside
### to the outside and vice versa.
### "diaSteps" determines the amount of steps (aka.: circles) which should
### be performed.
### If diaSep==1, a single circle, determined by "diaStart"'s diamenter is
### "milled".
#############################################################################
def geomCreateConcentricCircles( p1, diaStart, diaEnd, diaSteps, dir, basNr=0 ):
	con = []
	if diaStart <= 0.0:
		print( "ERR: geomCreateConcentricCircles: diaStart <= 0" )
		return []
	if diaEnd <= 0.0:
		print( "ERR: geomCreateConcentricCircles: diaStart <= 0" )
		return []
	if diaSteps < 1:
		print( "ERR: geomCreateConcentricCircles: diaSteps < 1" )
		return []
	diaPerRev=(diaEnd-diaStart)/diaSteps

	# NEW 9/2021: quickfix to make p1 the center (was left of circle before)
	p1 = ( p1[0] - diaStart/2.0, p1[1], p1[2])

	y=p1[1]
	z=p1[2]
	if basNr==0:
		nr=1
	else:
		nr=basNr
	# TOCHK (2021)
	for i in range(0,int(diaSteps)):
		x1=p1[0]-(i*diaPerRev/2.0)
		x2=p1[0]+(i*diaPerRev/2.0)+diaStart
		diaAct=diaStart+(i*diaPerRev)
		el=elemCreateArc180((x1,y,z),(x2,y,z),math.fabs(diaAct/2.0),dir,{'pNr':nr})
		nr+=1
		con.append(el)
		el=elemCreateArc180((x2,y,z),(x1,y,z),math.fabs(diaAct/2.0),dir,{'pNr':nr})
		nr+=1
		con.append(el)
		if i < diaSteps-1:
			x1=p1[0]-(i*diaPerRev/2.0)
			x2=p1[0]-(i*diaPerRev/2.0)-diaPerRev/4.0
			if diaPerRev > 0:
				if dir == 'cw':
					tdir='cc'
				else:
					tdir='cw'
			else:
				tdir=dir
			el=elemCreateArc180((x1,y,z),(x2,y,z),math.fabs(diaPerRev)/8.0,tdir,{'pNr':nr})
			nr+=1
			con.append(el)
			if diaPerRev < 0:
				if dir == 'cw':
					tdir='cc'
				else:
					tdir='cw'
			else:
				tdir=dir
			x1=p1[0]-(i*diaPerRev/2.0)-diaPerRev/4.0
			x2=p1[0]-(i*diaPerRev/2.0)-diaPerRev/2.0
			el=elemCreateArc180((x1,y,z),(x2,y,z),math.fabs(diaPerRev)/8.0,tdir,{'pNr':nr})
			nr+=1
			con.append(el)
	if not len(con)==(diaSteps*4)-2:
		print( "ERR: geomCreateConcentricCircles: number of circles: needed vs. made. ",nr-1,len(con) )
		return []
	return con



#############################################################################
### geomCreateConcentricSlots
###
### Creates a slot hole.
#############################################################################
def geomCreateConcentricSlots( p1, p2, diaStart, diaEnd, diaSteps, dir, basNr=0 ):
	con = []
	if diaStart <= 0.0:
		print( "ERR: geomCreateConcentricSlots: diaStart <= 0" )
		return []
	if diaEnd <= 0.0:
		print( "ERR: geomCreateConcentricSlots: diaStart <= 0" )
		return []
	if diaSteps < 1:
		print( "ERR: geomCreateConcentricSlots: diaSteps < 1" )
		return []
	diaPerRev=(diaEnd-diaStart)/diaSteps

	# This was derived from ConcentricCircles.
	# To reduce the amount of calculations (lol), the slot hole is always created
	# along the y-axis and rotated afterwards, to match p2.

	# length is actually the "y-difference" now
	lenp1p2 = vecLengthXY( p1, p2 )
	if dir == 'cw':
		lenp1p2 = -lenp1p2
	np2 = vecAdd( p1, (0, lenp1p2, 0) )

	# WARNING: this is the "work vector", along the y-axis!
	vecp1p2 = vecSub( np2, p1 )

	# NEW 9/2021: quickfix to make p1 the center (was left of circle before)
	np1 = ( p1[0] - diaStart/2.0, p1[1], p1[2] )

	y = np1[1]
	z = np1[2]
	if basNr == 0:
		nr = 1
	else:
		nr = basNr
	# TOCHK (2021)
	for i in range( 0, int(diaSteps) ):
		x1 = np1[0] - ( i * diaPerRev/2.0 )
		x2 = np1[0] + ( i * diaPerRev/2.0 ) + diaStart
		diaAct = diaStart + ( i * diaPerRev )
		# arc at start point
		el = elemCreateArc180( (x1,y,z), (x2,y,z), math.fabs( diaAct/2.0 ), dir, {'pNr':nr} )
		nr += 1
		con.append(el)
		# line to dest
		el = elemCreateLineTo( el, (x2,y+lenp1p2,z))
		con.append(el)
		nr += 1
		# arc at dest point
		el = elemCreateArc180( (x2,y,z), (x1,y,z), math.fabs( diaAct/2.0 ), dir, {'pNr':nr} )
		el = elemTranslate( el, vecp1p2 )
		nr += 1
		con.append(el)

		x1 = np1[0] - ( i * diaPerRev/2.0 )
		x2 = np1[0] - ( i * diaPerRev/2.0 ) - diaPerRev/4.0

		# line to start
		el = elemCreateLineTo( el, (x1,y,z))
		con.append(el)
		nr += 1

		if i < diaSteps-1:

			if diaPerRev > 0:
				if dir == 'cw':
					tdir='cc'
				else:
					tdir='cw'
			else:
				tdir = dir
			el = elemCreateArc180( (x1,y,z), (x2,y,z), math.fabs( diaPerRev ) / 8.0, tdir, {'pNr':nr} )
			nr += 1
			con.append(el)
			if diaPerRev < 0:
				if dir == 'cw':
					tdir='cc'
				else:
					tdir='cw'
			else:
				tdir=dir
			x1 = np1[0] - ( i * diaPerRev/2.0 ) - diaPerRev/4.0
			x2 = np1[0] - ( i * diaPerRev/2.0 ) - diaPerRev/2.0
			el = elemCreateArc180( (x1,y,z), (x2,y,z), math.fabs( diaPerRev ) / 8.0, tdir, {'pNr':nr} )
			nr += 1
			con.append(el)

	# TODO: This check was from the original ConcentricCircles function
	# if not len(con) == ( diaSteps * 4 ) - 2:
	# 	print( "ERR: geomCreateConcentricSlots: number of circles: needed vs. made. ", nr-1, len(con) )
	# 	return []

	# rotate around p1 to original position
	if dir == 'cc':
		vDir = vecSub( p2, p1 )
	else:
		vDir = vecSub( p1, p2 )
	ang = math.radians( 90 ) - vecAngleXY( vDir )
	con = geomRotateZAt( con, math.degrees(ang), p1 )

	return con



#############################################################################
### geomCreateSpiralToCircle
###
### For finishing in- or outsides. Gently approaches a circle from the
### in- or outside in a spiral motion, then goes around 360° and retracts
### The circle is specified by 'center' and 'dia'.
### Due to programming laziness, the spiral movement is restricted to a number
### of full 360° turns and the starting point always on the x-axis.
### The "retract" movement is always only one turn, ending at where the entry
### spiral began.
### If 'spiralDist' is negative, the spiral will approach the circle from the
### inside; if positive, from the outside. The value itself determines the
### (x-) distance to the finished circle.
#############################################################################
def geomCreateSpiralToCircle( center, dia, spiralDist, spiralTurns, dir, basNr=0 ):
	geom = []

	if spiralDist == 0:
		print( "ERR: geomCreateSpiralToCircle: spiralDist is zero" )
		return []
	# NEW 8/2021: make "spiralDist" an absolute value
#	startPt = ( -dia/2.0 - spiralDist*spiralTurns, 0, 0 )
	startPt = ( -dia/2.0 - spiralDist, 0, 0 )
	spiralDist *= -1

	# NEW 8/2021: make "spiralDist" an absolute value
#	geom += geomCreateSpiralHelix( center, startPt, spiralDist, 0, spiralTurns, dir )
	geom += geomCreateSpiralHelix( center, startPt, spiralDist/spiralTurns, 0, spiralTurns, dir )
	geom += geomCreateCircle( center, -180, dia, dir )

	return geom



#############################################################################
### geomCreateCircRingHole
###
### p1 defines the start position (middle) of the pocket. It's z-axis
### value is the start of the _milling_ operation (mill hits material).
### The helix is on top of this point!
#############################################################################
def geomCreateCircRingHole( p1, diaStart, diaEnd, diaSteps, depth, depthSteps, hDepth, hDepthSteps, clear, dir, basNr=0 ):
	if depth <= 0.0:
		print( "ERR: geomCreateCircRingHole: negative or zero depth:",depth )
		return []
	if depthSteps < 1:
		print( "ERR: geomCreateCircRingHole: depthSt < 1: ",depthSteps )
		return []
	if hDepth < 0:
		print( "ERR: geomCreateCircRingHole: helix depth needs to be a positive number:",hDepth )
		return []
	if hDepth < depth / depthSteps:
		print( "ERR: geomCreateCircRingHole: helix is too short; needs to be greater than depth/depthSteps : ", hDepth )
		return []
	if hDepthSteps < 1:
		print( "ERR: geomCreateCircRingHole: hDepthSteps < 1 : ",hDepthSteps )
		return []
	if clear < p1[2]:
		print( "ERR: geomCreateCircRingHole: clear < workpos: ",clear,p1[2] )
		return []
	if diaStart <= 0:
		print( "ERR: geomCreateCircRingHole: diaStart < 0: ",diaStart )
		return []
	if diaEnd <= 0:
		print( "ERR: geomCreateCircRingHole: diaStart < 0: ",diaEnd )
		return []
	
	if basNr==0:
		nr=1
	else:
		nr=basNr

	ccrh=[]
	
	for i in range(0,depthSteps):
		# starting point for helix
		# NEW 8/2021 geomCreateHelix now uses p1 as the center point!
#		pWork = (  p1[0] - (diaStart/2.0), p1[1], p1[2] + hDepth - ((i+1) * (depth/(depthSteps*1.0) ))  )
		pWork = (  p1[0], p1[1], p1[2] + hDepth - ( (i+1) * (depth/(depthSteps*1.0) ))  )
		hel = geomCreateHelix( pWork, diaStart, hDepth, hDepthSteps, dir, nr, 'nofinish' )
		if hel == []:
			print( "ERR: geomCreateCircRingHole: error creating helix" )
			return []
		# we are now on pWork(x,y) but already cut depth/depthSteps of the material
		for j in hel:
			ccrh.append(j)
		nr += len(hel)

		# NEW 9/2021 geomCrateConcentricCircles was changed to now work with
		# p1 as the center point.
#		pWork=(p1[0]-(diaStart/2.0),p1[1],p1[2]-((i+1)*(depth/(depthSteps*1.0))))
		pWork = ( p1[0], p1[1], p1[2] - ( (i+1)*(depth/(depthSteps*1.0))) )
		poc = geomCreateConcentricCircles( pWork, diaStart, diaEnd, diaSteps, dir, nr )
		if poc == []:
			print( "ERR: geomCreateCircRingHole: error creating concentric circles" )
			return []
		# we are now on pWork(x,y), with i*(depth/depthSteps) in reverse z-axis direction
		for j in poc:
			ccrh.append(j)
		nr+=len(poc)
		
		if i < depthSteps-1:
			# now, "back" to the "next" helix
			pWork1 = partGetLastPositionFromElements(poc)
			pWork0 = pWork1
			# NEW 8/2021: avoid moving directly up (might "scratch" the surface),
			# instead, move to the middle of the x-axis' entry and exit position
#			pWork2=(pWork1[0],pWork1[1],pWork1[2]+depth/(depthSteps*1.0))
			# This is okay, but looks super stupid, lol. Should be fixed later.
			pWork2 = ( (p1[0]-(diaStart/2.0)+pWork1[0])/2, pWork1[1], pWork1[2] + depth/(depthSteps*1.0) )
			# NEW 8/2021 B: now get rid of these two lines and add a cool 180° arc (see below)
			# lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
			# nr+=1
			# if lin==[]:
			# 	print( "ERR: geomCreateCircRingHole: error creating helix back line 1 in: ",i )
			# 	return []
			# ccrh.append(lin)
			pWork1 = pWork2
			pWork2 = (p1[0]-(diaStart/2.0),p1[1],p1[2]+hDepth-((i+2)*(depth/(depthSteps*1.0))))
			# lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
			# nr+=1
			# if lin==[]:
			# 	print( "ERR: geomCreateCircRingHole: error creating helix back line 2 in: ",i )
			# 	return []
			# ccrh.append(lin)

			# NEW 8/2021: now with double arc
			arc = elemCreateArc180( pWork0, pWork1, 0, dir, {'pNr':nr} )
			nr += 1
			ccrh.append(arc)
			odir = 'cc' if dir == 'cw' else 'cw'
			arc = elemCreateArc180( pWork1, pWork2, 0, odir, {'pNr':nr} )
			nr += 1
			ccrh.append(arc)

		else:
			# now, "back" to the starting point
			pWork1 = partGetLastPositionFromElements(poc)
			pWork0 = pWork1
			# NEW 8/2021: avoid moving directly up (might "scratch" the surface),
			# instead, move to the middle of the x-axis' entry and exit position
#			pWork2=(pWork1[0],pWork1[1],pWork1[2]+(i+1)*(depth/(depthSteps*1.0)))
			pWork2=(  (pWork1[0]+(p1[0]-(diaStart/2.0)))/2, pWork1[1], pWork1[2] + (i+1) * (depth/(depthSteps*1.0))  )
			# NEW 8/2021 B: arcs now also here
			# lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
			# nr+=1
			# if lin==[]:
			# 	print( "ERR: geomCreateCircRingHole: error creating back line 1" )
			# 	return []
			# ccrh.append(lin)
			pWork1 = pWork2
			pWork2 = (p1[0]-(diaStart/2.0),p1[1],p1[2]+hDepth-((depth/(depthSteps*1.0))))
			# lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
			# nr+=1
			# if lin==[]:
			# 	print( "ERR: geomCreateCircRingHole: error creating back line 2" )
			# 	return []
			# ccrh.append(lin)

			# NEW 8/2021: now with arc
			arc = elemCreateArc180( pWork0, pWork2, 0, dir, {'pNr':nr} )
			nr += 1
			ccrh.append(arc)

	return ccrh



#############################################################################
### geomCreateSpiralHelix
###
### Creates a spiral or a helix or both, depending on the radial or height
### increments. The geometry is interpolated with lines.
### Parameters include the 'center' point, a starting point
### 'startPt', an incremental radius parameter 'radInc', a height parameter
### 'heightInc', the number of 'turns' and a direction parameter 'dir',
### either clockwise 'cw' or counterclockwise 'cc'.
### If the direction of the spiral is set inwards, with a negative 'radInc'
### parameter, the spiral is aborted, so that the shape does not form
### a double cone. If that's required, set 'stopAtZero' to False.
### The parameter 'maxGrad' defines the maximum angle of one line segment.
### Smaller values result in finer resolutions; with larger values, eg 120°
### or 90°, it's possible to shape "low poly" geometries.
### By default, 'startPt' is relative to the center. this can be changed by
### setting 'startPtIsAbs' to 'True'.
#############################################################################
def geomCreateSpiralHelix(center,startPt,radInc,heightInc,turns,dir,stopAtZero=True,maxGrad=5.0,startPtIsAbs=False,basNr=0):

	if dir != 'cc' and dir != 'cw':
		print( "ERR: geomCreateSpiral: invalid 'dir' parameter: ", dir )
		return []

	# TODO: Check what happens if we have z!=0 or even different ones in center ans startPt!
	# normalize to center as we create everything around (0,0,n)
	if startPtIsAbs and center != (0,0,0):
		startPt = vecSub( startPt, center )

	geom = []

	stepsPerTurn = 360 / maxGrad
	stepRad      = 2*math.pi / stepsPerTurn

	if dir == 'cc':
		stepRad *= -1

	vec    = startPt
	vecLen = vecLength( vec )
	e   = elemCreateVertex( startPt )
	
	# only for the "stop at zero" check
	lenMin = 99999999999.9

	for i in range( 1, 1 + int( turns * stepsPerTurn) ):
		v = vecRotateZ( vec, i * stepRad )

		radAdd = i * (radInc / stepsPerTurn)
		v = vecSetLength( v, vecLen + radAdd )

		if radInc < 0 and stopAtZero == True:
			vl = vecLength( v )
			if vl < lenMin:
				lenMin = vl
			else:
				# if vl suddenly starts growing again, we need to stop here
				# TODO: Shall we make the last step to (0,0,0)?
				break

		v = ( v[0], v[1], v[2] + i * (heightInc / stepsPerTurn ) )
		e   = elemCreateLineTo( e, v )
		geom.append( e )


	if center != (0,0,0):
		geom = geomTranslate( geom, center )

	return geom



#############################################################################
### geomCreateZigZag
###
### Creates a "zig zag", flat milling shape, defined by two points, a step
### parameter and a selection which axis shall move first.
### The amount of steps is calculated from the distance to travel, divided by
### the increment per step 'incStep', rounded up!
### For stupid values, a positive 'incStep' value but "more negative" end
### point coordinates, at least the first move is always executed. A linear
### move or a slot (if milled).
### Height (z) is takes from StartPt.
#############################################################################
def geomCreateZigZag( startPt, endPt, incStep, yFirst, basNr=0 ):
	geom = []

	if incStep == 0:
		print( "INF: geomCreateZigZag: 'incStep' must not be zero" )
		return []

	if incStep < 0:
		print( "INF: geomCreateZigZag: negative 'incStep' value" )
		incStep *= -1

	# use z from startPt
	z = startPt[2]

	# a marker for the direction of movement
	movX = endPt[0] - startPt[0]
	movY = endPt[1] - startPt[1]

	# a sign marker
	sigX = 1 if movX > 1 else -1
	sigY = 1 if movY > 1 else -1

	# always execute the first move
	if yFirst == 0:
		# x is going to move first
		e = elemCreateLine( startPt, ( endPt[0], startPt[1], z) )
		if incStep == 0:
			return [e]
		steps = movY / incStep
	else:
		# y is going to move first
		e = elemCreateLine( startPt, ( startPt[0], endPt[1], z) )
		if incStep == 0:
			return [e]
		steps = movX / incStep

	geom.append( e )

	steps = abs( math.ceil( steps ) )

	# splitting this in x and y is redundant, but easier to follow
	for n in range( steps ):

		# for x moves and step over y
		if yFirst == 0:
			yn = startPt[1] + (n+1) * incStep * sigY
			if n % 2 == 0:
				# 0, 2, 4, ...: move x back
				if movY > 0:
					aDir = 'cc' if movX > 0 else 'cw'
				else:
					aDir = 'cw' if movX > 0 else 'cc'
				e = elemCreateArc180To( e, ( endPt[0], yn, z ), 0, aDir )
				geom.append( e )
				e = elemCreateLineTo( e, ( startPt[0], yn, z ) )
				geom.append( e )
			else:
				# 1, 3, 5, ...: move x forward
				if movY > 0:
					aDir = 'cw' if movX > 0 else 'cc'
				else:
					aDir = 'cc' if movX > 0 else 'cw'
				e = elemCreateArc180To( e, ( startPt[0], yn, z ), 0, aDir )
				geom.append( e )
				e = elemCreateLineTo( e, ( endPt[0], yn, z ) )
				geom.append( e )

		# move y, then step through x
		else:
			xn = startPt[0] + (n+1) * incStep * sigX
			if n % 2 == 0:
				# 0, 2, 4, ...: move y back
				if movX > 0:
					aDir = 'cw' if movY > 0 else 'cc'
				else:
					aDir = 'cc' if movY > 0 else 'cw'
				e = elemCreateArc180To( e, ( xn, endPt[1], z ), 0, aDir )
				geom.append( e )
				e = elemCreateLineTo( e, ( xn, startPt[1], z ) )
				geom.append( e )
			else:
				# 1, 3, 5, ...: move x forward
				if movX > 0:
					aDir = 'cc' if movY > 0 else 'cw'
				else:
					aDir = 'cw' if movY > 0 else 'cc'
				e = elemCreateArc180To( e, ( xn, startPt[1], z ), 0, aDir )
				geom.append( e )
				e = elemCreateLineTo( e, ( xn,  endPt[1], z ) )
				geom.append( e )

	return geom



#############################################################################
### geomCreateZig
###
### Copied from ZigZag; was too lazy
### Creates a one-way flat milling shape, defined by two points, a step
### parameter and a selection which axis shall move first.
### Unlike "ZigZag", which mills in boths ways, this one moves back at a
### safe Z position (G0 moves).
### The amount of steps is calculated from the distance to travel, divided by
### the increment per step 'incStep', rounded up!
### For "Zig", unlike "ZigZag", the incStep value is the one between the
### "real" milling moves, not the rapid moves backward.
### For stupid values, a positive 'incStep' value but "more negative" end
### point coordinates, at least the first move is always executed. A linear
### move or a slot (if milled).
### Height (z) is takes from StartPt.
#############################################################################
def geomCreateZig( startPt, endPt, incStep, safeZ, yFirst, basNr=0 ):
	geom = []

	if incStep == 0:
		print( "INF: geomCreateZig: 'incStep' must not be zero" )
		return []

	if incStep < 0:
		print( "INF: geomCreateZig: negative 'incStep' value" )
		incStep *= -1

	# the 2nd move is always a rapid one, so we ignore
	incStep /= 2.0

	# use z from startPt
	z = startPt[2]

	if safeZ < z:
		print( "INF: geomCreateZig: safeZ < z: ", safeZ, z )
		return []

	# a marker for the direction of movement
	movX = endPt[0] - startPt[0]
	movY = endPt[1] - startPt[1]

	# a sign marker
	sigX = 1 if movX > 1 else -1
	sigY = 1 if movY > 1 else -1

	# always execute the first move
	if yFirst == 0:
		# x is going to move first
		e = elemCreateLine( startPt, ( endPt[0], startPt[1], z) )
		if incStep == 0:
			return [e]
		steps = movY / incStep
	else:
		# y is going to move first
		e = elemCreateLine( startPt, ( startPt[0], endPt[1], z) )
		if incStep == 0:
			return [e]
		steps = movX / incStep

	geom.append( e )

	steps = abs( math.ceil( steps ) )

	# splitting this in x and y is redundant, but easier to follow
	for n in range( steps ):

		# for x moves and step over y
		if yFirst == 0:
			yn = startPt[1] + (n+1) * incStep * sigY
			if n % 2 == 0:
				# 0, 2, 4, ...: move x back
				if movY > 0:
					aDir = 'cc' if movX > 0 else 'cw'
				else:
					aDir = 'cw' if movX > 0 else 'cc'
				# TODO: should be a rapid move and a "safe out" one; not possible for arc though (rapid)
				e = elemCreateArc180To( e, ( endPt[0], yn, safeZ ), 0, aDir )
				geom.append( e )
				# at least the linear move can be rapid
				e = elemCreateLineTo( e, ( startPt[0], yn, safeZ ), {'tMove':EXTRA_MOVE_RAPID} )
				geom.append( e )
			else:
				# 1, 3, 5, ...: move x forward
				if movY > 0:
					aDir = 'cw' if movX > 0 else 'cc'
				else:
					aDir = 'cc' if movX > 0 else 'cw'
				e = elemCreateArc180To( e, ( startPt[0], yn, z ), 0, aDir )
				geom.append( e )
				e = elemCreateLineTo( e, ( endPt[0], yn, z ) )
				geom.append( e )

		# move y, then step through x
		else:
			xn = startPt[0] + (n+1) * incStep * sigX
			if n % 2 == 0:
				# 0, 2, 4, ...: move y back
				if movX > 0:
					aDir = 'cw' if movY > 0 else 'cc'
				else:
					aDir = 'cc' if movY > 0 else 'cw'
				# TODO: should be a rapid move and a "safe out" one; not possible for arc though (rapid)
				e = elemCreateArc180To( e, ( xn, endPt[1], safeZ ), 0, aDir )
				geom.append( e )
				# at least the linear move can be rapid
				e = elemCreateLineTo( e, ( xn, startPt[1], safeZ ), {'tMove':EXTRA_MOVE_RAPID} )
				geom.append( e )
			else:
				# 1, 3, 5, ...: move x forward
				if movX > 0:
					aDir = 'cc' if movY > 0 else 'cw'
				else:
					aDir = 'cw' if movY > 0 else 'cc'
				e = elemCreateArc180To( e, ( xn, startPt[1], z ), 0, aDir )
				geom.append( e )
				e = elemCreateLineTo( e, ( xn,  endPt[1], z ) )
				geom.append( e )

	return geom



#############################################################################
### geomCreateSlotLine
###
### Creates a single slot from startPt to endPt. The depth (if any) is
### calculated from the difference of endPt-StartPt depth. The max depth per
### cut can be specified by "depthPerMove". 
### If the z height of the end point is greater (more positive) than the
### starting point, the moves will be done up. Might only be useful for
### form endmills, e.g. a slot-mill, etc.
### Probably obsolete because now geomCreateSlotPoly exists, but in fact
### we call it from there now if needed.
#############################################################################
def geomCreateSlotLine( startPt, endPt, depthPerMove, basNr=0 ):
	geom = []

	if startPt == endPt:
		print( "ERR: geomCreateSlot: startPt == endPt: ", startPt )
		return []

	if depthPerMove < 0:
		print( "INF: geomCreateSlot: correcting negative depthPerMove value to positive; was: ", depthPerMove )
		depthPerMove = abs( depthPerMove )

	totDepth = endPt[2] - startPt[2]

	if depthPerMove > abs( totDepth ):
		print( "ERR: geomCreateSlot: depthPerMove is greater than z-difference of points: ", depthPerMove, totDepth )
		return []

	if abs( totDepth ) > 0 and depthPerMove == 0:
		# this is done automatically by the algorithm below
		print( "INF: geomCreateSlot: depthPerMove is 0, but z-values differ; moving without change of z-height" )

	# Half the depth per move because we're also going backwards, right
	# into the slope we created before. Max depth per cut will be reached
	# at the end of every move.
	curDepth = startPt[2] - depthPerMove / 2.0
	sPt   = startPt
	ePt   = ( endPt[0], endPt[1], curDepth)
	pos   = 2

	# always make the first move
	e = elemCreateLine( sPt, ePt )
	geom.append( e )

	if depthPerMove == 0 or totDepth == 0:
		return geom

	while( True ):

		if totDepth < 0:
			curDepth -= depthPerMove / 2.0
			if curDepth < totDepth:
				curDepth = totDepth
		else:
			curDepth += depthPerMove / 2.0
			if curDepth > totDepth:
				curDepth = totDepth

		if pos == 2:
			sPt = ( sPt[0], sPt[1], curDepth )
			e = elemCreateLineTo( e, sPt )
			pos = 1
		else:
			ePt = ( ePt[0], ePt[1], curDepth )
			e = elemCreateLineTo( e, ePt )
			pos = 2

		geom.append( e )

		if curDepth == totDepth:
			if pos == 1:
				lastPt = ( ePt[0], ePt[1], totDepth )
			else:
				lastPt = ( sPt[0], sPt[1], totDepth )
			e = elemCreateLineTo( e, lastPt )
			geom.append( e )
			break

	return geom



#############################################################################
### geomCreateSlotPoly
###
### Creates a linear movement along a list of points, back and forth, to cut
### something off. by default, the depth is changed at the start- and end
### point, along the z-axis, "straight in". If "smoothEnter" is set to True,
### the first vector from the start and the end of the list (the first lines
### for each move, forward and back) will be used for the depth change.
### The initial cut depth is controlled by the z-coordinate of the start
### point, the total depth from the end point. All other z-values are
### ignored.
### Mostly useful for cutting outlines, e.g.
#############################################################################
def geomCreateSlotPoly( listOfPoints, incDepth, smoothEnter=False, basNr=0 ):

	if not isinstance( listOfPoints, list ):
		print("ERR: geomCreateSlotPoly: listOfPoints is not a list: ", type(listOfPoints))
		return []

	if len( listOfPoints ) < 2:
		print("ERR: geomCreateSlotPoly: listOfPoints has not enough points (<2): ", len(listOfPoints))
		return []

	if incDepth < 0:
		print("INF: geomCreateSlotPoly: incDepth negative; corrected that" )
		incDepth = abs( incDepth )

	if incDepth == 0:
		print("ERR: geomCreateSlotPoly: incDepth is zero" )
		return []

	# well, lol
	if len( listOfPoints ) == 2 and smoothEnter:
		return geomCreateSlotLine( listOfPoints[0], listOfPoints[1], incDepth, basNr )

	p1 = listOfPoints[0]
	zDepth = p1[2]
	pz = listOfPoints[-1]
	zEnd = pz[2]

	# check if we can travel through everything without changing the direction
	if p1[0] == pz[0] and p1[1] == pz[1] and len( listOfPoints ) > 2:
		moveForwardOnly = True
	else:
		moveForwardOnly = False

	if zEnd - zDepth >= 0:
		print("ERR: geomCreateSlotPoly: wrong z-values for first or last point: ", p1, pz )
		return []


	geom = []

	# TODO: not a single error check in here (in case any of the createLine thingies fail)
	while zDepth >= zEnd:

		if len( geom ) == 0:
			pt0 = listOfPoints[0]
			e = elemCreateVertex( pt0 )
		else:
			# Executed upon the 2nd iteration, so it's save to use 'pt' here, even if Pylint complains.
			# 'pt' is set in the for loop below
			pt0 = pt

		zDepth -= incDepth
		if zDepth < zEnd:
			zDepth = zEnd

		if smoothEnter:
			pass
		else:
			# hammer that tool right into the material
			e = elemCreateLineTo( e, (pt0[0], pt0[1], zDepth ) )
			geom.append( e )

		n = 0
		for pt in listOfPoints[1:]:

			e = elemCreateLineTo( e, (pt[0], pt[1], zDepth ) )
			geom.append( e )

			if n == 0 and smoothEnter and not moveForwardOnly:
				# go back to pt0, with the current zDepth and back again to
				# cut away the rest of the "ramp material"
				e = elemCreateLineTo( e, (pt0[0], pt0[1], zDepth ) )
				geom.append( e )
				# and back to where we were (will not cut anything)
				e = elemCreateLineTo( e, (pt[0], pt[1], zDepth ) )
				geom.append( e )
			
			n += 1

		if zDepth == zEnd:
			break

		if not moveForwardOnly:
			list.reverse( listOfPoints )

	# okay, if we went forward only, we need to cut the remaining ramp to the 2nd point:
	if moveForwardOnly:
		pt2 = listOfPoints[1]
		e = elemCreateLineTo( e, (pt2[0], pt2[1], zDepth)  )
		geom.append( e )

	return geom



#############################################################################
### geomCreateSlotSpiral
###
### Useful for either a deep, single mill width slot hole or as a material
### enter path for the SlotHole function (concentric slots with a depth)
#############################################################################
def geomCreateSlotSpiral( p1, p2, dia, depthSteps, depthPerStep, dir, clearBottom=True, basNr=0 ):
	con = []
	if dia <= 0.0:
		print( "ERR: geomCreateSlotSpiral: dia <= 0" )
		return []

	# To reduce the amount of calculations (lol), the slot hole is always created
	# along the y-axis and rotated afterwards, to match p2.

	# length is actually the "y-difference" now
	lenp1p2 = vecLengthXY( p1, p2 )
	if dir == 'cw':
		lenp1p2 = -lenp1p2
	np2 = vecAdd( p1, (0, lenp1p2, 0) )

	# WARNING: this is the "work vector", along the y-axis!
	vecp1p2 = vecSub( np2, p1 )

	# NEW 9/2021: quickfix to make p1 the center (was left of circle before)
	np1 = ( p1[0] - dia/2.0, p1[1], p1[2] )

	y = np1[1]
	z = np1[2]
	if basNr == 0:
		nr = 1
	else:
		nr = basNr

	# calculate the length of the individial segments for the correct z-depth
	lenLine = vecLengthXY( p1, p2 )
	lenArc  = math.pi * (dia / 2.0)
	depthNorm = depthPerStep / (2*lenLine + 2*lenArc)
	depthLine = depthNorm * lenLine
	depthArc  = depthNorm * lenArc

	if clearBottom:
		oneMore = 1
	else:
		oneMore = 0

	for i in range( 0, depthSteps + oneMore ):
		x1 = np1[0]
		x2 = np1[0] + dia
		diaAct = dia
		# arc at start point
		el = elemCreateArc180( (x1,y,z), (x2,y,z-depthArc), math.fabs( diaAct/2.0 ), dir, {'pNr':nr} )
		z -= depthArc
		nr += 1
		con.append(el)
		# line to dest
		el = elemCreateLineTo( el, (x2,y+lenp1p2,z-depthLine))
		z -= depthLine
		con.append(el)
		nr += 1
		# arc at dest point
		el = elemCreateArc180( (x2,y,z), (x1,y,z-depthArc), math.fabs( diaAct/2.0 ), dir, {'pNr':nr} )
		z -= depthArc
		el = elemTranslate( el, vecp1p2 )
		nr += 1
		con.append(el)

		x1 = np1[0]
		x2 = np1[0] - 0

		# line to start
		el = elemCreateLineTo( el, (x1,y,z-depthLine))
		z -= depthLine
		con.append(el)
		nr += 1

		# set all incremental depths to zero, so that the last loop will not change its depth
		if clearBottom and i == depthSteps - 1:
			depthArc  = 0
			depthLine = 0

	# rotate around p1 to original position
	if dir == 'cc':
		vDir = vecSub( p2, p1 )
	else:
		vDir = vecSub( p1, p2 )
	ang = math.radians( 90 ) - vecAngleXY( vDir )
	con = geomRotateZAt( con, math.degrees(ang), p1 )

	return con



#############################################################################
### geomCreateSlotRingHole
###
### Needs to be renamed (together with this CircularRingHole thing)
### Creates a slot shaped hole. Start depth is taken from p1's depth (z),
### the steps and total depth can be controlled with "depth" and "depthInc".
### TODO: Needs more text here
#############################################################################
def geomCreateSlotRingHole( p1, p2, diaStart, diaEnd, diaSteps, depth, depthInc, enterHeight, enterSteps, dir ):

	# TODO: add a lot more checkds here

	if enterHeight < 0:
		print( "ERR: geomCreateSlotRingHole: enterHeight must be > 0 (SAFETY FIRST :-)" )
		return []

	if depth < 0:
		print( "ERR: geomCreateSlotRingHole: depth must be >= 0" )
		return []

	if depthInc < 0:
		print( "ERR: geomCreateSlotRingHole: depthInc must be be >= 0" )
		return []

	if enterHeight < depthInc:
		print( "ERR: geomCreateSlotRingHole: enterHeight must be larger than depthInc: ", enterHeight, depthInc )
		return []


	con = []
	depthCurrent = 0

	ptRetStart = None

	while True:

		# entry movement
		geomEntry = geomCreateSlotSpiral( (p1[0], p1[1], p1[2] - depthCurrent + enterHeight), p2, diaStart, enterSteps, enterHeight / enterSteps, dir, clearBottom=False)

		# do we need to add the "retract to next entry" move yet?
		if ptRetStart is not None:
			ptRetEnd = geomGetFirstPoint( geomEntry )
			# not nice as this makes a 180° turn
			# con.append(  elemCreateArc180( ptRetStart, ptRetEnd, 0, 'cw' if dir == 'cc' else 'cc' )  )

			ptRetMid = vecExtractMid( ptRetStart, ptRetEnd )
			con.append(  elemCreateArc180( ptRetStart, ptRetMid, 0, dir )  )
			con.append(  elemCreateArc180( ptRetMid,   ptRetEnd, 0, 'cw' if dir == 'cc' else 'cc' )  )

		# add the entry movement
		con += geomEntry

		# create the main milling op
		con += geomCreateConcentricSlots( (p1[0], p1[1], p1[2] - depthCurrent), p2, diaStart, diaEnd, diaSteps, dir )

		if depthCurrent < depth:
			depthCurrent += depthInc
			if depthCurrent > depth:
				depthCurrent = depth
		else:
			break

		# save point to retract from
		ptRetStart = geomGetLastPoint( con )
		if ptRetStart is None:
			print( "ERR: geomCreateSlotRingHole: geomGetLastPoint returned nothing valid" )
			return []

	# add retract movement; will retract with two arcs to the starting point.
	ex1 = geomGetLastPoint( con )
	ex2 = geomGetFirstPoint( con )
	exm = vecExtractMid( ex2, ex1 )
	con.append(  elemCreateArc180( ex1, exm, 0, dir )  )
	con.append(  elemCreateArc180( exm, ex2, 0, 'cw' if dir == 'cc' else 'cc' )  )

	return con



#############################################################################
### geomCreateSlotRingHoleTEST
###
### Testing some "feedrate in vertices" code.
#############################################################################
def geomCreateSlotRingHoleTEST( p1, p2, diaStart, diaEnd, diaSteps,
								depth, depthInc,
								enterHeight, enterSteps, dir ):

	# TODO: add a lot more checks here

	if enterHeight < 0:
		print( "ERR: geomCreateSlotRingHole: enterHeight must be > 0 (SAFETY FIRST :-)" )
		return []

	if depth < 0:
		print( "ERR: geomCreateSlotRingHole: depth must be >= 0" )
		return []

	if depthInc < 0:
		print( "ERR: geomCreateSlotRingHole: depthInc must be be >= 0" )
		return []

	if enterHeight < depthInc:
		print( "ERR: geomCreateSlotRingHole: enterHeight must be larger than depthInc: ", enterHeight, depthInc )
		return []


	con = []
	depthCurrent = 0

	ptRetStart = None

	while True:

		# entry movement
		geomEntry = geomCreateSlotSpiral( (p1[0], p1[1], p1[2] - depthCurrent + enterHeight), p2, diaStart, enterSteps, enterHeight / enterSteps, dir, clearBottom=False)

		# get the coordinate for the 1st vertex; used for "retract to next" and the feedrate vertex below
		ptRetEnd = geomGetFirstPoint( geomEntry )

		# do we need to add the "retract to next entry" move yet?
		if ptRetStart is not None:
			# not nice as this makes a 180° turn
			# con.append(  elemCreateArc180( ptRetStart, ptRetEnd, 0, 'cw' if dir == 'cc' else 'cc' )  )

			# TESTING: ADD FEEDRATE VERTEX
			con.append(  elemCreateVertex( ptRetStart, {'tFeed':"FEED_RETRACT"} ) )

			ptRetMid = vecExtractMid( ptRetStart, ptRetEnd )
			con.append(  elemCreateArc180( ptRetStart, ptRetMid, 0, dir )  )
			con.append(  elemCreateArc180( ptRetMid,   ptRetEnd, 0, 'cw' if dir == 'cc' else 'cc' )  )

		# TESTING: ADD FEEDRATE VERTEX
		con.append(  elemCreateVertex( ptRetEnd, {'tFeed':"FEED_ENGAGE"} ) )

		# add the entry movement
		con += geomEntry

		# create the main milling op
		geomMill = geomCreateConcentricSlots( (p1[0], p1[1], p1[2] - depthCurrent), p2, diaStart, diaEnd, diaSteps, dir )

		# TESTING: ADD FEEDRATE VERTEX
		con.append(  elemCreateVertex( geomGetFirstPoint( geomMill ), {'tFeed':"FEED_BASE", 'tMsg':"TEST COMMENT: NOW MILLING; millmillmillmill"} ) )

		# add the milling op
		con += geomMill

		if depthCurrent < depth:
			depthCurrent += depthInc
			if depthCurrent > depth:
				depthCurrent = depth
		else:
			break

		# save point to retract from
		ptRetStart = geomGetLastPoint( con )
		if ptRetStart is None:
			print( "ERR: geomCreateSlotRingHole: geomGetLastPoint returned nothing valid" )
			return []

	# add retract movement; will retract with two arcs to the starting point.
	ex1 = geomGetLastPoint( con )
	ex2 = geomGetFirstPoint( con )
	exm = vecExtractMid( ex2, ex1 )

	# TESTING: ADD FEEDRATE VERTEX
	con.append(  elemCreateVertex( ex1, {'tFeed':"FEED_RETRACT"} ) )

	con.append(  elemCreateArc180( ex1, exm, 0, dir )  )
	con.append(  elemCreateArc180( exm, ex2, 0, 'cw' if dir == 'cc' else 'cc' )  )

	return con



#############################################################################
### geomCreateContour
###
### All elements in a part are moved along a perpendicular line, which length
### is given by "dist".
### This "simple contour" is not(!) closed.
### dist < 0 means left and vice versa
#############################################################################
def geomCreateContour(part,dist):
	if not partCheckContinuous(part):
		print( "ERR: geomCreateContour: part not continuous" )
		return []
	if dist==0.0:
		print( "ERR: geomCreateContour: distance is 0" )
		return []
	# ToDo:
	partIsClosed=partCheckClosed(part)

	CoarseCont=[]

	for i in range(1,len(part['elements'])+1):
		el=partGetElement(part,i)
		if el==[]:
			print( "ERR: geomCreateContour: empty element at pos.: ",i )
			return []

		eln={}

		# line
		if el['type']=='l':
			vecL=vecExtract(el['p1'],el['p2'])
			if dist < 0.0:
				an=-math.pi/2.0
			else:
				an=math.pi/2.0
			vecN=vecRotateZ(vecL,an)
			vecN=vecScale(vecN,0)
			vecN=vecScale(vecN,math.fabs(dist))
			eln=elemTranslate(el,vecN)

		# arc
		if el['type']=='a':
			pass 
		
		if not eln=={}:
			CoarseCont.append(eln)

	return CoarseCont



#############################################################################
### geomCreateSlotContour
###
### Creates a single slot-contour for every element in the part.
### If dist < 0, the contour begins at the left side of an element and
### continues in clockwise direction.
#############################################################################
def geomCreateSlotContour(part,dist,basNr=0):

	if dist==0.0:
		print( "ERR: geomCreateSlotContour: distance is 0" )
		return []
	
	if basNr==0:
		Nr=1
	else:
		Nr=basNr

	slo=[]

	for i in range(1,len(part['elements'])+1):
		el=partGetElement(part,i)
		if el==[]:
			print( "ERR: geomCreateSlotContour: empty element at pos.: ",i )
			return []

		sel=geomCreateSlotContourFromElement(el,dist,Nr)
		Nr+=len(sel)
		if not sel==[]:
			slo+=sel

	return slo



#############################################################################
### geomExtractSlotDirVecs
###
### Extracts all first-two elements of the geometry.
#############################################################################
def geomExtractSlotDirVecs(geom):
	gout=[]
	i=1
	j=0
	for el in geom:
		if j < 2:
			el['pNr']=i
			i+=1
			gout.append(el)
		j+=1
		if j==4:
			j=0

	return gout



#############################################################################
### geomCreateSlotContourFromElement
###
### Creates a single "slot-contour" around an element.
### The closest distance from the outline of the contour to the points on the
### element are given by "dist".
#############################################################################
def geomCreateSlotContourFromElement(el,dist,basNr=0):
	con=[]

	if dist==0.0:
		print( "ERR: geomCreateSlotContourFromElement: distance is 0" )
		return []

	if basNr==0:
		Nr=1
	else:
		Nr=basNr

	# line
	if el['type']=='l':
		vecL=vecExtract(el['p1'],el['p2'])
		# this will only work in a xy-plane projection!
		vecL=(vecL[0],vecL[1],0)
		if vecLength(vecL) <= 0.0:
			print( "ERR: geomCreateSlotContourFromElement: no length in xy-plane projection" )
			return []
		if not el['p1'][2] == el['p2'][2]:
			print( "ERR: geomCreateSlotContourFromElement: element not in xy-plane or parallel: ",el )
			return []
		
		if dist < 0.0:
			an=-math.pi/2.0
		else:
			an=math.pi/2.0
		vecN=vecRotateZ(vecL,an)
		vecN=vecScale(vecN,0)
		vecN=vecScale(vecN,math.fabs(dist))
		l1=elemTranslate(el,vecN)
		l2=elemTranslate(el,vecReverse(vecN))
		l2=elemReverse(l2)
		if dist < 0.0:
			dir='cw'
		else:
			dir='cc'

		a1=elemCreateArc180(l1['p2'],l2['p1'],math.fabs(dist),dir,{'pNr':0})
		a2=elemCreateArc180(l2['p2'],l1['p1'],math.fabs(dist),dir,{'pNr':0})

		if a1==[] or a2==[]:
			print( "ERR: geomCreateSlotContourFromElement: error creating a1 with dir: ",dir )
			if a1==[]:
				print( "ERR: geomCreateSlotContourFromElement: error creating a1: ",l1['p2'],l2['p1'] )
			else:
				print( "ERR: geomCreateSlotContourFromElement: error creating a2: ",l2['p2'],l1['p1'] )
			con=[]
		else:
			l1['pNr']=Nr
			Nr+=1
			a1['pNr']=Nr
			Nr+=1
			l2['pNr']=Nr
			Nr+=1
			a2['pNr']=Nr
			con+=[l1,a1,l2,a2]

	# arc
	if el['type']=='a':
		# get midpoint
		pm=arcCenter180XY(el['p1'],el['p2'],el['rad'],el['dir'])
		if pm==None:
			print( "ERR: geomCreateSlotContourFromElement: unable to calc arc mispoint from: ",el )
			return []

		vec1=vecExtract(el['p1'],pm)
		vec1=(vec1[0],vec1[1],0)
		vec2=vecExtract(el['p2'],pm)
		vec2=(vec2[0],vec2[1],0)
		if vecLength(vec1) <= 0.0 or vecLength(vec2) <= 0.0:
			print( "ERR: geomCreateSlotContourFromElement: no length in xy-plane projection" )
			return []
		if not el['p1'][2] == el['p2'][2]:
			print( "ERR: geomCreateSlotContourFromElement: element not in xy-plane or parallel: ",el )
			return []

		vec1=vecScale(vec1,0)
		vec1=vecScale(vec1,math.fabs(dist))
		vec2=vecScale(vec2,0)
		vec2=vecScale(vec2,math.fabs(dist))

		if dist < 0.0 and el['dir']=='cc' or dist > 0.0 and el['dir']=='cw':
			# arc #1
			# points of arc move towards the midpoint
			if dist == el['rad']:
				# hack: we are exactly on the midpoint
				a1=elemCreateVertex(pm,{'pNr':0})
			else:
				p1=vecAdd(el['p1'],vec1)
				p2=vecAdd(el['p2'],vec2)
				rad=el['rad']-math.fabs(dist)
				if rad == 0.0:
					# midpoint again hack
					a1=elemCreateVertex(pm,{'pNr':0})
				else:
					if rad < 0.0:
						if el['dir']=='cw':
							dir='cc'
						else:
							dir='cw'
						rad=math.fabs(rad)
					else:
						dir=el['dir']
					a1=elemCreateArc180(p1,p2,rad,dir,{'pNr':0})
			#arc #2
			# points move away from midpoint
			vec1=vecReverse(vec1)
			vec2=vecReverse(vec2)
			p1=vecAdd(el['p1'],vec1)
			p2=vecAdd(el['p2'],vec2)
			rad=el['rad']+math.fabs(dist)
			if el['dir']=='cw':
				dir='cc'
			else:
				dir='cw'
			a2=elemCreateArc180(p2,p1,rad,dir,{'pNr':0})
		else:
			# arc #1
			# points move away from midpoint
			vec1=vecReverse(vec1)
			vec2=vecReverse(vec2)
			p1=vecAdd(el['p1'],vec1)
			p2=vecAdd(el['p2'],vec2)
			rad=el['rad']+math.fabs(dist)
			a1=elemCreateArc180(p1,p2,rad,el['dir'],{'pNr':0})
			# reorder
			vec1=vecReverse(vec1)
			vec2=vecReverse(vec2)
			# arc #2
			# points of arc move towards the midpoint
			if dist == el['rad']:
				# hack: we are exactly on the midpoint
				a2=elemCreateVertex(pm,{'pNr':0})
			else:
				p1=vecAdd(el['p1'],vec1)
				p2=vecAdd(el['p2'],vec2)
				rad=el['rad']-math.fabs(dist)
				if rad == 0.0:
					# midpoint again hack
					a2=elemCreateVertex(pm,{'pNr':0})
				else:
					if rad < 0.0:
						dir=el['dir']
						rad=math.fabs(rad)
					else:
						if el['dir']=='cw':
							dir='cc'
						else:
							dir='cw'
					a2=elemCreateArc180(p2,p1,rad,dir,{'pNr':0})

		# arc #3 (cap 1)
		if not a1=={}:
			if 'p2' in a1:   # could be a vertex
				p1=a1['p2']
			else:
				p1=a1['p1']
			p2=a2['p1']
			if dist < 0.0:
				dir='cw'
			else:
				dir='cc'
			a3=elemCreateArc180(p1,p2,math.fabs(dist),dir,{'pNr':0})

		# arc #4 (cap 2)
		if not a2=={}:
			if 'p2' in a2:   # could be a vertex
				p1=a2['p2']
			else:
				p1=a2['p1']
			p2=a1['p1']
			if dist < 0.0:
				dir='cw'
			else:
				dir='cc'
			a4=elemCreateArc180(p1,p2,math.fabs(dist),dir,{'pNr':0})
		
		if not a1=={}:
			a1['pNr']=Nr
			Nr+=1
			con.append(a1)
		if not a3=={}:
			a3['pNr']=Nr
			Nr+=1
			con.append(a3)
		if not a2=={}:
			a2['pNr']=Nr
			Nr+=1
			con.append(a2)
		if not a4=={}:
			a4['pNr']=Nr
			con.append(a4)
	# end el['type']=='a'
		
	return con



#############################################################################
### geomCreateLeftContourBAK
###
### Creates a single "inner-contour" around a list of slots.
### This function does NOT check for intersections of elements!
### It simply "moves" along the slots (with nice blendings, indeed 8)
### The geometry must meet the following conditions:
### - direction of elements has to be counter-clockwise (mhh, not always...)
### - dist has to be negative (aka.: we follow the left side of the slots)
#############################################################################
def geomCreateLeftContourBAK(part,dist,basNr=0):

	conNr=1
	con=[]
	slo1=[]
	slo2=[]
	
	totLen=len(part['elements'])

	if not dist < 0.0:
		print( "ERR: geomCreateLeftContour: distance is not negative: ",dist )
		return []

	for i in range(1,totLen+1):
		# get element

		# !!!future upgrade!!!
		
#    if con==[]:
#      el1=partGetElement(part,i)
#    else:
#      el1=con[-1]
		el1=partGetElement(part,i)

		if el1==[]:
			print( "ERR: geomCreateLeftContour: empty element at pos.: ",i )
			return []

		# create a slot around the first element
		slo1=geomCreateSlotContourFromElement(el1,dist)
		if slo1==[]:
			print( "ERR: geomCreateLeftContour: unable to create slot for first element: ",i )
			return []

		if len(slo1)!=4:
			print( "ERR: geomCreateLeftContour: slot has less than 4 elements for first elem: ",i )
			return []

		# get the second element
		if i < totLen:
			el2=partGetElement(part,i+1)
		else:
			if partCheckClosed(part):
				# if part is closed, take first element to finish the operation
				el2=partGetElement(part,1)
			else:
				# nothing more to do
				break

		if el2==[]:
			print( "ERR: geomCreateLeftContour: empty element at pos.: ",i+1 )
			return []

		# create a slot around the second element
		slo2=geomCreateSlotContourFromElement(el2,dist)
		if slo2==[]:
			print( "ERR: geomCreateLeftContour: unable to create slot for second element: ",i )
			return []

		if len(slo2)!=4:
			print( "ERR: geomCreateLeftContour: slot has less than 4 elements for second elem: ",i )
			return []


		# determine the angle to the next element
		#
		# if a < 0: next element turns to the right
		#   -> create a 'cw' circle to slo2[1]['p1']
		#
		# if a > 0: next element turns to the left
		#   -> determine intersection on slo2[1] for normalized distance <= 1.0
		#   -> determine intersection on slo2[2] for normalized distance <= 1.0
		#   -> if intersections are beyond a norm. dist. of 1.0 -> follow slo2[1]
		#   -> else follow slo2[1] or slo2[2] to slo2[1] from intersection
		#
		# if a== 0: no change of direction
		#   -> simply follow slo2[1]
		
		# This _should_ work by calculating the values from the original element,
		# not their representation by slot elements.
		ang=elemNextAngle(el1,el2)
		print( "*** angle: i,ang: ",i,ang*360/(2.0*math.pi) )
		if ang==None:
			print( "ERR: geomCreateLeftContour: no angle after element: ",i )
			return []

		# easy operations first =)
		if math.fabs(ang) < RADTOL:
			print( "op == 0" )
			ee=elemCopy(slo1[0])
			ee['p2']=slo2[0]['p1']
			ee['pNr']=conNr
			conNr+=1
			con.append(ee)

		if ang <= -RADTOL:
			print( "op < 0" )
			ee=elemCopy(slo1[0])
			ee['pNr']=conNr
			conNr+=1
			con.append(ee)
			# ToDo:
			# this circle may have an angle > pi!
			ee=elemCreateArc180(slo1[0]['p2'],slo2[0]['p1'],math.fabs(dist),'cw',{'pNr':conNr})
			conNr+=1
			con.append(ee)
		
		if ang >= RADTOL:
			print( "op > 0" )

#     old style
#      hi=elemIntersectsElemXY(slo1[0],slo2[0])
#      print( "hi: ",hi )

			hi=elemIntersectsElemXY(slo1[0],slo2[1])
			hiX=1
			print( "hi(1): ",hi )
			elemDebugPrint(slo1[0])      
			elemDebugPrint(slo2[1])

			if hi==[]:
				hi=elemIntersectsElemXY(slo1[0],slo2[0])
				hiX=2
				print( "hi(0): ",hi )
				elemDebugPrint(slo1[0])      
				elemDebugPrint(slo2[0])

			if hi==[]:
				print( "ERR: geomCreateLeftContour: no intersections on left turn at elem nr: ",i )
				return []
			
			phi=None
			dhi=-1.0
			for i in hi:
				if i[0] > 0.0 and i[0] <= 1.0:
					if i[0] > dhi:
						dhi=i[0]
						phi=i[1]
				else:
					if i[0]==None and slo1[0]['type']=='a':
						phi=i[1]
						break

			if phi != None:
				ee=elemCopy(slo1[0])
				ee['p2']=phi
				ee['pNr']=conNr
				conNr+=1
				con.append(ee)

		# end if ang==0
	# end for        

	# con = geomTrimPointsStartToEnd( con, partCheckClosed(part) )

	return con



#############################################################################
### geomCreateLeftContour
###
#############################################################################
def geomCreateLeftContour( part, dist, basNr=0 ):
	con=[]
	conNr=1
	conSkip=-1

	slo = geomCreateSlotContour(part,dist)
	
	if slo == []:
		print( "ERR: geomCreateLeftContour: error while creating slot elements from part " )
		return []

	slo = geomExtractSlotDirVecs(slo)
	
	print( "len(slo): ",len(slo) )

	# process all elements in the list
	for i in range(len(slo)):

		if i < conSkip:
			print( "." )
			continue
		
		his=[]

		for ii in slo:
			elemDebugPrint(ii)

		for j in range(i+1,i+len(slo)-2):
			if j > len(slo)-1:
				j-=len(slo)
			his.append(elemIntersectsElemXY(slo[i],slo[j]))

		# future upgrade =)
		if True:
			print( "**********" )
			print( "*** NR ***",i )
			elemDebugPrint(slo[i])
	#    print( "len",len(his) )
			
			for j in his:
				print( j )

			sdi = 999999999999999.9
			eleCount = 0
			eleTarget = None
			eleInt = None
			
			for j in his:
				for k in j:
					print( "k[0] / sdi ",k[0]," / ",sdi )
					if k[0] <= sdi and k[0] >= 0.0 + LINTOL:
						sdi=k[0]
						eleInt=k[1]
						eleTarget=eleCount
				eleCount+=1
				if eleCount > len(slo)-1:
					eleCount-=len(slo)

			if eleTarget==None:
				eleTarget=i+1
			else:
				eleTarget+=i+1
			
			if eleTarget > len(slo)-1:
				eleTarget-=len(slo)
				
			conSkip=eleTarget
			
			print( "FOUND El Nr:  ",eleTarget )
			print( "FOUND eleInt: ",eleInt )

			eleElem=elemCopy(slo[i])
			eleElem['pNr']=conNr
			conNr+=1
			if eleInt != None:
				# set new endpoint of current element
				eleElem['p2']=eleInt
				# set the limiting element's startpoint to this intersection, too
				elemDebugPrint(slo[eleTarget])
				slo[eleTarget]['p1']=eleInt
				elemDebugPrint(slo[eleTarget])
			con.append(eleElem)

			if conSkip==0:
				break        


	con = geomTrimPointsStartToEnd( con, partCheckClosed(part) )

			
	return con



#############################################################################
### geomCreatePolyVertsOffset
###
#############################################################################
def geomCreatePolyVertsOffset( geomVerts: list, offset: float, basNr: int = 0 ) -> list:
	"""
	Offsets the vertices of a PolyVerts-geom.
	The vertices will be created on a vector going through the middle of the angle formed by
	three vertices; acting as two lines going out from the mid-vertex.

	In case offset is 0, nothing is changed. Yep.

	The created vertices can then (after some additional cleanup) be used to create parallel lines to the original geometry, aka offset lines or polygons.
	If the offset is negative, the parallel lines are created to the left side of the original geometry; if positive, to the right side.
	The vertices' z-values are ignored; and their order should be given anti-clockwise.

	Args:
		geomVerts (list): A list of vertices representing the original geometry, e.g.
		offset (float): The offset value determining how far the vertices are from the original geometry. <0 means inside, >0 means outside.
		basNr (int, optional): An optional base number, default is 0.

	Returns:
		list: A geom with vertices, shifted by the given offset.
	"""
	if not isinstance( geomVerts, list ):
		print("ERR: geomCreatePolyVertsOffset: geomVerts is not a list: ", type(geomVerts))
		return []

	if len( geomVerts ) < 3:
		print("ERR: geomCreatePolyVertsOffset: geomVerts has not enough points (<3): ", len(geomVerts))
		return []

	if not isinstance( geomVerts[0], dict ):
		print("ERR: geomCreatePolyVertsOffset: content of geomVerts is not a dict: ", type(geomVerts[0]))
		return []



	lenGeom = len( geomVerts )	

	geom = []


	# a shortcut in case offset == 0
	if offset == 0.0:
		return geomVerts


	for i in range( lenGeom ):
		pts = []

		# iterate through the list; end at the first entry again (modulo)
		for j in range( 3 ):
			pts.append( geomVerts[ (i+j) % lenGeom]['p1'] )
		
		v1 = vecExtract( pts[1], pts[0] ) # vector "to the left"
		v2 = vecExtract( pts[1], pts[2] ) # vector "to the right"
		a1 = vecAngleXY( v1 )             # absolute angle of v1
		a2 = vecAngleXY( v2 )             # absolute angle of v2

		ad = vecAngleDiffXY( v2, v1 )     # angle between v1 and v2
		an = ad / 2.0 + a2                # half angle between v1 and v2 (where the points will be placed)

		# small angles or large ones toward 2*Pi will cause a divide by zero
		if ( adabs := math.fabs(ad) ) < MINOFFSETANGLE or (adabs + MINOFFSETANGLE) > (2.0 * math.pi) :
			print("ERR: geomCreatePolyVertsOffset: angle of poly corner too small/large: ", ad )
			return []

		# recalculate the length of the offset vector and also the direction;
		# negative offset values shall move to the left (inside), positive to the right (outside)
		vn = ( -offset / math.sin( ad / 2.0 ), 0, 0)

		# [...] and rotate it in place
		vn = vecRotateZ( vn, -an )

		geom.append( elemCreateVertex( vecAdd( pts[1], vn ) ) )

	# because the algorithm starts at the second vertex, they're now all off by one
	geom.insert( 0, geom.pop() )

	return geom



#############################################################################
### geomCreatePolyOffset
###
#############################################################################
def geomCreatePolyOffset( geomPoly: list, offset: float, basNr: int = 0 ) -> list:
	# Here's the strategy [tm] *** FOR INSIDE OFFSETS ***:
	#   - extract verts from poly
	#   - use geomCreatePolyVertsOffset() to create the offset vertices
	#   - use geomCreatePoly() to create (A): the offset lines
	#   - use geomCreatePoly() to create (B): the half angle lines; from the old vertices to the corresponding new ones (p1 -> p1', p2 -> p2', ...)
	# So far, I can think of two methods, which needs both be tested, to determine which vertices need to be deleted:
	#   - if a created vertex is outside of the original polygon, delete it;
	#     GUESS: it most likely needs to be "moved back" along the lines, until we hit the first intersection of two offset lines
	#   - if one of the half-angle lines intersects one of the offset lines, delete the vertex
	#     GUESS: it most likely needs to be "moved back" along the lines, until we hit the first intersection of two offset lines

	# TODO: sanity checks
	#   - check if geomPoly ia a poly (and not a list of verts)

	geom = []

	geomVerts = geomExtractPolyVerts( geomPoly )
	offsVerts = geomCreatePolyVertsOffset( geomVerts, offset, basNr )

	if len( geomVerts ) != len( offsVerts ):
		print("ERR: geomCreatePolyOffset: size of original and offset verts list don't match: ", len(geomVerts), len(offsVerts) )
		return []

	angleLines = []
	for i in range( len( geomVerts ) ):
		angleLines.append( elemCreateLine( geomVerts[i]['p1'], offsVerts[i]['p1'] ) )

	geomLines = geomCreatePoly( geomVerts, basNr )
	offsLines = geomCreatePoly( offsVerts, basNr )


	offsVertsCleaned = []
	offsVertsDeleted = []
	for i in offsVerts:
		if geomCheckVertexInPoly( i, geomPoly ):
			offsVertsCleaned.append( i )
		else:
			offsVertsDeleted.append( i )

	# DEBUG SHOW ALL
#	geom = geomVerts + offsVerts + angleLines + offsLines + geomLines
	geom = angleLines + offsLines + geomLines + offsVertsCleaned



	return geom



#############################################################################
### geomExtractPolyVerts
###
#############################################################################
def geomExtractPolyVerts( geomPoly: list ) -> list:

	geom = []

	for i in geomPoly:

		if i['type'] == 'a':
			print("ERR: geomExtractPolyVerts: arcs are not supported; skipped: ", i )
			continue

		if i['type'] == 'l':
			geom.append( elemCreateVertex( i['p1'] ) )

	return geom



#############################################################################
### geomCreatePolyVerts
###
#############################################################################
def geomCreatePolyVerts( listOfPoints: list, basNr: int = 0 ) -> list:
	"""
	Create a geom of vertices from a list of points.
	The list of points should be given anti-clockwise.

	Args:
		listOfPoints (list): A list of points representing the original geometry, e.g. [ (0,0,0), (10,0,0), (0,10,0), (0,10,0), ... ]
		basNr (int, optional): An optional base number, default is 0.

	Returns:
		list: A geom with vertices.
	"""

	geom = []

	for i in listOfPoints:
		geom.append( elemCreateVertex( i ) )

	return geom



#############################################################################
### geomCreatePoly
###
#############################################################################
def geomCreatePoly( geomVerts: list, basNr: int = 0 ) -> list:
	"""
	Creates a closed polygon as a geom made of vectors from a list of vertices.

	Args:
		geomVerts (list): A geom (list of vertices) representing the geometry.
		basNr (int, optional): An optional base number, default is 0.

	Returns:
		list: A geom of vectors.
	"""
	if not isinstance( geomVerts, list ):
		print("ERR: geomCreatePoly: geomVerts is not a list: ", type(geomVerts))
		return []

	lenList = len( geomVerts )

	if lenList < 3:
		print("ERR: geomCreatePoly: geomVerts has not enough points (<3): ", len(geomVerts))
		return []


	geom = []

	for i in range( lenList ):
		geom.append( elemCreateLine( geomVerts[i]['p1'], geomVerts[ (i+1) % lenList ]['p1'] ) )


	return geom



#############################################################################
### geomTranslate
###
### Moves a geometry  into the direction specified by a vector.
### Returns a new instance
#############################################################################
def geomTranslate( geom, vec ):
	# TODO: probably not necessary to copy the element here
	geomn = []
	if not isinstance( geom, list ):
		print( "ERR: geomTranslate: 'geom' not a list" )
		return []
	for elem in geom:
		if not isinstance( elem, dict ):
			print( "ERR: geomTranslate: element is not a dict:", type(elem) )
			return []
		if 'type' not in elem:
			print( "ERR: geomTranslate: no 'type' in element" )
			return []
		else:
			if elem['type'] == 'v' or elem['type'] == 'l' or elem['type'] == 'a':
				geomn.append( elemTranslate( elem, vec ) )
			else:
				print( "ERR: geomTranslate: unknown 'type' in element:", elem['type'] )
				return []
	return geomn



#############################################################################
### geomRotateZ
###
### Rotates a geometry around the center of the z-axis vec(0,0,1).
### Returns a new instance
#############################################################################
def geomRotateZ( geom, ang ):
	# TODO: probably not necessary to copy the element here
	geomn=[]
	# mhh, basically the same code as in geomTranslate above :-/
	if not isinstance( geom, list ):
		print( "ERR: geomRotateZ: 'geom' not a list" )
		return []
	for elem in geom:
		if not isinstance( elem, dict ):
			print( "ERR: geomRotateZ: element is not a dict:", type(elem) )
			return []
		if 'type' not in elem:
			print( "ERR: geomRotateZ: no 'type' in element" )
			return []
		else:
			if elem['type'] == 'v' or elem['type'] == 'l' or elem['type'] == 'a':
				geomn.append( elemRotateZ( elem, ang ) )
			else:
				print( "ERR: geomRotateZ: unknown 'type' in element:", elem['type'] )
				return []
	return geomn



#############################################################################
### geomRotateZAt
###
### Rotates a geometry around a point given by 'vec'.
### Returns a new instance
#############################################################################
def geomRotateZAt( geom, ang, center ):
	# TODO: probably not necessary to copy the element here
	geomn=[]
	# mhh, basically the same code as in geomTranslate above :-/
	if not isinstance( geom, list ):
		print( "ERR: geomRotateZAt: 'geom' not a list" )
		return []
	for elem in geom:
		if not isinstance( elem, dict ):
			print( "ERR: geomRotateZAt: element is not a dict:", type(elem) )
			return []
		if 'type' not in elem:
			print( "ERR: geomRotateZAt: no 'type' in element" )
			return []
		else:
			if elem['type'] == 'v' or elem['type'] == 'l' or elem['type'] == 'a':
				vec = vecReverse( center )
				elemn = elemTranslate( elem, vec )
				elemn = elemRotateZ( elemn, ang )
				elemn = elemTranslate( elemn, center )
				geomn.append( elemn )
			else:
				print( "ERR: geomRotateZAt: unknown 'type' in element:", elem['type'] )
				return []
	return geomn



#############################################################################
### geomTrimPointsStartToEnd
###
### Trims a list of elements:
### The startpoint of the _next_ element is set to the end position of
### the previous element.
### No checks are done!
### Elements have to be in the right order!
#############################################################################
def geomTrimPointsStartToEnd( elIn, isClosed=False ):
	elOut=[]
	
	for i in elIn:
		elOut.append(i)

	maxLen=len(elOut)-1

	for i in range(maxLen):
		if 'p2' in elOut[i]:
			elOut[i+1]['p1']=elOut[i]['p2']
		else:
			elOut[i+1]['p1']=elOut[i]['p1']
		
	if isClosed:
		if 'p2' in elOut[maxLen]:
			elOut[0]['p1']=elOut[maxLen]['p2']
		else:
			elOut[0]['p1']=elOut[maxLen]['p1']

	return elOut



#############################################################################
### geomGetLastPoint
###
### Returns the point of the last element in a geom.
#############################################################################
def geomGetLastPoint( geom ):

	if not isinstance( geom, list ):
		print( "ERR: geomGetLastPoint: geom is not a list: ", type(geom) )
		return None

	if len( geom ) < 1:
		print( "ERR: geomGetLastPoint: geom is empty" )
		return None

	e = geom[-1]

	if not isinstance( e, dict ):
		print( "ERR: geomGetLastPoint: last element of geom is not a dict: ", type(e) )
		return None

	pts = elemGetPts( e )

	if   len(pts) == 1:
		return pts[0]
	elif len(pts) == 2:
		return pts[1]

	print( "ERR: geomGetLastPoint: last element does not have valid amount of points: ", len(pts) )
	return None



#############################################################################
### geomGetFirstPoint
###
### Returns the point of the last element in a geom.
#############################################################################
def geomGetFirstPoint( geom ):

	if not isinstance( geom, list ):
		print( "ERR: geomGetFirstPoint: geom is not a list: ", type(geom) )
		return None

	if len( geom ) < 1:
		print( "ERR: geomGetFirstPoint: geom is empty" )
		return None

	e = geom[0]

	if not isinstance( e, dict ):
		print( "ERR: geomGetFirstPoint: first element of geom is not a dict: ", type(e) )
		return None

	pts = elemGetPts( e )

	if len(pts) > 0:
		return pts[0]

	print( "ERR: geomGetFirstPoint: first element does not have valid amount of points: ", len(pts) )
	return None



#############################################################################
### geomCheckVertexInPoly
###
#############################################################################
def geomCheckVertexInPoly( vertex: dict, geomPoly: list ) -> bool:
	"""
	Checks if a vertex is in- or outside of a polygon.
	Uses the simple ray casting algorithm

	Args:
		geomPoly (list): A polygon geom (list of vectors) representing the geometry.
		vertex (dict): one vertex element

	Returns:
		bool: True/False for inside/outside of polygon
		None: on error
	"""

	if not isinstance( geomPoly, list ):
		print("ERR: geomCheckVertexInPoly: geomVerts is not a list: ", type(geomPoly))
		return None

	lenList = len( geomPoly )

	if lenList < 3:
		print("ERR: geomCheckVertexInPoly: geomVerts has not enough points (<3): ", len(geomPoly))
		return None
	

	hits = []

	for rayPoint in RAYCAST_POINTS:
		hitCount = 0
		ray = elemCreateLine( vertex['p1'], rayPoint )

		for line in geomPoly:
			if ( hpos := elemIntersectsElemXY( line, ray ) ) != []:
				hitCount += 1

		# even result == outside, odd result == inside
		hits.append( hitCount % 2 )

	if hits[0] == hits[1] == hits[2]:

		# DEBUG ONLY
		print("RAYCAST RESULTS: ", hits )

		# if hitCount modulo 2 is 0, the point is outside
		if hits[0] == 0:
			return False
		else:
			return True
	else:
		print("ERR: geomCheckVertexInPoly: raycasting mismatch: ", hits )
		return None





#############################################################################
### toolReadTextFile
###
### Opens a text file and returns its contents in a list, line by line.
#############################################################################
def toolReadTextFile( fname ):
	lines = []
	try:
		fin = open( fname, 'r+t', encoding='UTF-8')
	except:
		print( "ERR: toolReadTextFile: unable to open file ", fname ) 
		return None

	if fin:
		with open( fname ) as fin:
			while True:
				line = fin.readline()
				if not line:
					break
				lines.append( line.rstrip() )
	
	return lines



#############################################################################
### toolCreateSimpleHeader
###
#############################################################################
def toolCreateSimpleHeader( fname=None ):
	head=[]


	if not toolFeedRateCheck():
		return ["(###)","(### ERROR: INVALID GCODE_OP_BFEED)", "(###)",""]


	if fname is not None:
		headFile = toolReadTextFile ( fname + '_start.nc' )
		if headFile:
			# check for magic names
			for i in range(len(headFile)):
				if '(GCODE_OP_BFEED)' in headFile[i]:
					# override immutable string
					headFile[i] = headFile[i].replace( '(GCODE_OP_BFEED)', str(GCODE_OP_BFEED) )

			return headFile

	for line in GCODE_PRG_START:
		if '(GCODE_OP_BFEED)' in line:
			# override immutable string
			line = line.replace( '(GCODE_OP_BFEED)', str(GCODE_OP_BFEED) )

		head.append(line)

	return head



#############################################################################
### toolCreateSimpleFooter
###
#############################################################################
def toolCreateSimpleFooter( fname=None ):
	foot=[]

	if fname is not None:
		headFile = toolReadTextFile ( fname + '_end.nc' )
		if headFile:
			# check for magic names
			for i in range(len(headFile)):
				if '(GCODE_OP_SAFEZ)' in headFile[i]:
					# override immutable string
					headFile[i] = headFile[i].replace( '(GCODE_OP_SAFEZ)', str(GCODE_OP_SAFEZ) )

			return headFile

	foot.append( '(END)' )

	for line in GCODE_PRG_END:
		if '(GCODE_OP_SAFEZ)' in line:
			# override immutable string
			line = line.replace( '(GCODE_OP_SAFEZ)', str(GCODE_OP_SAFEZ) )

		foot.append(line)

	return foot



#############################################################################
### toolRapidToNextPart
###
#############################################################################
def toolRapidToNextPart( part ):
	rap = []

	p1 = partGetFirstPosition(part)

	if p1 == None:
		print( "ERR: toolRapidToNextPart: part has no first point" )
		return []

	if 'name' in part:
		pname = part['name']
	else:
		pname = 'unnamed part'

	rap.append( '(rapid to: ' + pname + ')' )
	rap.append( GCODE_RAPID + ' Z' + str(GCODE_OP_SAFEZ) )
	rap.append( GCODE_RAPID + ' X' + format( p1[0], 'f' ) + ' Y' + format( p1[1], 'f' ) )
	rap.append( GCODE_RAPID + ' Z' + format( p1[2], 'f' ) )

	return rap

		

#############################################################################
### toolCreateFromPart
###
### Creates an toolpath (naked move commands) from a part.
#############################################################################
def toolCreateFromPart( part ):
	tops = []
	
	if not partCheckContinuous(part):
		print( "ERR: toolCreateFromPart: part \""+part['name']+"\" not continuous" )
		return []

	# If "partCheckContinuous" returned no error, it should (SHOULD!) be
	# ok to skip further tests concerning the geometry...
	part = partRenumber( part )
	
	if 'name' in part:
		tops.append('('+part['name']+')')
	else:
		tops.append('(unnamed part)')

	lastCmd = ''
	# TODO: Probably an error for arc creation.
	# The lastN storage shall correct the R-circles error that might be created
	# due to rounding errors with the 'format()' function.
	# Actually, this is a problem, because we already "somehow" moved
	# to this position, but we don't know where we are.
	# If the first moves are arcs or circles, we might run into trouble.

	# WARNING: These are strings!
	strLastX = None
	strLastY = None
	strLastZ = None
	for i in range( 1, len(part['elements']) + 1 ):
		el = partGetElement( part, i )
		if len(el) == 0:
			print( "ERR: toolCreateFromPart: partGetElement returned zero length at ", i )
			return[]
			
		# TOCHK (2021)
		if not 'type' in el:
			print( "ERR: toolCreateFromPart: element nr. ", i," has no \'type\' attribute" )
			return[]

		cxyz = ''

		# --- VERTEX ------------------------------------------------
		if el['type'] == 'v':
			if 'tMsg' in el:
				pStr = str( el['tMsg'] )
				if '(' in pStr or ')' in pStr:
					print( "INF: toolCreateFromPart: nested comment in 'tMsg'; ignoring: ", pStr )
					pStr = "ERROR IN tMsg: NESTED COMMENT"

				if len(pStr) == 0:
					pStr = "vertex with empty message"
				cxyz = '(' + pStr + ')'
				lastCmd = GCODE_COMMENT

			if 'tFeed' in el:
				if lastCmd == GCODE_COMMENT:
					cxyz += '\n'
				cxyz += '(FEEDRATE VERTEX FOUND: ' + str( el['tFeed'] ) + ')'
				lastCmd = GCODE_FEED
			else:
				# it's just a vertex; create a comment
				# maybe something useful can be added in the future
				cxyz = '(a wild vertex appears)'
				lastCmd = ''

		# --- LINE --------------------------------------------------
		if el['type'] == 'l':
			# process X, Y and Z actions, only if different
			if el['p1'][0] == el['p2'][0]:
				cx = ''
			else:
				# format() avoids exponents (was str() before)
				strLastX = format( el['p2'][0], 'f' )
				cx = 'X' + strLastX
			if el['p1'][1] == el['p2'][1]:
				cy = ''
			else:
				strLastY = format( el['p2'][1], 'f' )
				cy = 'Y' + strLastY
			if el['p1'][2] == el['p2'][2]:
				cz = ''
			else:
				strLastZ = format( el['p2'][2], 'f' )
				cz = 'Z' + strLastZ
			if lastCmd == GCODE_LINE:
				cc = ' '
			else:
				# NEW 9/2021: now with optional rapid moves, if 'tMove':EXTRA_MOVE_RAPID
				cc = GCODE_LINE 
				if 'tMove' in el:
					if el['tMove'] == EXTRA_MOVE_RAPID:
						cc = GCODE_RAPID
			cxyz = cc + ' ' + cx + ' ' + cy + ' ' + cz
			lastCmd = GCODE_LINE

		# --- ARC ---------------------------------------------------
		if el['type'] == 'a':
			if el['dir'] == 'cw':
				if lastCmd == GCODE_ARC_CW:
					cc = ' '
				else:
					cc = GCODE_ARC_CW
			else:
				if lastCmd == GCODE_ARC_CC:
					cc = ' '
				else:
					cc = GCODE_ARC_CC

			# avoids exponent in output (was str() before)
			strAx2 = format( el['p2'][0], 'f' )
			strAy2 = format( el['p2'][1], 'f' )
			strAz2 = format( el['p2'][2], 'f' )
			strAr2 = format( el['rad'],   'f' )

			# check if the rounding left us with a valid arc
			if strLastX is not None and strLastY is not None:
				# DEBUG
				# if strLastX == '0.027794':
				# 	qqq = None
				pDist = vecLengthXY(  ( float(strAx2), float(strAy2), 0 ), ( float(strLastX), float(strLastY), 0 )  )
				pDist = float( format( pDist, 'f') )
				# TODO: It might be better to multiply float(strAr2) with 2 instead of dividing pDist.
				# Gives a better result, because pDist/2 can again be off :-/
				if float(strAr2) < pDist / 2.0:
					nstrAr2 = format( pDist / 2.0, 'f' )
					print( "INF: toolCreateFromPart: corrected invalid arc R rounding:", strAr2, nstrAr2 )
					strAr2 = nstrAr2
			cx = 'X' + strAx2
			cy = 'Y' + strAy2
			cz = 'Z' + strAz2
			cr = 'R' + strAr2

			strLastX = strAx2
			strLastY = strAy2
			strLastZ = strAz2

			cxyz = cc + ' ' + cx + ' ' + cy + ' ' + cz + ' ' + cr
			if el['dir'] == 'cw':
				lastCmd = GCODE_ARC_CW
			else:
				lastCmd = GCODE_ARC_CC

		# --- ERROR -------------------------------------------------
		if cxyz == '':
			print( "ERR: toolCreateFromPart: empty nc-code line at: ", el )
			return[]
		
		tops.append( cxyz )

	return tops



#############################################################################
### toolFileCreate
###
### Writes the toolpath to a file.
#############################################################################
def toolFileWrite( tools, fname='ncEFI.nc', append=False ):

	if not isinstance( tools, list ):
		print( "ERR: toolFileWrite: 'tools' is not a list: ", type(tools) )
		return False

	try:
		f = open( fname, 'w+t' if append == False else 'a+t' )
	except:
		print( "ERR: toolFileWrite: unable to open file: ", fname )
		return False

	for tool in tools:
		f.write( tool + '\n' )

	f.close()
	return True



#############################################################################
### toolFileAppend
###
### Writes the toolpath to a file.
#############################################################################
def toolFileAppend( tools, fname='ncEFI.nc' ):
	return toolFileWrite( tools, fname, append=True)



#############################################################################
### toolFullAuto
###
### Creates a G-code file from a list of geometries, connecting them via
### rapid moves. Just here to save you some typing :)
### 'geoms' is a list of geometries; optionally, with 'names', a list of the
### same length as 'geoms', can be used to name the created parts. The items
### need to be strings.
### 'safeZ' is the safe Z travel height. If not specified, the default value
### will be used.
### The name of the G-code output file can be overriden with 'fname'.
#############################################################################
def toolFullAuto( geoms, feedRate=None, safeZ=None, names=None, fname='ncEFI.nc', fnameHeader=None ):

	global GCODE_OP_BFEED
	global GCODE_OP_SAFEZ


	if feedRate is None:
		feedRate = GCODE_OP_BFEED
	
	if safeZ is None:
		safeZ = GCODE_OP_SAFEZ

	# avoid overwriting files if someone swaps arguments
	forbiddenFileNames = ['ncEFI', 'ncVec', 'ncPRG', 'README', '.gitignore', 'testlol']
	if fname != 'ncEFI.nc':
		for n in forbiddenFileNames:
			if n in fname:
				print( "ERR: toolFullAuto: unsafe file name used: ", fname )
				return False

	if not isinstance( geoms, list ):
			print( "ERR: toolFullAuto: 'geoms' is not a list ", type(geoms) )
			return False
	
	if len(geoms) < 1:
		print( "ERR: toolFullAuto: 'geoms' is empty" )
		return False

	if names is not None:
		if len(names) != len(geoms):
			print( "WARNING: toolFullAuto: length of 'names' does not match length of 'geoms: ", len(geoms), len(names) )
			names = None

	if not isinstance( safeZ, (int, float, complex)) or isinstance(safeZ, bool):
		print( "ERR: toolFullAuto: 'safeZ' is not a number ", type(safeZ) )
		return False

	if not toolFeedRateCheck( feedRate ):
		print( "ERR: toolFullAuto: base feed rate is invalid: ", feedRate )
		return False

	# TODO: overriding this "should" [tm] be safe
	GCODE_OP_BFEED = feedRate

	if safeZ < 0:
		print( "WARNING: 'safeZ' is < 0: ", safeZ )

	# TODO: overriding this "should" [tm] be safe
	GCODE_OP_SAFEZ = safeZ

	# create parts
	parts = []
	n = 0
	for e in geoms:
		name = "no name"
		if names is not None:
			name = names[n]
			if not isinstance(name,str):
				print( "INF: toolFullAuto: 'names' contains other types than strings" )
				names = None
				name = "no name"
		parts.append( partCreate( name, e ) )

	# create tool path
	tool = []
	tool += toolCreateSimpleHeader( fnameHeader )
	for p in parts:
		tool += toolRapidToNextPart( p )
		tool += toolCreateFromPart( p )
	tool += toolCreateSimpleFooter( fnameHeader )

	toolFileWrite( tool, fname )



#############################################################################
### toolCalcFeedratePercentage
###
### Utility function to calculate feedrates relative to a base value.
### The parameter "strPercentage" must be an string, containing an integer
### or float value followed by a percentage sign.
### E.g. "50%", "70.34%", "200 %".
### In case of an error, None is returned.
### Leading and trailing spaces are ignored.
#############################################################################
def toolCalcFeedratePercentage( fBase, strPercentage ):
	
	if not isinstance( strPercentage, str ):
		print( "ERR: toolCalcFeedratePercentage: 'strPercentage' is not a string: ", type(strPercentage) )
		return None
	
	strWrk = strPercentage.strip()
	
	if len(strWrk) < 2:
		print( "ERR: toolCalcFeedratePercentage: string 'strPercentage' too short: ", strPercentage )
		return None

	if strWrk[-1] != '%':
		print( "ERR: toolCalcFeedratePercentage: 'strPercentage' does not contain a '%' sign as last digit: ", strWrk[-1] )
		return None

	try:
		val = float( strWrk.strip(" %") )
	except:
		print( "ERR: toolCalcFeedratePercentage: Error converting this to a float:", strPercentage.strip(" %") )
		return None

	return (fBase / 100.0) * val



#############################################################################
### toolFeedRateSet
###
### Sets the global base feed rate.
#############################################################################
def toolFeedRateSet( feedRate ):

	if toolFeedRateCheck( feedRate ):
		global GCODE_OP_BFEED
		GCODE_OP_BFEED = feedRate
		return True

	print( "ERR: toolFeedRateSet: error setting feed rate to: ", feedRate )
	return False



#############################################################################
### toolFeedRateCheck
###
### Checks if the given feed rate is set and valid.
### With empty arguments, the global feed rate is checked
#############################################################################
def toolFeedRateCheck( feedRate = None ):

	if feedRate is None:
		feedRate = GCODE_OP_BFEED

	if not isinstance( feedRate, int ):
		print( "ERR: toolFeedRateCheck: feed rate is not an integer: ", type(feedRate) )
		return False

	if feedRate < 1:
		print( "ERR: toolFeedRateCheck: feed rate is 0 or negative: ", feedRate )
		return False

	if feedRate < 100:
		print( "INF: toolFeedRateCheck: WARNING! LOW FEED RATE: ", feedRate )

	# TODO: do we need to check a max feed rate? if yes, what's the max value?
	if feedRate > 9999:
		print( "ERR: toolFeedRateCheck: feed rate is >9999: ", feedRate )
		return False
	
	return True



#############################################################################
### debugShowViewer
###
### Writes all elements to the standard output file 'ncEFI.dat' and
### calls the OpenGL debug view app.
#############################################################################
def debugShowViewer( llist ):
	f = open( 'ncEFI.dat', 'w+b' )
	pickle.dump( llist, f )
	f.close()

	# The original was "python", but failed on macOS (with a lot of MacPorts Python versions installed).
	# Something like "Python3" failed on Windoze, so let us just use the same executable with which
	# this here was launched.
	# os.system('python ncEFIDisp2.py ncEFI.dat')
	# os.system('python3 ncEFIDisp2.py ncEFI.dat')
	thisPython = sys.executable
	os.system( thisPython + ' ncEFIDisp2.py ncEFI.dat')
