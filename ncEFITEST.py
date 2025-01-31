#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncEFI import *



#---------------------------------------
llist = []

# back to the original plan, the offset development (which benefits from having the color cycling)

# lstPts = [ (-40,-40,0), (-3,-2,0),(40,-40,0),(40,40,0),(3,2,0),(-60,10,0),(-78,2,0),(-80,0,0),(-78,-2,0)  ]
# lstPts = [ (-40,-40,0), (-3,-3,0),(40,-40,0),(45,-40,0),(48,20,0),(40,20,0),(2,2,0),(-60,10,0),(-78,2,0),(-80,0,0),(-78,-2,0)  ]
lstPts = [ (-40,-40,0), (-10,-1,0),(40,-40,0),(45,-40,0),(48,20,0),(40,20,0),(2,2,0),(-60,10,0),(-78,2,0),(-80,0,0),(-78,-2,0)  ]


myPart = partCreate( name = "Hupe" )
# WARNING THIS NOW RETURNS A LIST WITH LISTS FOR BETTER VISIBILITY
# DO NOT USE APPEND TO ADD TO LLIST
gPOff1 = geomCreatePolyOffset( geomCreatePoly( geomCreatePolyVerts( lstPts ) ), -5 )
for lstElem in gPOff1:
	for i in lstElem:
		partAddElement( myPart, i )

partRename( myPart, "ColorMe" )


llist.append( myPart )

debugShowViewer( llist )




#---------------------------------------
# Some tests for the new "no default instance copy" part translate/rotate function.
# llist=[]
# p1 = partCreate('Hole')
# p1 = partAddElements( p1, geomCreateCircRingHole( (30,30,0), 20,30,3,   10,3,  20,2,5, 'cw')  )

# # part functions to test:
# #  - partCopy
# #  - partTranslate
# #  - partRotateZ
# #  - partRotateZAt

# # p1a = partTranslate( p1, (-30,0,0) )             # p1a is just a reference to p1; p1 gets modified
# # p1b = partTranslate( p1, (-30,0,0), copy=True )  # p1b is a true copy; no changes to p1
# # print( p1a == p1, p1b == p1 )

# # p1a = partRotateZ( p1, 45 )                      # p1a is just a reference to p1; p1 gets modified
# # p1b = partRotateZ( p1, 45, copy=True )           # p1b is a true copy; no changes to p1
# # print( p1a == p1, p1b == p1 )

# p1a = partRotateZAt( p1, 45, (-50,0,0) )                      # p1a is just a reference to p1; p1 gets modified
# p1b = partRotateZAt( p1, 45, (-50,0,0), copy=True )           # p1b is a true copy; no changes to p1
# print( p1a == p1, p1b == p1 )

# # also test this on the fly
# partAddColor( p1,  (1,0,0) )
# partAddColor( p1b, (0,1,0) )
# partAddSize( p1,  3 )


# # keep in mind that this here is only a visualization of the current state of the parts
# llist.append( p1  )
# llist.append( p1a ) # will be this of course creates anothercreates
# llist.append( p1b )


# p1z = partCopy( p1a )
# p1z = partTranslate( p1z, (-40,0,0) )
# p1z = partDeleteColor(p1z)
# p1z = partAddRandomElementColors( p1z )
# p1z = partRename( p1z, "ColorMe" )
# llist.append( p1z )

# debugShowViewer( llist )
# sys.exit(0)




#---------------------------------------
# COPIED FROM BELOW TO TEST IF THE PART SYSTEM IS STILL WORKING
# llist=[]
# p1 = partCreate('Hole')
# # def geomCreateCircRingHole(p1,diaStart,diaEnd,diaSt,depth,depthSt,hDepth,hDepthSt,clear,dir,basNr=0):
# p1 = partAddElements( p1, geomCreateCircRingHole( (20,25,0), 20,30,3,   10,3,  20,2,5, 'cw')  )
# for i in range(6):
# #	llist.append(  partTranslate(p1, (-100 + i*30,-50,0))  )
# #	llist.append(  partRotateZ(p1, 360/5 * i)  )

# 	# Some tests with the new "no instance" translate/rotate function.
# 	# Appending without copying to the list will of course always create a new entry,
# 	# but even after that, modifications to the original (if the variable is still available)
# 	# WILL affect the appended part, as the elements are not truly copied, but just referenced (by Python itself).

# 	# llist.append(  partRotateZAt(p1, 360/5 * i, (-10,-15,0 ), copy = False )  )
# 	# partRotateZAt( p1, 360/5 * i, (-10,-15,0 ) )
# 	# llist.append( p1 )

# 	# p1 = partRotateZAt( p1, 360.0/5, (-10,-15,0 ), copy=True )
# 	p1 = partRotateZAt( p1, 30, (-10,-15,0 ), copy=True )
# 	llist.append( p1 )


# debugShowViewer( llist )
# tool = []
# for part in llist:
# 	tool += toolRapidToNextPart( part )
# 	tool += toolCreateFromPart( part )
# toolFileWrite( tool )
# sys.exit(0)






#---------------------------------------
# llist = []

# # lstPts = [ (-40,-40,0), (-3,-2,0),(40,-40,0),(40,40,0),(3,2,0),(-60,10,0),(-78,2,0),(-80,0,0),(-78,-2,0)  ]
# # lstPts = [ (-40,-40,0), (-3,-3,0),(40,-40,0),(45,-40,0),(48,20,0),(40,20,0),(2,2,0),(-60,10,0),(-78,2,0),(-80,0,0),(-78,-2,0)  ]
# lstPts = [ (-40,-40,0), (-10,-1,0),(40,-40,0),(45,-40,0),(48,20,0),(40,20,0),(2,2,0),(-60,10,0),(-78,2,0),(-80,0,0),(-78,-2,0)  ]


# myPart = partCreate( name = "Hupe" )
# # WARNING THIS NOW RETURNS A LIST WITH LISTS FOR BETTER VISIBILITY
# # DO NOT USE APPEND TO ADD TO LLIST
# gPOff1 = geomCreatePolyOffset( geomCreatePoly( geomCreatePolyVerts( lstPts ) ), -5 )
# for lstElem in gPOff1:
# 	for i in lstElem:
# 		partAddElements( myPart, i )



# llist.append( myPart )

# debugShowViewer( llist )




#---------------------------------------
# TEST line to line distance in 3D space with debug output
# llist = []
# debug_list = []
# line = elemCreateLine((-50,-30,-30), (70,50,30))
# llist.append(line)

# import random

# vList = []
# for i in range(3000):  # Reduziert von 3000
# 	p = (random.uniform(-30, 30), random.uniform(-30, 30), random.uniform(-30, 30))
# 	vList.append(elemCreateVertex(p))

# # Test mit Debug-Ausgaben
# for i in range(4000):  # Reduziert von 4000
# 	l = elemCreateLineBetween(random.choice(vList), random.choice(vList))
# 	if l != {}:
# 		dist = elemDistance(l, line)
# 		if dist > 10:
# 			llist.append(l)
# 			# Debug für Endpunktdistanzen
# 			ep_dist = min(
# 				elemDistance( elemCreateVertex(l['p1']), line ),
# 				elemDistance( elemCreateVertex(l['p2']), line )
# 			)

# 			if ep_dist < 10:
# 				print( "Wrong distance: ", ep_dist)
# 				print( "line: ", l )

# debugShowViewer(llist)





#---------------------------------------
# TEST line to line distance in 3D space
# llist = []
# # line = elemCreateLine( (-50,-30,0), (70,50,0) )
# line = elemCreateLine( (-50,-30,-30), (70,50,30) )

# llist.append( line )

# import random

# # create a list of randomly placed vertices
# vList = []
# for i in range(3000):
# 	# p = (random.uniform(-100, 100), random.uniform(-100, 100), 0 )
# 	p = (random.uniform(-30, 30), random.uniform(-30, 30), random.uniform(-30, 30) )
# 	vList.append( elemCreateVertex( p ) )

# # create test-lines between randomly selected point
# for i in range(4000):
# 	l = elemCreateLineBetween( random.choice(vList), random.choice(vList) )
# 	if l != {} and elemDistance( l, line ) > 10:
# 		llist.append( l )

# debugShowViewer( llist )



#---------------------------------------
# TEST vertex to line distance in 3D space
# llist = []
# # line = elemCreateLine( (-50,-30,0), (70,50,0) )
# line = elemCreateLine( (-50,-30,-30), (70,50,30) )

# llist.append( line )

# import random

# for i in range(5000):
# 	# p = (random.uniform(-100, 100), random.uniform(-100, 100), 0 )
# 	p = (random.uniform(-30, 30), random.uniform(-30, 30), random.uniform(-30, 30) )
# 	v = elemCreateVertex( p )

# 	if elemDistance( line, v ) > 10:
# 		llist.append( v )


# debugShowViewer( llist )




#---------------------------------------
# llist = []

# lstPts = [ (-40,-40,0), (-3,-2,0),(40,-40,0),(40,40,0),(3,2,0),(-60,10,0),(-78,2,0),(-80,0,0),(-78,-2,0)  ]


# gPOff1 = geomCreatePolyOffset( geomCreatePoly( geomCreatePolyVerts( lstPts ) ), -5 )


# llist += gPOff1


# debugShowViewer( llist )





#---------------------------------------
# llist = []

# lstPts = [ (-40,-40,0), (-3,-2,0),(40,-40,0),(40,40,0),(3,2,0),(-60,10,0),(-78,2,0),(-80,0,0),(-78,-2,0)  ]
# llist += ( gP1 := geomCreatePoly( gV := geomCreatePolyVerts( lstPts ) ) )

# #llist += (gO := geomCreatePolyVertsOffset( gV, -2 ))
# llist += (gO := geomCreatePolyVertsOffset( gV, -5 ))
# #llist += (gO := geomCreatePolyVertsOffset( gV, -15 ))
# llist += geomCreatePoly( gO )

# geomCheckPointInPoly( elemCreateVertex( ( 0, 0, 0) ), gP1 )
# geomCheckPointInPoly( elemCreateVertex( (10,10, 0) ), gP1 )

# debugShowViewer( llist )





#---------------------------------------
# llist = []
# # VERTSOFFSET WAS CHANGED TO ACCEPT A GEOM OF VERTS, NOT JUST A LIST OF POINTS ANYMORE
# # OLD llist.append( geomCreatePolyVertsOffset( [ (-10,-10,0), (30,-20,0),(40,50,0),(-30,20,0)  ], -5 ) )
# # OLD llist.append( geomCreatePolyVertsOffset( [ (-5,-10,0), (0,-20,0),(40,50,0),(-10,0,0)  ], -5 ) )
# # OLD llist.append( geomCreatePolyVertsOffset( [ (0,0,0), (50,0,0),(0,10,0),(0,5,0) ], -2 ) )
# # OLD llist.append( geomCreatePolyVertsOffset( [ (0,0,0), (50,0,0),(0,10,0),(2.5,5,0) ], -2 ) )
# # OLD llist.append( geomCreatePolyVertsOffset( [ (-5,-10,0), (0,-20,0),(40,50,0),(-10,0,0)  ], 5 ) )

# lstPts = [ (-40,-40,0), (0,-10,0),(40,-40,0),(40,40,0),(0,10,0),(-40,40,0)  ]

# OLD gV1 = geomCreatePolyVertsOffset( lstPts, -5 )
# OLD gV2 = geomCreatePolyVertsOffset( lstPts, 5 )

# OLD gV0a = geomCreatePolyVertsOffset( lstPts, 0 )
# OLD gV0a = geomTranslate( gV0a, (0,0,10) )
# gV0b = geomCreatePolyVerts( lstPts )

# gPi = geomCreatePoly( gV1 )
# gPo = geomCreatePoly( gV2 )
# gPO = geomCreatePoly( gP1 )

# llist += gP1 + gV1 + gV2 + gV0a + gV0b + gPi + gPo + gPO


# debugShowViewer( llist )




#---------------------------------------
# llist = []
# llist.append( geomCreateSlotPoly( [(-90,0,0), (-80,10,0), (-50,0,-10)], 2, smoothEnter=False ) )
# llist.append( geomCreateSlotPoly( [(-30,0,0), (-10,10,0), (10,-10,0), (30,0,-10)], 4, smoothEnter=True ) )
# llist.append( geomCreateSlotPoly( [(40,60,0), (80,60,0), (80,20,0), (40,20,0),(40,60,-15)], 5, smoothEnter=True ) )
# llist.append( geomCreateSlotPoly( [(40, 0,0), (80, 0,0), (80,-40,0), (40,-40,0),(40, 0,-15)], 5, smoothEnter=False ) )
# llist.append( geomCreateSlotPoly( [(-50, -50,0), (50, -50, -20)], 5, smoothEnter=False ) )
# llist.append( geomCreateSlotPoly( [(-50, -80,0), (50, -80, -20)], 5, smoothEnter=True ) )

# debugShowViewer( llist )

# toolFullAuto( llist )



#---------------------------------------
##def geomCreateSlotRingHoleTEST( p1, p2, diaStart, diaEnd, diaSteps,
##                                depth, depthInc,
##                                enterHeight, enterSteps, dir,
##                                fBase, fEntry, fRetract     ):
# feedrates per part could look like this, as optional arguments, supporting
# either None (aka, nothing; as predefined from reference), an absolute value
# (as reference), a percentage (as a base modifier) or a RAPID instruction.
# RAPIDS would work directly for straight moves only (already implemented),
# but would require a double set of instructions for everything else; e.g.
# set a high feedrate for this G2/3 move, but switch back to the base speed
# afterwards. Would be easier to use "info" vertices here, rather than putting
# all of this in the elements themselves.
# llist = []
# llist.append(  geomCreateSlotRingHoleTEST(  (-10,10,-10), (80,40,0), 100, 200, 3,
#                                             30, 15,
#                                             20, 2, 'cc' )  )
# debugShowViewer( llist )

# ## doesn't matter where this appears as long as it's before toolFullAuto()
# toolFeedRateSet( 4444 )


# ## should give an error (0 feed rate)
# #toolFullAuto( llist )

# ## should give a warning (low feed rate)
# ## implemented because the feed rate was the safe-Z position in earlier code variants
# #toolFullAuto( llist, 20)

# ## should be okay
# #toolFullAuto( llist, 900 )

# ## should use the value from toolFeedRateSet() above
# toolFullAuto( llist )



#---------------------------------------
##def toolCalcFeedratePercentage( fBase, strPercentage ):

# print( toolCalcFeedratePercentage( 330, " " ) )
# print( toolCalcFeedratePercentage( 330, "%55" ) )
# print( toolCalcFeedratePercentage( 330, "  55.44 %  " ) )
# print( toolCalcFeedratePercentage( 330, "200%" ) )




#---------------------------------------
##def geomCreateSlotRingHole( p1, p2, diaStart, diaEnd, diaSteps, depth, depthInc, enterHeight, enterSteps, dir ):
# llist = []
# #llist.append(  geomCreateSlotRingHole( (-10,10,-10), (80,40,0), 80, 40, 2, 30, 15, 20, 1, 'cc' )  )
# #llist.append(  geomCreateSlotRingHole( (-10,10,-10), (80,40,0), 40, 80, 2, 30, 15, 20, 1, 'cw' )  )
# llist.append(  geomCreateSlotRingHole( (-10,10,-10), (80,40,0), 100, 200, 10, 10, 2, 3, 1, 'cw' )  )

# debugShowViewer( llist )

# toolFullAuto( llist, 20 )



#---------------------------------------
##def geomCreateConcentricSlots( p1, p2, diaStart, diaEnd, diaSteps, dir, basNr=0 ):
# llist = []
# llist.append(  geomCreateConcentricSlots( (20,20,0), (60,30,-10), 15, 30, 15, 'cw' )  )
# llist.append(  geomCreateConcentricSlots( (20,60,0), (60,50,-10), 15, 30, 15, 'cc' )  )
# llist.append(  geomCreateConcentricSlots( (-50,80,0), (20,-80,-10), 10, 20, 3, 'cc' )  )

# debugShowViewer( llist )

# toolFullAuto( llist, 20 )



#---------------------------------------
##def geomCreateSlotSpiral( p1, p2, dia, depthSteps, depthPerStep, dir, clearBottom=True, basNr=0 ):
# llist = []
# llist.append(  geomCreateSlotSpiral( (30,20,0), (70,30,0), 20, 5, 10, 'cc', clearBottom=True)  )
# llist.append(  geomCreateSlotSpiral( (30,20,0), (60,40,0), 20, 5, 10, 'cc', clearBottom=True)  )
# llist.append(  geomCreateSlotSpiral( (30,20,0), (60,60,0), 20, 5, 10, 'cc', clearBottom=True)  )
# llist.append(  geomCreateSlotSpiral( (30,20,0), (120,40,0), 20, 5, 10, 'cc', clearBottom=True)  )
# llist.append(  geomCreateSlotSpiral( (30,20,0), (120,40,0), 20, 5, 10, 'cw', clearBottom=True)  )
# llist.append(  geomCreateSlotSpiral( (-60,20,0), (-80,40,0), 20, 5, 10, 'cc', clearBottom=True)  )
# llist.append(  geomCreateSlotSpiral( (-20,-20,0), (-60,-40,0), 20, 20, 1, 'cw', clearBottom=True)  )
# llist.append(  geomCreateSlotSpiral( (-20,-20,0), (-60,-40,0), 20, 20, 1, 'cc', clearBottom=True)  )

# debugShowViewer( llist )

# toolFullAuto( llist, 20 )



#---------------------------------------
# print( arcLengthXY( (0,0,0), (1,1,0), 1 ) / math.pi )
# print( arcLengthXY( (0,0,0), (-1,1,0), 1 ) / math.pi )
# print( arcLengthXY( (0,0,0), (-1,-1,0), 1 ) / math.pi )
# print( arcLengthXY( (3,3,0), (4,4,0), 1 ) / math.pi )
# print( arcLengthXY( (3,3,0), (2,4,0), 1 ) / math.pi )
# print( arcLengthXY( (3,3,0), (2,2,0), 1 ) / math.pi )
# print( arcLengthXY( (0,0,0), (2,0,0), 1 ) / math.pi )
# print( arcLengthXY( (0,0,0), (-2,0,0), 1 ) / math.pi )
# print( arcLengthXY( (0,0,0), (-2,0,0), 1 ) / math.pi )



#---------------------------------------
#def geomCreateSlotHole( p1, p2, diaStart, diaEnd, diaSteps, dir, basNr=0 )

# llist = []
# llist.append(  geomCreateConcentricSlots( (20,20,0), (60,40,0), 10, 20, 3, 'cc' )  )
# llist.append(  geomCreateConcentricSlots( (-20,20,0), (-60,40,0), 10, 20, 3, 'cw' )  )

# debugShowViewer( llist )

# toolFullAuto( llist, 20 )


#---------------------------------------
#def geomCreateConcentricRects( p1, p2, xdiff, ydiff, stepOver, dir, basNr=0 ):
# llist = []
# llist.append( geomCreateConcentricRects( ( 10, 30,0), (50,50,0), 10, 5, 3, 'cw' )  )
# llist.append( geomCreateConcentricRects( ( 20,-20,0), (40,20,0), 8, 8, 3, 'cw' )  )
# llist.append( geomCreateConcentricRects( ( 20,-70,0), (40,-30,0), 5, 10, 3, 'cw' )  )
# llist.append( geomCreateConcentricRects( ( 60, 30,0), (100,50,0), 10, 5, 3, 'cc' )  )
# llist.append( geomCreateConcentricRects( ( 70,-20,0), (90,20,0), 8, 8, 3, 'cc' )  )
# llist.append( geomCreateConcentricRects( ( 70,-70,0), (90,-30,0), 5, 10, 3, 'cc' )  )
# # these need some work :-)
# llist.append( geomCreateConcentricRects( ( -10, 30,0), (-50,50,0), -10, -5, 3, 'cc' )  )
# llist.append( geomCreateConcentricRects( ( -20,-20,0), (-40,20,0), 8, 8, 3, 'cc' )  )
# llist.append( geomCreateConcentricRects( ( -20,-70,0), (-40,-30,0), 5, 10, 3, 'cc' )  )

# llist.append( geomCreateConcentricRects( ( 90-35,-90,0), (90-35,-50,0), 5, 10, 3, 'cw' )  )

# debugShowViewer( llist )

# toolFullAuto( llist, 20 )



#---------------------------------------
# discovered an error while working on conentric rects; cc/cw didn't work
# llist = []
# llist.append( geomCreateRect( (-50,-40,0), (50,40,0), 0, 'cw' ) )
# llist.append( geomCreateRect( (-40,-30,0), (40,30,0), 0, 'cc' ) )

# debugShowViewer( llist )

# toolFullAuto( llist, 20 )


#---------------------------------------
#def geomCreateRadial( p1, dia1, p2, dia2, angleStart, angleInc, angleSteps, connect1='direct', connect2='direct', basNr=0 ):
# llist = []
# llist.append( geomCreateRadial( ( 10,0,0), 10, (0,0,0), 40, 22.0, 10, 18 ) )
# llist.append( geomCreateRadial( (-30,30,0), 20, (-30,30,0), 30, 0, 10, 36 ) )
# llist.append( geomCreateRadial( (0,30,0), 20, (0,30,10), 30, 0, 10, 36 ) )
# llist.append( geomCreateRadial( (30,30,0), 20, (30,30,-10), 10, 0, 10, 36 ) )
# llist.append( geomCreateRadial( (-30,-30,0), 20, (-30,-30,0), 30, 0, 10, 36, 'line', 'back' ) )
# llist.append( geomCreateRadial( (  0,-30,0), 20, (  0,-30,5),15, 0, 10, 36, 'line', 'back' ) )
# llist.append( geomCreateRadial( ( 30,-30,0), 20, ( 30,-30,-5),10, 0, 10, 36, 'line', 'zup' ) )
# llist.append( geomCreateRadial( ( 70,-30,0), 20, ( 70,-30,-5),30, 0, 10, 36, 'line', 'zup' ) )
# llist.append( geomCreateRadial( ( -30,0,0), 1, ( -30,0,0.2),1.2, 0, 20, 18, 'line', 'zup' ) )
# llist.append( geomCreateRadial( ( 30,0,0), 20, ( 35,5,10),22, 0, 20, 18, 'line', 'zup' ) )
# llist.append( geomCreateRadial( ( -30,-70,0), 30, ( -30,-70,-10),20, 0, 20, 18, 'line', 'arcflat' ) )
# llist.append( geomCreateRadial( ( 0,-70,0), 20, ( 0,-70,-10),30, 0, 20, 18, 'line', 'arcflat' ) )
# llist.append( geomCreateRadial( ( 40,-70,0), 20, ( 40,-70,-10),30, 0, -20, 18, 'line', 'arcflat' ) )
# llist.append( geomCreateRadial( ( 40,-70,0), 20, ( 40,-70,-10),10, 0, -20, 18, 'line', 'arcflat' ) )
# llist.append( geomCreateRadial( ( -30,70,0), 30, ( -30,70,-10),20, 0, 20, 18, 'arcflat', 'arcflat' ) )
# llist.append( geomCreateRadial( ( 0,70,0), 20, ( 0,70,-10),30, 0, 20, 18, 'arcflat', 'arcflat' ) )
# llist.append( geomCreateRadial( ( 40,70,0), 20, ( 40,70,-10),30, 0, -20, 18, 'arcflat', 'arcflat' ) )
# llist.append( geomCreateRadial( ( 70,70,0), 20, ( 70,70,-10),10, 0, -20, 18, 'arcflat', 'arcflat' ) )
# llist.append( geomCreateRadial( ( 70,25,0), 5, ( 70,25, 0),30, 0, 10, 36, 'arcflat', 'arcflat' ) )


# debugShowViewer( llist )

# toolFullAuto( llist, 5 )




#---------------------------------------
#def geomCreateCircRingHole( p1, diaStart, diaEnd, diaSteps, depth, depthSteps, hDepth, hDepthSteps, clear, dir, basNr=0 ):
# llist = []
# llist.append(  geomCreateCircRingHole( (-20,0,0), 1, 3, 4, 5.5, 11, 1, 4, True, 'cc'  )  )
# llist.append(  geomCreateCircRingHole( (-10,0,0), 1, 3, 4, 5.5, 11, 1, 4, True, 'cw'  )  )
# llist.append(  geomCreateCircRingHole( (0,0,0), 1, 3, 8, 5.5, 11, 1, 8, True, 'cc'  )  )
# llist.append(  geomCreateCircRingHole( (10,0,0), 1, 3, 4, 5.5, 22, 1, 4, True, 'cc'  )  )


# debugShowViewer( llist )

# toolFullAuto( llist, 5 )






#---------------------------------------
#def geomCreateBezier( p1, p2, p3, p4, steps, basNr=0 ):
# llist = []
# llist.append(  geomCreateBezier4P( (0,0,0), (25,0,0), (25,10,0), (50,10,0), 20 )  )
# llist.append(  geomCreateBezier4P( (0,0,0), (50,0,0), (50,30,0), (30,10,0), 20 )  )
# llist.append(  geomCreateBezier4P( (0,0,-20), (50,0,0), (50,30,0), (30,10,30), 20 )  )
# llist.append(  geomCreateBezier  ( (0,0,30), (50,0,0), (50,50,-30), 50 )  )
# llist.append(  geomCreateBezier  ( (0,0,30), (50,0,0), (50,50,-30),  5 )  )
# llist.append(  geomCreateBezier  ( (0,0,0), (50,0,0), (50,10,0), 20 )  )

# debugShowViewer( llist )

# toolFullAuto( llist, 20 )



#---------------------------------------
#def geomCreateConcentricCircles(p1,diaStart,diaEnd,diaSteps,dir,basNr=0):
# llist = []
# llist.append(  geomCreateConcentricCircles( (0,0,0), 10, 20, 3, 'cw')  )

# debugShowViewer( llist )

# toolFullAuto( llist, 20, ['zig','zag'], fnameHeader='ncPRG' )



#---------------------------------------
# llist = []
# llist.append( geomCreateZig(  (91, 0, -0.5), ( 30, 30, 0), 3, 5,  False )  )
# llist.append( geomCreateZig(  (-50, -50, 1.0), ( 10, -10, 0), 3, 2,  False )  )

# debugShowViewer( llist )

# toolFullAuto( llist, 20, ['zig','zag'], fnameHeader='ncPRG' )



#---------------------------------------
# llist = []
# llist.append( geomCreateZig(  (91, 0, -0.5), ( 30, 30, 0), 3, 5,  False )  )
# llist.append( geomCreateZig(  (-50, -50, 1.0), ( 10, -10, 0), 3, 2,  False )  )

# debugShowViewer( llist )

# parts = []
# for e in llist:
# 	parts.append( partCreate( "C2000 Test Messing", e ) )
# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)


#---------------------------------------
# llist = []
# llist.append( geomCreateZigZag(  ( -3, 0, -0.6), (91, 30, 0), 1.5, False )  )
# debugShowViewer( llist )
# parts = []
# for e in llist:
# 	parts.append( partCreate( "C2000 Test Messing", e ) )
# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)




#---------------------------------------
#def geomCreateRectHelix( p1, p2, depth, depthSteps, dir, clearBottom=True, basNr=0 ):
# llist = []
# llist.append( geomCreateRectHelix( (-50,-40,0), (30,20,0), 10, 5, 'cw' ) )
# r2 = geomCreateRectHelix( (-30,-10,0), (40,-50,0), 3, 20, 'cc' )
# r2 = geomRotateZ( r2, 12.5 )
# llist.append( r2 )
# debugShowViewer( llist )
# parts = []
# for e in llist:
# 	parts.append( partCreate( "Loch von 10.5 auf 12 aufspiralen", e ) )
# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)



#---------------------------------------
# def geomCreateRect( p1, p2, dir, basNr=0 ):
# llist = []
# llist.append( geomCreateRect( (-50,-40,0), (30,20,0), 10, 'cw' ) )
# llist.append( geomCreateRect( (-50, 30,0), (60,30,0), 20, 'cw' ) )
# r2 = geomCreateRect( (-30,-10,0), (40,-50,0), 0, 'cc' )
# r2 = geomRotateZ( r2, 12.5 )
# llist.append( r2 )
# debugShowViewer( llist )
# parts = []
# for e in llist:
# 	parts.append( partCreate( "Loch von 10.5 auf 12 aufspiralen", e ) )
# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)




#---------------------------------------
# llist = []
# llist.append( geomCreateSpiralToCircle( (0,0,-5), 10, -1.5, 15, 'cc' ) )
# debugShowViewer( llist )
# parts = []
# for e in llist:
# 	parts.append( partCreate( "Loch von 10.5 auf 12 aufspiralen", e ) )
# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)




#---------------------------------------
# llist = []
# # geomCreateHelix( p1, dia, depth, depthSteps, dir, basNr=0, finish='finish' ):
# llist.append( geomCreateHelix( (-10,-10,0), 10, 10, 2, 'cc') )
# debugShowViewer( llist )
# parts = []
# for e in llist:
# 	parts.append( partCreate( "helix reworked", e ) )
# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)



#---------------------------------------
# llist = []
# llist.append( geomCreateSpiralToCircle( (0,0,0), 10, -1.5, 15, 'cc' ) )
# debugShowViewer( llist )
# parts = []
# for e in llist:
# #	parts.append( partCreate( "spiral for 6mm Fr; 30 to 29mm, 20 steps", e ) )
# #	parts.append( partCreate( "spiral for 6mm Fr; 29 to 28mm, 10 steps", e ) )
# 	parts.append( partCreate( "spiral for 6mm Fr; 29 to 28mm, 20 steps", e ) )
# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)



#---------------------------------------
# llist = []
# # geomCreateCircRingHole(p1,diaStart,diaEnd,diaSt,depth,depthSt,hDepth,hDepthSt,clear,dir,basNr=0):
# # llist.append( geomCreateCircRingHole( (-20,0,0), 10, 40, 3,   5,2,   3,3,    2, 'cc') )
# # llist.append( geomCreateCircRingHole( ( 20,0,0), 10, 40, 3,   5,2,   3,3,    2, 'cw') )
# llist.append( geomCreateCircRingHole( ( 0,0,0), 10, 40, 6,   5,2,   5,3,   0,   'cw') )
# debugShowViewer( llist )
# parts = []
# for e in llist:
# 	parts.append( partCreate( "mill a 10.5mm hole, 5mm deep with a 2mm endmill ", e ) )
# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)



#---------------------------------------
# llist = []
# llist.append( geomCreateCircRingHole( (0,0,0), 1, 9, 20,   5,10,2,10,1,'cc') )

# debugShowViewer( llist )

# parts = []
# for e in llist:
# 	parts.append( partCreate( "mill a 10.5mm hole, 5mm deep with a 2mm endmill ", e ) )

# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()

# toolFileWrite( tool )
# sys.exit(0)



#---------------------------------------
# llist = []
# #llist.append( geomCreateSpiralToCircle( (0,0,0), 35 , 0.05, 20, 'cw' ) )
# #llist.append( geomCreateSpiralToCircle( (0,0,0), 35 , 0.1, 10, 'cc' ) )
# llist.append( geomCreateSpiralToCircle( (0,0,0), 34 , 0.05, 20, 'cw' ) )
# #llist.append( geomCreateSpiralToCircle( (0,0,0), 34 , 0.05, 20, 'cc' ) )
# debugShowViewer( llist )

# parts = []
# for e in llist:
# #	parts.append( partCreate( "spiral for 6mm Fr; 30 to 29mm, 20 steps", e ) )
# #	parts.append( partCreate( "spiral for 6mm Fr; 29 to 28mm, 10 steps", e ) )
# 	parts.append( partCreate( "spiral for 6mm Fr; 29 to 28mm, 20 steps", e ) )

# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()

# toolFileWrite( tool )
# sys.exit(0)




#---------------------------------------
# llist = []
# llist.append( geomCreateSpiralToCircle( ( 20, 20,0), 20.0,  1, 5, 'cw' ) )
# llist.append( geomCreateSpiralToCircle( ( 20,-20,0), 20.0,  1, 5, 'cc' ) )
# llist.append( geomCreateSpiralToCircle( (-20, 20,0), 20.0, -1, 5, 'cw' ) )
# llist.append( geomCreateSpiralToCircle( (-20,-20,0), 20.0, -1, 5, 'cc' ) )
# debugShowViewer( llist )

# parts = []
# for e in llist:
# 	parts.append( partCreate( "trololol", e ) )

# tool = []
# for p in parts:
# 	# tool += toolCreateSimpleHeader()
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# 	# tool += toolCreateSimpleFooter()

# toolFileWrite( tool )
# sys.exit(0)



#---------------------------------------
# l1 = elemCreateLine( (0,0,0),(10,10,0))
# l2 = elemCreateLineTo( l1, (-10,10,0 ) )
# geom = [ l1, l2]
# debugShowViewer( geom )
# partCreate( "trololol", geom )
# sys.exit(0)



#---------------------------------------
# llist = []
# llist.append( geomCreateCircle( (20,20,0), 22.5, 25.0, 'cc' ) )
# debugShowViewer( llist )
# sys.exit(0)


#---------------------------------------
#e1 = geomCreateSpiralHelix( ( 0, 0, 0), (-20,0,0), -1.5, 0, 999, 'cw' ) 
# e1 = geomCreateSpiralHelix( ( 0, 0, 0), (-20,0,0), -3.0, 0, 999, 'cw' ) 
# debugShowViewer( [e1] )
# p1 = partCreate( "spiral 1" )
# partAddElements( p1, e1 )
# tool = []
# # tool += toolCreateSimpleHeader()
# tool += toolRapidToNextPart(p1)
# tool += toolCreateFromPart(p1)
# # tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)



#---------------------------------------
# llist = []
# llist.append( geomCreateSlotPoly( [(-90,0,0), (-80,10,0), (-50,0,-10)], 2, smoothEnter=False ) )
# llist.append( geomCreateSlotPoly( [(-30,0,0), (-10,10,0), (10,-10,0), (30,0,-10)], 4, smoothEnter=True ) )
# llist.append( geomCreateSlotPoly( [(40,60,0), (80,60,0), (80,20,0), (40,20,0),(40,60,-15)], 5, smoothEnter=True ) )
# llist.append( geomCreateSlotPoly( [(40, 0,0), (80, 0,0), (80,-40,0), (40,-40,0),(40, 0,-15)], 5, smoothEnter=False ) )
# llist.append( geomCreateSlotPoly( [(-50, -50,0), (50, -50, -20)], 5, smoothEnter=False ) )
# llist.append( geomCreateSlotPoly( [(-50, -80,0), (50, -80, -20)], 5, smoothEnter=True ) )
# debugShowViewer( llist )
# plist = []
# for e in llist:
# 	p = partCreate()
# 	p = partAddElements( p, e )
# 	plist.append( p )
# tool = []
# tool += toolCreateSimpleHeader()
# for p in plist:
# 	tool += toolRapidToNextPart( p )
# 	tool += toolCreateFromPart( p )
# toolFileWrite( tool )
# sys.exit(0)


#---------------------------------------
# The rounding of the new "format" conversion of the number-to-string
# produces an error in the G-Code output:
# G02 X0.027794 Y-57.157101 Z-3.333333 R0.416667
#   X-21.545993 Y-72.831374 Z-3.333333 R13.333333  <- illegal arc; should be R13.333334
#     X0.027794 Y-57.157101 Z-3.333333 R13.333333
# Yep, it was an error (done in 1995 :) to use R instead of IJ
# Anyway, now corrected.
# llist=[]
# p1 = partCreate('Hole')
# # def geomCreateCircRingHole(p1,diaStart,diaEnd,diaSt,depth,depthSt,hDepth,hDepthSt,clear,dir,basNr=0):
# p1 = partAddElements( p1, geomCreateCircRingHole( (20,25,0), 20,30,3,   10,3,  20,2,5, 'cw')  )
# for i in range(6):
# #	llist.append(  partTranslate(p1, (-100 + i*30,-50,0))  )
# #	llist.append(  partRotateZ(p1, 360/5 * i)  )
# 	llist.append(  partRotateZAt(p1, 360/5 * i, (-10,-15,0 ) )  )
# debugShowViewer( llist )
# tool = []
# for part in llist:
# 	tool += toolRapidToNextPart( part )
# 	tool += toolCreateFromPart( part )
# toolFileWrite( tool )
# sys.exit(0)


#---------------------------------------
# e1 = geomCreateSpiralHelix( ( 0, 0, 0), (50,0,0), -5, -5, 10, 'cc' )
# e2 = geomCreateCircRingHole((0,0,0),20.0,20.0,1.0,5,3,2,2,5,'cw')
# debugShowViewer( [e1, e2] )
# p1 = partCreate( "helix 1" )
# partAddElements( p1, e1 )
# p2 = partCreate( "hole 1" )
# partAddElements( p2, e2 )
# tool = []
# # tool += toolCreateSimpleHeader()
# tool += toolRapidToNextPart(p1)
# tool += toolCreateFromPart(p1)
# tool += toolRapidToNextPart(p2)
# tool += toolCreateFromPart(p2)
# # tool += toolCreateSimpleFooter()
# toolFileWrite( tool )
# sys.exit(0)




#---------------------------------------
# e  = geomCreateSlotLine( (-20,-10,5), (50,30,-10), 4)
# e += geomCreateSlotLine( (-50,-10,0), (-10,-10,-10), 0)
# debugShowViewer( e )
# sys.exit()


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
#---- Everything below is super old ----
#---------------------------------------
#---------------------------------------
# l1=elemCreateLine((-10,-10,0),   (100,-10,0))
# l2=elemCreateLine((100,-10,0), (130,60,0))
# l3=elemCreateLine((130,60,0),(-50,30,0))
# a1=elemCreateArc180((-50,30,0),(-60,-20,0),30,'cw')
# a2=elemCreateArc180((-60,-20,0),(-30,10,0),50,'cw')
# l4=elemCreateLine((-30,10,0),  (-10,-10,0))


# #a1=elemCreateArc180((0,0,0),(50,0,0),40,'cw')
# l01=elemCreateLine((0,0,0),(20,0,0))
# l02=elemCreateLine((20,0,0),(20,-15,0))
# l03=elemCreateLine((20,-15,0),(35,-15,0))
# l04=elemCreateLine((35,-15,0),(35,0,0))
# l05=elemCreateLine((35,0,0),(50,0,0))

# l1=elemCreateLine((50,0,0),   (0,50,0))
# a2=elemCreateArc180((0,50,0),(-50,30,0),40,'cc')
# l2=elemCreateLine((-50,30,0),   (0,0,0))


# p1=partCreate('pups')

# p1=partAddElement(p1,l01,1)
# p1=partAddElement(p1,l02,2)
# p1=partAddElement(p1,l03,3)
# p1=partAddElement(p1,l04,4)
# p1=partAddElement(p1,l05,5)

# p1=partAddElement(p1,l1,6)
# p1=partAddElement(p1,a2,10)
# p1=partAddElement(p1,l2,11)

# a1=elemCreateArc180((0,0,0),(30,0,20),15,'cw')
# a2=elemCreateArc180((30,0,20),(0,0,40),15,'cw')
# a3=elemCreateArc180((0,0,40),(30,0,60),15,'cw')
# a4=elemCreateArc180((30,0,60),(0,0,80),15,'cw')

# p2=partCreate('pansen')
# p2=partAddElement(p2,a1,1)
# p2=partAddElement(p2,a2,2)
# p2=partAddElement(p2,a3,3)
# p2=partAddElement(p2,a4,4)


# h1=geomCreateHelix((50,50,0),5,10,10,'cw',0,'nofinish')
# p3=partCreate('helix')
# p3=partAddElements(p3,h1)


# c1=geomCreateConcentricCircles((0,0,0),30,10,5,'cc')
# p4=partCreate('Concentric')
# p4=partAddElements(p4,c1)


# h1=geomCreateCircRingHole((0,0,0),1,50,49,5,3,2,2,5,'cw')


# p5=partCreate('Hole')
# p5=partAddElements(p5,geomCreateCircRingHole((0,0,0),20.0,20.0,1.0,5,3,2,2,5,'cw'))

# p6=partCreate('Hole2')
# p6=partAddElements(p6,geomCreateCircRingHole((100,0,0),1,10,9,5,3,2,2,5,'cc'))

# p7=partCreate('Hole3')
# p7=partAddElements(p7,geomCreateCircRingHole((100,50,0),10,1,9,5,3,2,2,5,'cw'))

# p8=partCreate('Hole4')
# p8=partAddElements(p8,geomCreateCircRingHole((0,50,0),1,10,9,5,3,2,2,5,'cw'))




#f=open('debug.log','w+t')
#for i in p5['elements']:
#  f.write(str(i)+'\n')
#f.close()



# f=open('ncEFI.nc','w+t')
# for i in toolCreateSimpleHeader():
# 	f.write(i+'\n')


# for i in toolRapidToNextPart(p1):
# 	f.write(i+'\n')
# for i in toolCreateFromPart(p1):
# 	f.write(i+'\n')

# for i in toolRapidToNextPart(p6):
# 	f.write(i+'\n')
# for i in toolCreateFromPart(p6):
# 	f.write(i+'\n')

# for i in toolRapidToNextPart(p7):
# 	f.write(i+'\n')
# for i in toolCreateFromPart(p7):
# 	f.write(i+'\n')

# for i in toolRapidToNextPart(p8):
# 	f.write(i+'\n')
# for i in toolCreateFromPart(p8):
# 	f.write(i+'\n')

# for i in toolRapidToNextPart(p1):
# 	f.write(i+'\n')
# for i in toolCreateFromPart(p1):
# 	f.write(i+'\n')

	
# for i in toolCreateSimpleFooter():
# 	f.write(i+'\n')

# f.close()

# print( "p1 closed :",partCheckClosed(p1) )

# p10=partCreate('PupsContour')
# e10=geomCreateContour(p1,-5.0)
# p10=partAddElements(p10,e10)

# p20=partCreate('PupsSlot')
# e20=geomCreateSlotContour(p1,-3.0)
# p20=partAddElements(p20,e20)



# #for i in range(1,len(p1['elements'])):
# #  e1=partGetElement(p1,i)
# #  e2=partGetElement(p1,i+1)
# #  if e1 == [] or e2 == []:
# #    break
# #  ips=elemIntersectsElemXY(e1,e2)
# #  print( "i: ",i," -> ",ips )
	

# #cc1=geomCreateLeftContour(p1,-5.0)
# #cc1=geomTrimPointsStartToEnd(cc1,'Closed')
# #p50=partCreate('PupsContour1')
# #p50=partAddElements(p50,cc1)
# #cc2=geomCreateLeftContour(p50,-5.0)
# #p51=partCreate('PupsContour2')
# #p51=partAddElements(p51,cc2)


# ss1=geomCreateSlotContour(p1,-5)
# ss1=geomExtractSlotDirVecs(ss1)
# p60=partCreate('SlotControl')
# p60=partAddElements(p60,ss1)


# ss2=geomCreateLeftContour(p1,-5.0)
# p61=partCreate('LeftContour1')
# p61=partAddElements(p61,ss2)

# ss3=geomCreateLeftContour(p61,-5.0)
# p62=partCreate('LeftContour2')
# p62=partAddElements(p62,ss3)

# ss4=geomCreateSlotContour(p61,-5.0)
# ss4=geomExtractSlotDirVecs(ss4)
# p63=partCreate('SlotControl61')
# p63=partAddElements(p63,ss4)


# partlist=[p1,p61,p62]

# f=open('ncEFI.dat','w+b')
# pickle.dump(partlist,f)
# f.close()

# print( "SLOT CONTOUR:" )
# for i in p62['elements']:
# 	print( i )

# import os
# os.system('python ncEFIDisp2.py ncEFI.dat')

# sys.exit(0)



