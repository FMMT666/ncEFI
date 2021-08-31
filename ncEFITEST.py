#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from ncEFI import *


# just various test routines



#---------------------------------------
# def geomCreateRect( p1, p2, dir, basNr=0 ):
llist = []
llist.append( geomCreateRect( (-50,-40,0), (30,20,0), 'cw' ) )
r2 = geomCreateRect( (-30,-10,0), (40,-50,0), 'cc' )
r2 = geomRotateZ( r2, 12.5 )
llist.append( r2 )
debugShowViewer( llist )
parts = []
for e in llist:
	parts.append( partCreate( "Loch von 10.5 auf 12 aufspiralen", e ) )
tool = []
for p in parts:
	# tool += toolCreateSimpleHeader()
	tool += toolRapidToNextPart( p )
	tool += toolCreateFromPart( p )
	# tool += toolCreateSimpleFooter()
toolFileWrite( tool )
sys.exit(0)




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



