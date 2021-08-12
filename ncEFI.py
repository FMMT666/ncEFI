#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ncEFI
# Some stupid G-Code ideas I had about 25 years ago.
# Yes, really, really stupid.
# FMMT666/ASkr 1995..2021 lol



# TODO (MAYBE):
#  - add geomCreateCircle    necessary at all? could use geomCreateSpiralHelix
#  - add geomCreateRect      necessary at all? better to create a general 3- or 4pt pocket milling option
# TODO:
#  - add geomCreateArcSlot
#  - add geomMoveTo; should be a 3-liner (theoretically :)
#  - add spiral pocket geom (using SpiralHelix and Circle)
#  - add retract movement or at least a "retractPt" to all the geom functions; last move to move the tool out
#  - split ncEFI into several files, maybe elem, geom, part, tool?
#  - change geomCreateConcentricCircles
#      - rename to geomCreateConcentricCirclesConnected
#      - add another approach to connect the circles via a spiral
#      - make use of the new geomCreateCircle() function
#  - whatever the 'basNr' parameter in some geom function shall do - it doesn't; purpose??


import sys
import math
import pickle
from random import random

from ncVec import *


GCODE_RAPID        = "G00"
GCODE_LINE         = "G01"
GCODE_ARC_CW       = "G02"
GCODE_ARC_CC       = "G03"

# TODO
# Just some stupid default values for now.
GCODE_PRG_FEEDUNIT = 'G94 (feedrate in \'units\' per minute)'
GCODE_PRG_UNITS    = 'G21 (units are millimeters)'
GCODE_PRG_PLANE    = 'G17 (working in/on xy-plane)'
GCODE_PRG_PATHMODE = 'G64P0.05 (LinuxCNC, continuous mode with \'p\' as tolerance)'
GCODE_PRG_INIT1    = 'T1M06'
GCODE_PRG_INIT2    = 'G00X0Y0 S6000 M03'
GCODE_PRG_INIT3    = 'F900'

GCODE_PRG_ENDPOS   = 'G00X0Y0'
GCODE_PRG_END      = 'M02'

GCODE_OP_SAVEZ     = '10'

TOOL_CONTINUOUS_TOLERANCE = 0.001    # in units; if mm, this makes 1um...



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



#############################################################################
### extraAddExtra
###
#############################################################################
def extraAddExtra(elem,extra):
	for i in extra:
		if i=='pNr':
			elem['pNr']=extra['pNr']
		if i=='pNext':
			elem['pNext']=extra['pNext']
		if i=='pPrev':
			elem['pPrev']=extra['pPrev']



#############################################################################
### elemCreateVertex
###
#############################################################################
def elemCreateVertex(p1,extra={}):
	if isinstance(p1,tuple) == False:
		return {}
	ret={'type':'v','p1':p1}
	extraAddExtra(ret,extra)
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
	extraAddExtra(ret,extra)
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
	extraAddExtra(ret,extra)
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
	extraAddExtra(ret,extra)
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
### elemCreateArc360
###
###
#############################################################################
def elemCreateArc360(p1,p2,rad,dir):
	pass



#############################################################################
### elemCreateCircle
###
###
#############################################################################
def elemCreateCircle(p1,rad,dir):
	pass



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
def partCreate(name, extras={}):
	if isinstance(name,str) == False:
		return {'name':"", 'type':'p'}
	if len(name)<1:
		return {'name':"", 'type':'p'}
	ret={'name':name,'type':'p', 'elements':[]}
	for i in extras:
		ret[i]=extras[i]
	return ret



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
#############################################################################
def partGetFreeNumber(part):
	nr=[]
	for i in part['elements']:
		if 'pNr' in i:
			nr.append(i['pNr'])
	nr.sort()
	return nr[len(nr)-1]+1

	

#############################################################################
### partAddElement
###
### number=0 -> auto numbering
### number<0 -> no numbering
#############################################################################
def partAddElement(part, elem, number=0):
	for i in part['elements']:
		if 'pNr' in i:
			if i['pNr'] == number:
				number=0
				continue
	nelem=elem
	if number == 0:
		nelem['pNr']=partGetFreeNumber(part)
	else:
		if number > 0:
			nelem['pNr']=number
	part['elements'].append(nelem)
	return part



#############################################################################
### partAddElements
###
#############################################################################
def partAddElements(part, elems):
	for i in elems:
		part=partAddElement(part,i,-1)
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
def partCheckUniqueNumbers(part):
	nrFound=[]
	for i in range(0,len(part['elements'])):
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
	li=[]
	for i in range(0,len(part['elements'])):
		li.append(part['elements'][i]['pNr'])
	li.sort()
	return li



#############################################################################
### partGetLastPositionFromElements
###
#############################################################################
def partGetLastPositionFromElements(elems):
	li=[]
	nr=0
	el={}
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
def partRenumber(part):
	if not partCheckUniqueNumbers(part):
		return part
	li=[]
	for i in range(0,len(part['elements'])):
		li.append([part['elements'][i]['pNr'],i])
	li.sort()
	for i in range(0,len(li)):
		part['elements'][li[i][1]]['pNr']=i+1
	return part



#############################################################################
### partSortByNumber
###
#############################################################################
def partSortByNumber(part):
	if not partCheckUniqueNumbers(part):
		return part
	li=[]
	for i in range(0,len(part['elements'])):
		li.append([part['elements'][i]['pNr'],i])
	li.sort()
	oldelems=part['elements']
	part['elements']=[]
	for i in range(0,len(li)):
		part=partAddElement(part,oldelems[li[i][1]],li[i][0])
	return part



def PartSortByGeometry(part):
	pass  



#############################################################################
### partCheckContinuous
###
#############################################################################
def partCheckContinuous(part):
	if not partCheckUniqueNumbers(part):
		return False
	li=partGetNumbers(part)
	if len(li) == 0:
		print( "ERR: partCheckContinuous: no elements in part!" )
		return False
	if len(li) == 1:
		return True
	e1=partGetElement(part,li[0])
	if e1['type']=='v':
		print( "ERR: partCheckContinuous: vertex found!" )
		return False
	for i in range(1,len(li)):
		e2=partGetElement(part,li[i])
		if e2['type']=='v':
			print( "ERR: partCheckContinuous: vertex found!" )
			return False
		if not e1['p2']==e2['p1']:
			ez=math.fabs(vecLength(e1['p2'],e2['p1']))
			if ez > TOOL_CONTINUOUS_TOLERANCE:
				print( "ERR: partCheckContinuous: p2!=p1 at number: ",i )
				print( "                        : e1['p2']: ",e1['p2'] )
				print( "                        : e2['p1']: ",e2['p1'] )
				return False
		e1=e2
	return True
		
	

#############################################################################
### partCheckClosed
###
#############################################################################
def partCheckClosed(part):
	if not partCheckContinuous(part):
		return False
	li=partGetNumbers(part)
	if len(li)<2:
		return False
	e1=partGetElement(part,li[0])
	e2=partGetElement(part,li[-1])
	if e1['type']=='v' or e2['type']=='v':
		return False
	if e2['p2']==e1['p1']:
		return True
	return False



#############################################################################
### geomCreateHelix
### 
### p1's position is the most left position on the helix (xy-plane).
### Endpoint is p1's (x,y)-position (z is depth).
### "depth" is positive for negative z-axis values (milling a hole usually
### is done by milling "down", not "up").
#############################################################################
def geomCreateHelix(p1,dia,depth,depthSteps,dir,basNr=0,finish='finish'):
	hel=[]
	if depth == 0.0:
		print( "ERR: geomCreateHelix: depth == 0" )
		return []
	if depthSteps < 1.0:
		print( "ERR: geomCreateHelix: steps < 0" )
		return []
	if dia <= 0.0:
		print( "ERR: geomCreateHelix: dia <= 0" )
		return []
	depthPerHalfRev=depth/(depthSteps*2.0)
	x1=p1[0]
	x2=p1[0]+dia
	p2=(x2,p1[1],p1[2]-depthPerHalfRev)
	if basNr==0:
		nr=1
	else:
		nr=basNr
	for i in range(0,depthSteps):
		el=elemCreateArc180(p1,p2,dia/2.0,dir,{'pNr':nr})
		nr+=1
		hel.append(el)
		p1=p2
		p2=(x1,p1[1],p1[2]-depthPerHalfRev)
		el=elemCreateArc180(p1,p2,dia/2.0,dir,{'pNr':nr})
		nr+=1
		hel.append(el)
		p1=p2
		if not i == depthSteps-1:
			p2=(x2,p1[1],p1[2]-depthPerHalfRev)
		else:
			p2=(x2,p1[1],p1[2])
	# end for all depthSteps

	if not len(hel)==depthSteps*2:
		print( "ERR: geomCreateHelix: skipped one or more arcs (helix)" )
		return[]

	if finish=='finish':
		el=elemCreateArc180(p1,p2,dia/2.0,dir,{'pNr':nr})
		nr+=1
		if el==[]:
			print( "ERR: geomCreateHelix: skipped first finishing arc" )
			return []
		hel.append(el)

		el=elemCreateArc180(p2,p1,dia/2.0,dir,{'pNr':nr})
		nr+=1
		if el==[]:
			print( "ERR: geomCreateHelix: skipped second finishing arc" )
			return []
		hel.append(el)
	# end if 'finish'

	return hel



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
### geomCreateConcentricCircles
###
### p1 is the left posistion of the beginnig circle
### If diaStart < diaEnd, the circular pocket is "milled" from the inside
### to the outside and vice versa.
### "diaSteps" determines the amount of steps (aka.: circles) which should
### be performed.
### If diaSep==1, a single circle, determined by "diaStart"'s diamenter is
### "milled".
#############################################################################
def geomCreateConcentricCircles(p1,diaStart,diaEnd,diaSteps,dir,basNr=0):
	con=[]
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
### geomCreateCircRingHole
###
### p1 defines the start position (middle) of the pocket. It's z-axis
### value is the start of the _milling_ operation (mill hits material).
### The helix is on top of this point!
#############################################################################
def geomCreateCircRingHole(p1,diaStart,diaEnd,diaSt,depth,depthSt,hDepth,hDepthSt,clear,dir,basNr=0):
	if depth <= 0.0:
		print( "ERR: geomCreateCircRingHole: depth <= 0 :",depth )
		return []
	if depthSt < 1:
		print( "ERR: geomCreateCircRingHole: depthSt < 1 :",depthSt )
		return []
	if hDepth < 0:
		print( "ERR: geomCreateCircRingHole: hDepth < 0 :",hDepth )
		return []
	if hDepthSt < 1:
		print( "ERR: geomCreateCircRingHole: hDepthSt < 1 :",hDepthSt )
		return []
	if clear < p1[2]:
		print( "ERR: geomCreateCircRingHole: clear < workpos :",clear,p1[2] )
		return []
	if diaStart <= 0:
		print( "ERR: geomCreateCircRingHole: diaStart < 0 :",diaStart )
		return []
	if diaEnd <= 0:
		print( "ERR: geomCreateCircRingHole: diaStart < 0 :",diaEnd )
		return []
	
	if basNr==0:
		nr=1
	else:
		nr=basNr

	ccrh=[]
	
	for i in range(0,depthSt):
		# starting point for helix
		pWork=(p1[0]-(diaStart/2.0),p1[1],p1[2]+hDepth-((i+1)*(depth/(depthSt*1.0))))
		hel=geomCreateHelix(pWork,diaStart,hDepth,hDepthSt  ,dir,nr,'nofinish')
		if hel==[]:
			print( "ERR: geomCreateCircRingHole: error creating helix" )
			return []
		# we are now on pWork(x,y) but already cut depth/depthSt of the material
		for j in hel:
			ccrh.append(j)
		nr+=len(hel)
	
		pWork=(p1[0]-(diaStart/2.0),p1[1],p1[2]-((i+1)*(depth/(depthSt*1.0))))
		poc=geomCreateConcentricCircles(pWork,diaStart,diaEnd,diaSt,dir,nr)
		if poc==[]:
			print( "ERR: geomCreateCircRingHole: error creating concentric circles" )
			return []
		# we are now on pWork(x,y), with i*(depth/depthSt) in reverse z-axis direction
		for j in poc:
			ccrh.append(j)
		nr+=len(poc)
		
		if i < depthSt-1:
			# now, "back" to the "next" helix
			pWork1=partGetLastPositionFromElements(poc)
			pWork2=(pWork1[0],pWork1[1],pWork1[2]+depth/(depthSt*1.0))
			lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
			nr+=1
			if lin==[]:
				print( "ERR: geomCreateCircRingHole: error creating helix back line 1 in: ",i )
				return []
			ccrh.append(lin)
			pWork1=pWork2
			pWork2=(p1[0]-(diaStart/2.0),p1[1],p1[2]+hDepth-((i+2)*(depth/(depthSt*1.0))))
			lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
			nr+=1
			if lin==[]:
				print( "ERR: geomCreateCircRingHole: error creating helix back line 2 in: ",i )
				return []
			ccrh.append(lin)
		else:
			# now, "back" to the starting point
			pWork1=partGetLastPositionFromElements(poc)
			pWork2=(pWork1[0],pWork1[1],pWork1[2]+(i+1)*(depth/(depthSt*1.0)))
			lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
			nr+=1
			if lin==[]:
				print( "ERR: geomCreateCircRingHole: error creating back line 1" )
				return []
			ccrh.append(lin)
			pWork1=pWork2
			pWork2=(p1[0]-(diaStart/2.0),p1[1],p1[2]+hDepth-((depth/(depthSt*1.0))))
			lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
			nr+=1
			if lin==[]:
				print( "ERR: geomCreateCircRingHole: error creating back line 2" )
				return []
			ccrh.append(lin)
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
	geom =  []

	if incStep < 0:
		print( "INF: geomCreateZigZag: inverted negative 'incStep' value" )
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
### geomCreateSlot
###
### Creates a single slot from startPt to endPt. The depth (if any) is
### calculated from the difference of endPt-StartPt depth. The max depth per
### cut can be specified by "depthPerMove". 
### If the z height of the end point is greater (more positive) than the
### starting point, the moves will be done up. Might only be useful for
### form endmills, e.g. a slot-mill, etc.
#############################################################################
def geomCreateSlotLine(startPt,endPt,depthPerMove,basNr=0):
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

	curDepth = startPt[2] - depthPerMove
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
			curDepth -= depthPerMove
			if curDepth < totDepth:
				curDepth = totDepth
		else:
			curDepth += depthPerMove
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
### geomCreateSimpleContour
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
### - dist has to negative (aka.: we follow the left side of the slots)
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

		
	if partCheckClosed(part) == True:
		op='Closed'
	else:
		op='notClosed'

#  con=geomTrimPointsStartToEnd(con,op)


	return con



#############################################################################
### geomCreateLeftContour
###
#############################################################################
def geomCreateLeftContour(part,dist,basNr=0):
	con=[]
	conNr=1
	conSkip=-1

	slo=geomCreateSlotContour(part,dist)
	
	if slo==[]:
		print( "ERR: geomCreateLeftContour: error while creating slot elements from part " )
		return []

	slo=geomExtractSlotDirVecs(slo)
	
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

			sdi=999999999999999.9
			eleCount=0
			eleTarget=None
			eleInt=None
			
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


	con=geomTrimPointsStartToEnd(con,partCheckClosed(part))

			
	return con



#############################################################################
### geomTranslate
###
### Moves a geometry  into the direction specified by a vector.
### Returns a new instance
#############################################################################
def geomTranslate( geom, vec ):
	# TODO: probably not necessary to copy the element here
	geomn=[]
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
def geomTrimPointsStartToEnd(elIn,isClosed='notClosed'):
	elOut=[]
	
	for i in elIn:
		elOut.append(i)

	maxLen=len(elOut)-1

	for i in range(maxLen):
		if 'p2' in elOut[i]:
			elOut[i+1]['p1']=elOut[i]['p2']
		else:
			elOut[i+1]['p1']=elOut[i]['p1']
		
	if isClosed != 'notClosed':
		if 'p2' in elOut[maxLen]:
			elOut[0]['p1']=elOut[maxLen]['p2']
		else:
			elOut[0]['p1']=elOut[maxLen]['p1']

	return elOut



#############################################################################
### toolCreateSimpleHeader
###
#############################################################################
def toolCreateSimpleHeader():
	head=[]
	head.append(GCODE_PRG_UNITS)
	head.append(GCODE_PRG_FEEDUNIT)
	head.append(GCODE_PRG_PATHMODE)
	head.append(GCODE_PRG_PLANE)
	head.append(GCODE_PRG_INIT1)
	head.append(GCODE_PRG_INIT2)
	head.append(GCODE_PRG_INIT3)
	return head


#############################################################################
### toolCreateSimpleFooter
###
#############################################################################
def toolCreateSimpleFooter():
	foot=[]
	foot.append('(rapid to endposition)')
	foot.append(GCODE_RAPID+'Z'+GCODE_OP_SAVEZ)
	foot.append(GCODE_PRG_ENDPOS)
	foot.append(GCODE_PRG_END)
	return foot



#############################################################################
### toolRapidToNextPart
###
#############################################################################
def toolRapidToNextPart(part):
	rap=[]

	p1=partGetFirstPosition(part)
	
	if p1==None:
		print( "ERR: toolRapidToNextPart: part has no first point" )
		return []
		
	if 'name' in part:
		pname=part['name']
	else:
		pname='unnamed part'

	rap.append('(rapid to: '+pname+')')
	rap.append(GCODE_RAPID+'Z'+GCODE_OP_SAVEZ)
	rap.append(GCODE_RAPID+'X'+str(p1[0])+'Y'+str(p1[1]))
	rap.append(GCODE_RAPID+'Z'+str(p1[2]))

	return rap

		

#############################################################################
### toolCreateFromPart
###
### Creates an toolpath (naked move commands) from a part.
###
#############################################################################
def toolCreateFromPart(part):
	tops=[]
	
	if not partCheckContinuous(part):
		print( "ERR: toolCreateFromPart: part \""+part['name']+"\" not continuous" )
		return []

	# If "partCheckContinuous" returned no error, it should (SHOULD!) be
	# ok to skip further tests concerning the geometry...
	part=partRenumber(part)
	
	if 'name' in part:
		tops.append('('+part['name']+')')
	else:
		tops.append('(unnamed part)')

	lastCmd=''
	for i in range(1,len(part['elements'])+1):
		el=partGetElement(part,i)
		if len(el)==0:
			print( "ERR: toolCreateFromPart: partGetElement returned zero length at ",i )
			return[]
			
		# TOCHK (2021)
		if not 'type' in el:
			print( "ERR: toolCreateFromPart: element nr. ",i," has no \'type\' attribute" )
			return[]

		cxyz=''
		if el['type']=='l':
			# process X, Y and Z actions, only if different
			if el['p1'][0]==el['p2'][0]:
				cx=''
			else:
				cx='X'+str(el['p2'][0])
			if el['p1'][1]==el['p2'][1]:
				cy=''
			else:
				cy='Y'+str(el['p2'][1])
			if el['p1'][2]==el['p2'][2]:
				cz=''
			else:
				cz='Z'+str(el['p2'][2])
			if lastCmd==GCODE_LINE:
				cc=' '
			else:
				cc=GCODE_LINE
			cxyz=cc+cx+cy+cz
			lastCmd=GCODE_LINE

		if el['type']=='a':
			if el['dir']=='cw':
				if lastCmd==GCODE_ARC_CW:
					cc=' '
				else:
					cc=GCODE_ARC_CW
			else:
				if lastCmd==GCODE_ARC_CC:
					cc=' '
				else:
					cc=GCODE_ARC_CC

			cx='X'+str(el['p2'][0])
			cy='Y'+str(el['p2'][1])
			cz='Z'+str(el['p2'][2])
			cr='R'+str(el['rad'])

			cxyz=cc+cx+cy+cz+cr
			if el['dir']=='cw':
				lastCmd=GCODE_ARC_CW
			else:
				lastCmd=GCODE_ARC_CC
			
		if cxyz == '':
			print( "ERR: toolCreateFromPart: empty nc-code line at: ",el )
			return[]
		
		tops.append(cxyz)

	return tops



#############################################################################
### debugShowViewer
###
### Writes all elements to the standard output file 'ncEFI.dat' and
### calls the OpenGL debug view app.
#############################################################################
def debugShowViewer( llist ):
	f=open('ncEFI.dat','w+b')
	pickle.dump(llist,f)
	f.close()
	import os
	os.system('python ncEFIDisp2.py ncEFI.dat')






e  = geomCreateSlotLine( (-20,-10,5), (50,30,-10), 4)
e += geomCreateSlotLine( (-50,-10,0), (-10,-10,-10), 0)

debugShowViewer( e )
sys.exit()



#---------------------------------------
# e = geomCreateZigZag( ( -50,-50, 0), (50, 50, 0), 5, False )
# e = geomRotateZ( e, 22.5 )
# e += geomCreateZigZag( ( -100,-90, 0), (100, -90, 0), 0, False )

# e += geomCreateZigZag( ( -100,-100, 0), (00, 00, 0), 5, False )
# e += geomCreateZigZag( (  0, 0 , 0), (100, 100,0), 5, False )
# e += geomCreateZigZag( ( 20, 10, 0), ( 10, 20, 0), 2, True )
# e += geomCreateZigZag( ( 50, 10, 0), ( 60,  0, 0), 2, True )
# e += geomCreateZigZag( ( 60, 30, 0), ( 50, 20, 0), 2, True )
# e += geomCreateZigZag( (-30, 10, 0), (-40, 20, 0), 2, True )
# e += geomCreateZigZag( (-20, 10, 0), (-10, 20, 0), 2, True )
# e += geomCreateZigZag( (-50, 10, 0), (-60,  0, 0), 2, True )
# e += geomCreateZigZag( (-60, 30, 0), (-50, 20, 0), 2, True )
# e += geomCreateZigZag( (-30,-10, 0), (-40,-20, 0), 2, True )
# e += geomCreateZigZag( (-20,-10, 0), (-10,-20, 0), 2, True )
# e += geomCreateZigZag( (-50,-10, 0), (-60,  0, 0), 2, True )
# e += geomCreateZigZag( (-60,-30, 0), (-50,-20, 0), 2, True )
# e += geomCreateZigZag( ( 30,-10, 0), ( 40,-20, 0), 2, True )
# e += geomCreateZigZag( ( 20,-10, 0), ( 10,-20, 0), 2, True )
# e += geomCreateZigZag( ( 50,-10, 0), ( 60,  0, 0), 2, True )
# e += geomCreateZigZag( ( 60,-30, 0), ( 50,-20, 0), 2, True )

# debugShowViewer( e )
# sys.exit()


#---------------------------------------
#e  = geomCreateSpiralHelix( ( 0, 0, 0), (50,0,0), -5, 0, 10, 'cc', maxGrad=90, stopAtZero=False )
#debugShowViewer( e )
#sys.exit()



# e  = geomCreateSpiralHelix( (-50,-50,0), (10,0,0), 5, -4, 10, 'cc', maxGrad=120, stopAtZero=False )
# e += geomCreateSpiralHelix( (-50, 50,0), (10,0,0), 0, -4, 10, 'cc', maxGrad=120, stopAtZero=False )
# e += geomCreateSpiralHelix( ( 50, 50,0), (10,0,0), 5, -4, 10, 'cc', maxGrad=3, stopAtZero=False )
# e += geomCreateSpiralHelix( ( 50,-50,0), (10,0,0), 0, -4, 10, 'cc', maxGrad=3, stopAtZero=False )
# e += geomCreateSpiralHelix( ( 50,-50,0), (30,-50,0), 0, -4, 10, 'cc', maxGrad=3, startPtIsAbs=True, stopAtZero=False )
# debugShowViewer( e )
# sys.exit()




#---------------------------------------
# e = geomCreateSpiralHelix( (-10,-10,0), (10,0,0), 5, -1, 10, 'cc', stopAtZero=False )
# debugShowViewer( e )
# sys.exit()




#---------------------------------------
# vec = ( 20,0,0 )
# e = elemCreateVertex( vec )
# llist = [ e ]
# hStep = 0.0
# for i in range(0,100,2):
# 	vec = ( vec[0], vec[1], -i )
# 	vecMid = vecRotateZ( vec, math.radians( -(i+1)*22.5) )
# #	vecMid = vecScale( vecMid, 1 + hStep )
# #	hStep += 1
# 	vecEnd = vecRotateZ( vec, math.radians( -(i+1)*45.0) )
# 	vecEnd = vecScale( vecEnd, 1 + hStep )
# 	hStep += 0.01
# 	e = elemCreateArc180by3PtsTo( e, vecEnd, vecMid, 'cc' ) 
# 	llist.append( e )
# debugShowViewer( llist )
# sys.exit()



#---------------------------------------
# vec = ( 20,0,0 )
# e = elemCreateVertex( vec )
# llist = [ e ]
# for i in range(10):
# 	e = elemCreateLineTo( e, vecRotateZ(  vec, math.radians( -(i+1)*22.5) )  )
# 	llist.append( e )
# debugShowViewer( llist )
# sys.exit()





#---------------------------------------
# llist = []
# for i in range(1000000):
# 	x = random() * 20 + 10
# 	y = random() * 20 
# 	pt = (x,y,0)
# 	if arcHasPoint( (20,10,0), 5, pt ):
# 		llist.append( elemCreateVertex( pt ) )
# debugShowViewer( llist )
# sys.exit()




#---------------------------------------
# llist = []
# for i in range(10000):
# 	x = random() * 200 - 100
# 	y = random() * 200 - 100
# 	pt = (x,y,0)
# 	cp = vecHasPointLeftOrRight( (-50,30,0) ,(-30,-10,0),pt)
# 	if cp < 0:
# 		llist.append( elemCreateVertex( pt ) )
# debugShowViewer( llist )
# sys.exit()






#---------------------------------------
# llist = []
# p1 = ( 2,1,0)
# p2 = ( 4,3,0)
# p3 = ( 3,5,0)
# c1 = elemCreateArc180by3Pts( p1, p3, p2, 'cc' )
# p1 = elemCreateVertex( p1 )
# p2 = elemCreateVertex( p2 )
# p3 = elemCreateVertex( p3 )
# llist.append( [p1, p2, p3, c1 ] )
# debugShowViewer( llist )
# sys.exit()









#---------------------------------------
# llist = []
# for x in range(7):
# 	for y in range(7):
# 		p1 = ( random()*60-30 - 100+200/6*x, random()*60-30 - 100+200/6*y, 0 )
# 		p2 = ( random()*60-30 - 100+200/6*x, random()*60-30 - 100+200/6*y, 0 )
# 		p3 = ( random()*60-30 - 100+200/6*x, random()*60-30 - 100+200/6*y, 0 )
# 		if random() > 0.5:
# 			c1 = elemCreateArc180by3Pts( p1, p2, p3, 'cc')
# 			c2 = elemCreateArc180by3Pts( p1, p3, p2, 'cc')
# 			c3 = elemCreateArc180by3Pts( p2, p1, p3, 'cc')
# 			c4 = elemCreateArc180by3Pts( p2, p3, p1, 'cc')
# 			c5 = elemCreateArc180by3Pts( p3, p1, p2, 'cc')
# 			c6 = elemCreateArc180by3Pts( p3, p2, p1, 'cc')
# 		else:
# 			c1 = elemCreateArc180by3Pts( p1, p2, p3, 'cw')
# 			c2 = elemCreateArc180by3Pts( p1, p3, p2, 'cw')
# 			c3 = elemCreateArc180by3Pts( p2, p1, p3, 'cw')
# 			c4 = elemCreateArc180by3Pts( p2, p3, p1, 'cw')
# 			c5 = elemCreateArc180by3Pts( p3, p1, p2, 'cw')
# 			c6 = elemCreateArc180by3Pts( p3, p2, p1, 'cw')
# 		p1 = elemCreateVertex( p1 )
# 		p2 = elemCreateVertex( p2 )
# 		p3 = elemCreateVertex( p3 )
# 		llist.append( [p1, p2, p3, c1, c2, c3, c4, c5, c6 ] )
# debugShowViewer( llist )
# sys.exit()



#---------------------------------------
# cc1 = geomCreateConcentricCircles( (-5,0,0),  10,50,5, 'cc')
# debugShowViewer( [cc1] )
# sys.exit(0)



#---------------------------------------
# from random import randint
# from random import random
# llist=[]
# p1 = partCreate('Hole')
# # def geomCreateCircRingHole(p1,diaStart,diaEnd,diaSt,depth,depthSt,hDepth,hDepthSt,clear,dir,basNr=0):
# p1 = partAddElements( p1, geomCreateCircRingHole( (20,25,0), 20,30,3,   10,3,  20,2,5, 'cw')  )
# for i in range(6):
# #	llist.append(  partTranslate(p1, (-100 + i*30,-50,0))  )
# #	llist.append(  partRotateZ(p1, 360/5 * i)  )
# 	llist.append(  partRotateZAt(p1, 360/5 * i, (-10,-15,0 ) )  )
# partlist = llist
# f=open('ncEFI.dat','w+b')
# pickle.dump(partlist,f)
# f.close()
# import os
# os.system('python ncEFIDisp2.py ncEFI.dat')
# sys.exit(0)






#---------------------------------------
# from random import randint
# from random import random
# llist=[]
# g1 = geomCreateHelix( (0,0,0),5, 10, 5, 'cw', 0, 'nofinish' )
# g1 = geomCreateCircRingHole( (10,0,0), 10, 30, 3, 10, 1, 10, 5, 0, 'cc')
# for n in range(6):
# 	gn = geomRotateZAt( g1, n, (50,30,0))
# 	llist.append( gn )
# partlist = llist
# f=open('ncEFI.dat','w+b')
# pickle.dump(partlist,f)
# f.close()
# import os
# os.system('python ncEFIDisp2.py ncEFI.dat')
# sys.exit(0)



#---------------------------------------
# from random import randint
# from random import random
# llist=[]
# for x in range(-10,11):
# 	for y in range(-10,11):
# 		dia = randint(1,7)
# 		llist.append( geomCreateHelix( (x*10-dia/2.0,y*10,0),dia,randint(1,30),randint(1,10),'cw',0,'nofinish') )
# partlist = llist
# f=open('ncEFI.dat','w+b')
# pickle.dump(partlist,f)
# f.close()
# import os
# os.system('python ncEFIDisp2.py ncEFI.dat')
# sys.exit(0)


#---------------------------------------
# from random import randint
# from random import random
# p1 = partCreate("holes")
# for x in range(-10,11):
# 	for y in range(-10,11):
# 		dia = randint(1,7)
# 		p1 = partAddElements(p1, geomCreateHelix( (x*10-dia/2.0,y*10,0),dia,randint(1,30),randint(1,10),'cw',0,'nofinish') )
# partlist = [ p1 ]
# f=open('ncEFI.dat','w+b')
# pickle.dump(partlist,f)
# f.close()
# import os
# os.system('python ncEFIDisp2.py ncEFI.dat')
# sys.exit(0)



#---------------------------------------
# g1 = geomCreateCircRingHole( (0,0,0), 10, 30, 3, 10, 1, 10, 5, 0, 'cc')
# partlist = g1
# f=open('ncEFI.dat','w+b')
# pickle.dump(partlist,f)
# f.close()
# import os
# os.system('python ncEFIDisp2.py ncEFI.dat')
# sys.exit(0)




#---------------------------------------
# e1 = elemCreateLine( (10,0,0), (20,0,0) )
# e1 = elemCreateArc180( (20,0,0), (25,-5,0), 0, 'cw' )
# e1 = elemCreateVertex( (10,0,0) )
# llist=[]
# from random import randint
# from random import random
# n = 0
# for x in range(-10,11):
# 	for y in range(-10,11):
# #		for z in range(-10,0):
# 		z = 0
# 		llist.append( elemMoveTo(    elemRotateZ( e1, random()*math.pi*2.0 ),    (10*x,10*y,10*z), 'p1p2' )    )
# partlist = llist
# f=open('ncEFI.dat','w+b')
# pickle.dump(partlist,f)
# f.close()
# import os
# os.system('python ncEFIDisp2.py ncEFI.dat')
# sys.exit(0)



#---------------------------------------
# l1 = elemCreateLine((0,0,0), (50,50,0))
# a1 = elemCreateArc180To(l1,vecAdd((50,50,0),vecRotateZ((10,0,0),math.pi/4) ),0,'cw')
# l2 = elemTranslate( elemCopy(l1), vecRotateZ((10,0,0),math.pi/4) )
# l2 = elemReverse(l2)
# p1=partCreate('pups')
# p1=partAddElement(p1,l1,1)
# p1=partAddElement(p1,a1,2)
# p1=partAddElement(p1,l2,3)
# f=open('ncEFI.nc','w+t')
# for i in toolCreateSimpleHeader():
# 	f.write(i+'\n')
# for i in toolRapidToNextPart(p1):
# 	f.write(i+'\n')
# for i in toolCreateFromPart(p1):
# 	f.write(i+'\n')
# for i in toolCreateSimpleFooter():
# 	f.write(i+'\n')
# f.close()
# partlist=[p1]
# f=open('ncEFI.dat','w+b')
# pickle.dump(partlist,f)
# f.close()

# import os
# os.system('python ncEFIDisp2.py ncEFI.dat')

# sys.exit(0)


#---------------------------------------
l1=elemCreateLine((-10,-10,0),   (100,-10,0))
l2=elemCreateLine((100,-10,0), (130,60,0))
l3=elemCreateLine((130,60,0),(-50,30,0))
a1=elemCreateArc180((-50,30,0),(-60,-20,0),30,'cw')
a2=elemCreateArc180((-60,-20,0),(-30,10,0),50,'cw')
l4=elemCreateLine((-30,10,0),  (-10,-10,0))


#a1=elemCreateArc180((0,0,0),(50,0,0),40,'cw')
l01=elemCreateLine((0,0,0),(20,0,0))
l02=elemCreateLine((20,0,0),(20,-15,0))
l03=elemCreateLine((20,-15,0),(35,-15,0))
l04=elemCreateLine((35,-15,0),(35,0,0))
l05=elemCreateLine((35,0,0),(50,0,0))

l1=elemCreateLine((50,0,0),   (0,50,0))
a2=elemCreateArc180((0,50,0),(-50,30,0),40,'cc')
l2=elemCreateLine((-50,30,0),   (0,0,0))


p1=partCreate('pups')

p1=partAddElement(p1,l01,1)
p1=partAddElement(p1,l02,2)
p1=partAddElement(p1,l03,3)
p1=partAddElement(p1,l04,4)
p1=partAddElement(p1,l05,5)

p1=partAddElement(p1,l1,6)
p1=partAddElement(p1,a2,10)
p1=partAddElement(p1,l2,11)

a1=elemCreateArc180((0,0,0),(30,0,20),15,'cw')
a2=elemCreateArc180((30,0,20),(0,0,40),15,'cw')
a3=elemCreateArc180((0,0,40),(30,0,60),15,'cw')
a4=elemCreateArc180((30,0,60),(0,0,80),15,'cw')

p2=partCreate('pansen')
p2=partAddElement(p2,a1,1)
p2=partAddElement(p2,a2,2)
p2=partAddElement(p2,a3,3)
p2=partAddElement(p2,a4,4)


h1=geomCreateHelix((50,50,0),5,10,10,'cw',0,'nofinish')
p3=partCreate('helix')
p3=partAddElements(p3,h1)


c1=geomCreateConcentricCircles((0,0,0),30,10,5,'cc')
p4=partCreate('Concentric')
p4=partAddElements(p4,c1)


h1=geomCreateCircRingHole((0,0,0),1,50,49,5,3,2,2,5,'cw')


p5=partCreate('Hole')
p5=partAddElements(p5,geomCreateCircRingHole((0,0,0),20.0,20.0,1.0,5,3,2,2,5,'cw'))

p6=partCreate('Hole2')
p6=partAddElements(p6,geomCreateCircRingHole((100,0,0),1,10,9,5,3,2,2,5,'cc'))

p7=partCreate('Hole3')
p7=partAddElements(p7,geomCreateCircRingHole((100,50,0),10,1,9,5,3,2,2,5,'cw'))

p8=partCreate('Hole4')
p8=partAddElements(p8,geomCreateCircRingHole((0,50,0),1,10,9,5,3,2,2,5,'cw'))




#f=open('debug.log','w+t')
#for i in p5['elements']:
#  f.write(str(i)+'\n')
#f.close()



f=open('ncEFI.nc','w+t')
for i in toolCreateSimpleHeader():
	f.write(i+'\n')


for i in toolRapidToNextPart(p1):
	f.write(i+'\n')
for i in toolCreateFromPart(p1):
	f.write(i+'\n')

for i in toolRapidToNextPart(p6):
	f.write(i+'\n')
for i in toolCreateFromPart(p6):
	f.write(i+'\n')

for i in toolRapidToNextPart(p7):
	f.write(i+'\n')
for i in toolCreateFromPart(p7):
	f.write(i+'\n')

for i in toolRapidToNextPart(p8):
	f.write(i+'\n')
for i in toolCreateFromPart(p8):
	f.write(i+'\n')

for i in toolRapidToNextPart(p1):
	f.write(i+'\n')
for i in toolCreateFromPart(p1):
	f.write(i+'\n')

	
for i in toolCreateSimpleFooter():
	f.write(i+'\n')

f.close()

print( "p1 closed :",partCheckClosed(p1) )

p10=partCreate('PupsContour')
e10=geomCreateContour(p1,-5.0)
p10=partAddElements(p10,e10)

p20=partCreate('PupsSlot')
e20=geomCreateSlotContour(p1,-3.0)
p20=partAddElements(p20,e20)

#for i in range(1,len(p1['elements'])):
#  e1=partGetElement(p1,i)
#  e2=partGetElement(p1,i+1)
#  if e1 == [] or e2 == []:
#    break
#  ips=elemIntersectsElemXY(e1,e2)
#  print( "i: ",i," -> ",ips )
	

#cc1=geomCreateLeftContour(p1,-5.0)
#cc1=geomTrimPointsStartToEnd(cc1,'Closed')
#p50=partCreate('PupsContour1')
#p50=partAddElements(p50,cc1)
#cc2=geomCreateLeftContour(p50,-5.0)
#p51=partCreate('PupsContour2')
#p51=partAddElements(p51,cc2)


ss1=geomCreateSlotContour(p1,-5)
ss1=geomExtractSlotDirVecs(ss1)
p60=partCreate('SlotControl')
p60=partAddElements(p60,ss1)


ss2=geomCreateLeftContour(p1,-5.0)
p61=partCreate('LeftContour1')
p61=partAddElements(p61,ss2)

ss3=geomCreateLeftContour(p61,-5.0)
p62=partCreate('LeftContour2')
p62=partAddElements(p62,ss3)

ss4=geomCreateSlotContour(p61,-5.0)
ss4=geomExtractSlotDirVecs(ss4)
p63=partCreate('SlotControl61')
p63=partAddElements(p63,ss4)


partlist=[p1,p61,p62]

f=open('ncEFI.dat','w+b')
pickle.dump(partlist,f)
f.close()

print( "SLOT CONTOUR:" )
for i in p62['elements']:
	print( i )

import os
os.system('python ncEFIDisp2.py ncEFI.dat')

sys.exit(0)

