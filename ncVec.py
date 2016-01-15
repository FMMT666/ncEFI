#!/usr/bin/python2.4


import string
import pickle
import math
import sys
import types


LINTOL=0.001	# 100nm (if units are "mm")
RADTOL=0.001    # < 1m Grad




#############################################################################
### vecLength
###
#############################################################################
def vecLength(p1,p2=None):
  if p2 == None:
    return ( p1[0]**2 + p1[1]**2 + p1[2]**2 )**0.5
  else:
    return ( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2 )**0.5
  

#############################################################################
### vecExtract
###
#############################################################################
def vecExtract(p1,p2):
  return (p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2])


#############################################################################
### vecAdd
###
#############################################################################
def vecAdd(p1,p2):
  return (p2[0]+p1[0],p2[1]+p1[1],p2[2]+p1[2])


#############################################################################
### vecInSnapToleranceXY
###
#############################################################################
def vecInSnapToleranceXY(p1,p2):
  a=math.fabs(p1[0]-p2[0])
  b=math.fabs(p1[0]-p2[0])

  if a < LINTOL and b < LINTOL:
    return True
  else:
    return False


#############################################################################
### vecReverse
###
#############################################################################
def vecReverse(p1):
  return (-p1[0],-p1[1],-p1[2])


#############################################################################
### vecRotateZ
###
#############################################################################
def vecRotateZ(p1,ang):
  x=p1[0]*math.cos(ang)+p1[1]*math.sin(ang)
  y=-p1[0]*math.sin(ang)+p1[1]*math.cos(ang)
  return (x,y,p1[2])


#############################################################################
### vecScale
### 0 = normalized
#############################################################################
def vecScale(p1,fac):
  if fac != 0:
    pr=(p1[0]*fac,p1[1]*fac,p1[2]*fac) 
    return pr
  else:
    len=vecLength(p1)
    if len == 0:
      return (0,0,0)
    else:
      return (p1[0]/len,p1[1]/len,p1[2]/len)


#############################################################################
### vecAngleXY
###
### Returns angle of given vector
### (100,0,0) -> 0 
### (0,100,0) -> pi/2  (90)
#############################################################################
def vecAngleXY(p1):
  len=vecLength((p1[0],p1[1],0))
  if len == 0:
    print "vecAngleXY: vector has zero length"
    return None
  an=math.asin(math.fabs(p1[1])/len)
  if p1[0] >= 0:
    if p1[1] >= 0:
      # first quadrant (upper right)
      return an
    else:
      # second quadrant (lower right)
      an=2*math.pi-an
      if an >= 2*math.pi:
        an-=2*math.pi
      else:
        if an<0:
          an+=2*math.pi
      return an
  else:
    if p1[1] < 0:
      # third quadrant
      return math.pi+an
    else:
      # fourth quadrant
      return math.pi-an


#############################################################################
### vecAngleDiffXY
###
### Returns the difference of the angle between two vectors.
###  0 -> p2 is an extension to p1
### >0 -> p2 turns to left side
### <0 -> p2 turns to right side
#############################################################################
def vecAngleDiffXY(p1,p2):
  a1=vecAngleXY(p1)
  a2=vecAngleXY(p2)

  if a1==None or a2==None:
    return None

  if a1==a2:
    return 0.0
  
  as=2.0*math.pi-a1+a2
  if as >= 2.0*math.pi:
    as-=2.0*math.pi

  if as <= math.pi:
    return as
  else:
    return -(2.0*math.pi-as)

  

#############################################################################
### vecHasPoint
###
### Returns true if px is on a infinite line through p1 and p2
#############################################################################
def vecHasPointXY(p1,p2,px):
  if not p1[2]==p2[2]==px[2]:  
    print "vecHasPointXY: line and point not in same plane (xy)"
    return False

  if p1==p2:
    if px==p1:
      return True
    else:
      return False
  
  x1,y1,z1=p1
  x2,y2,z2=p2
  x,y,z=px

  if y2-y1 == 0.0:
    if y==y1:
      return True
    else:
      return False

  if x2-x1 == 0.0:
    if x==x1:
      return True
    else:
      return False

  # add some tolerances:
  a=1.0*(x-x1)/(x2-x1)
  b=1.0*(y-y1)/(y2-y1)
  
  if math.fabs(a-b) < LINTOL:
    return True
  else:
    return False


#############################################################################
### vecDistPointOnLineXY
###
### If px resides on the (infinite) line p1->p2, this function returns the
### normalized distance from p1 to px:
### d < 0: not on line but d "behind" p1
### 0 < d < 1: on line (d==0 -> on p1; d==1 -> on p2)
### d > 1: beyond p2
### None: somewhere else
#############################################################################
def vecDistPointOnLineXY(p1,p2,px):
  if not vecHasPointXY(p1,p2,px):
    return None
  rlen=vecLength(p1,p2)
  if rlen == 0.0:
    if px==p1:
      return 0.0
    else:
      return None
  plen1=vecLength(p1,px)
  plen2=vecLength(p2,px)
  
  if (plen1+plen2) + LINTOL > rlen:
    if plen2>plen1:
      return -(plen2-rlen)/rlen

  return plen1/rlen


#############################################################################
### vecHasPointOnLineXY
###
### Returns true if px is on a line between p1 and p2
#############################################################################
def vecHasPointOnLineXY(p1,p2,px):
  erg=vecDistPointOnLineXY(p1,p2,px)
  if erg==None:
    return False
  if 0.0 <= erg <= 1.0:
    return True
  else:
    return False



#############################################################################
### vecGetParameter
###
### Returns the parameter of a given vector (or "line")
#############################################################################
def vecGetParameter(p1,p2):
  if p1==p2:
    p1=(0,0,0)
  return (p2[1]-p1[1],p1[0]-p2[0],p2[0]*p1[1]-p1[0]*p2[1])


#############################################################################
### vecIntersectXY
###
### Returns the intersection of two vectors (by points)
#############################################################################
def vecIntersectXY(p1,p2,q1,q2):
  if not p1[2]==p2[2]==q1[2]==q2[2]:  
    print "vecIntersectXY: lines not in same plane (xy)"
    return None
  par1=vecGetParameter(p1,p2)
  par2=vecGetParameter(q1,q2)
  c1=par1[0]*par2[1]-par1[1]*par2[0]
  if not c1:
    return None
  c2=par1[1]*par2[2]-par1[2]*par2[1]
  c3=par1[2]*par2[0]-par1[0]*par2[2]
  return (c2/c1,c3/c1,p1[2])


#############################################################################
### vecArcIntersectXY (spelled "arc" but pronounced "circle")
###
### Returns a list of intersections of a line and an arc (by midpoint and radius)
#############################################################################
def vecArcIntersectXY(p1,p2,pc,r):
  if not p1[2]==p2[2]==pc[2]:  
    print "vecIntersectXY: line and arc not in same plane (xy)"
    return None

#  print "vecArcIntersect"
#  print "__ p1: ",p1
#  print "__ p2: ",p2
#  print "__ pc: ",pc
#  print "__ r : ",r

  # intersection points list
  ips=[]

  # less to write ()
  x1,y1,z1=p1
  x2,y2,z2=p2
  x3,y3,z3=pc

  a=(x2-x1)**2+(y2-y1)**2
  b=2.0*((x2-x1)*(x1-x3)+(y2-y1)*(y1-y3))
  c=x3**2+y3**2+x1**2+y1**2-2.0*(x3*x1+y3*y1)-r**2
  s=b**2-4.0*a*c

  # s <0 -> no intersection 
  # s==0 -> tangent
  # s >0 -> 2 intersections
  if s < -LINTOL:
    return []

  if s < LINTOL:
    u=-b/(2.0*a)
    x=x1+u*(x2-x1)
    y=y1+u*(y2-y1)
    ips.append((x,y,p1[2]))
  else:
    u=(-b+math.sqrt(s))/(2.0*a)
    x=x1+u*(x2-x1)
    y=y1+u*(y2-y1)
    ips.append((x,y,p1[2]))
    u=(-b-math.sqrt(s))/(2.0*a)
    x=x1+u*(x2-x1)
    y=y1+u*(y2-y1)
    ips.append((x,y,p1[2]))
  return ips


#############################################################################
### arcIntersectXY (spelled "arc" but pronounced "circle")
###
### Returns a list of intersections of two circles (by midpoints and radii)
#############################################################################
def arcIntersectXY(p1,r1,p2,r2):
  if not p1[2]==p2[2]:  
    print "arcIntersectXY: arcs not in same plane (xy)"
    return []

  if p1==p2:
    return []

  # this simplifies our equations a lot =)
  x1,y1,z1=p1
  x2,y2,z2=p2

  d=math.sqrt((x2-x1)**2+(y2-y1)**2)
  c=(((r1+r2)**2)-(d**2))*((d**2)-((r2-r1)**2))
  if c == 0.0:
    return []
  # ups
#  c=math.sqrt(c)
  if c < 0.0:
    return []
  c=math.sqrt(math.fabs(c))

  xs1=(x2+x1)/2.0+((x2-x1)*(r1**2-r2**2))/(2*(d**2))+(y2-y1)/(2*(d**2))*c
  xs2=(x2+x1)/2.0+((x2-x1)*(r1**2-r2**2))/(2*(d**2))-(y2-y1)/(2*(d**2))*c
  ys1=(y2+y1)/2.0+((y2-y1)*(r1**2-r2**2))/(2*(d**2))+(x2-x1)/(2*(d**2))*c
  ys2=(y2+y1)/2.0+((y2-y1)*(r1**2-r2**2))/(2*(d**2))-(x2-x1)/(2*(d**2))*c

  return [(xs1,ys1,p1[2]),(xs2,ys2,p2[2])]



#############################################################################
### arcHasPointInSegmentXY
###
### Returns True if px is in a segment between p1 and p2
#############################################################################
def arcHasPointInSegmentXY(p1,p2,rad,dir,px):

  pm=arcCenter180XY(p1,p2,rad,dir)
  if pm == None:
    print "arcHasPointInSegmentXY: no midpoint: ",p1,p2,rad,dir
    return None
    
  # quick hack:
  if vecInSnapToleranceXY(p1,px) or vecInSnapToleranceXY(p2,px):
    return True
  
  if p1==p2:
    return False

  p1px=vecAngleDiffXY(vecExtract(p1,pm),vecExtract(p1,px))
  p2px=vecAngleDiffXY(vecExtract(p2,pm),vecExtract(p2,px))

  if p1px==None or p2px==None:
    return False

  # If ax is between a1 and a2, it is in the segment
  # Difference(!) from a1 and a2 range from -pi to pi (incl. direction)
  # The span can not be greater than pi!

#  print
#  print "pm   ",pm
#  print "p1   ",p1
#  print "p2   ",p2
#  print "px   ",px
#  print "p1px ",360.0/(2.0*math.pi)*p1px
#  print "p2px ",360.0/(2.0*math.pi)*p2px
#  print "dir  ",dir

  if dir == 'cw':
    if p1px >= -RADTOL and p2px <= RADTOL:
      return True
    else:
      return False
  else:
    if p1px <= RADTOL and p2px >= -RADTOL:
      return True
    else:
      return False


#############################################################################
### arcDistPointOnBowXY
###
### Returns the normalized angle (d) between pm->p1 and pm->px.
###      d <  0 -> "before" p1
### 0 <= d <= 1 -> between p1 and p2
###      d >  1 -> "beyond" p2
###
### ATTENTION:
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
### !!! Make sure this point _IS_ on a circle given by p1, p2 and rad !!!
### !!!              Otherwise, this may return crap!                 !!!
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#############################################################################
def arcDistPointOnBowXY(p1,p2,rad,dir,px):
  # ToDo:
  # - This routine really sucks...
  # - This won't work for very small arcs (length between p1 p2)

  # check if it is between p1 and p2
  chkIn=arcHasPointInSegmentXY(p1,p2,rad,dir,px)
  if chkIn==None:
    print "arcDistPointOnBowXY: arcHasPointInSegment error"
    return None

  pm=arcCenter180XY(p1,p2,rad,dir)
  if pm == None:
    print "arcDistPointOnBowXY: no midpoint: ",p1,p2,rad,dir
    return None
   
  # quick hack:
  if vecInSnapToleranceXY(p1,px):
    return 0.0
  if vecInSnapToleranceXY(p2,px):
    return 1.0

  p1p2=math.fabs(vecAngleDiffXY(vecExtract(pm,p1),vecExtract(pm,p2)))
  pxp2=math.fabs(vecAngleDiffXY(vecExtract(pm,px),vecExtract(pm,p2)))

  if p1p2==0.0:
    print "arcDistPointOnBowXY: length between p1 and p2 is 0.0"
    return None

#  print "pm:   ",pm
#  print "p1p2: ",p1p2*360.0/(math.pi*2.0)
#  print "pxp2: ",pxp2*360.0/(math.pi*2.0)

  erg=(p1p2-pxp2)/p1p2

  if chkIn==False:
    erg*=-1.0

  return erg


     
#############################################################################
### arcAngle ;)
###
#############################################################################
def arcAngle(len,rad):
  if len == 0.0 or rad == 0.0:
    return None
  try:
    return math.asin(len/(2.0*rad))*2.0
  except:
    return None



#############################################################################
### arcAngleAtPx
###
#############################################################################
def arcAngleAtPx(p1,p2,rad,dir,p):
  pm=arcCenter180XY(p1,p2,rad,dir)
  if pm == None:
    print "arcAngleAtPx: no midpoint: ",p1,p2,rad,dir
    return None
  if p!='p1' and p!='p2':
    print "arcAngleAtPx: point select is not \'p1\' or \'p2\': ",p
    return None
  if p == 'p1':
    a=vecExtract(pm,p1)
  else:
    a=vecExtract(pm,p2)
  if dir == 'cw':
    ang=math.pi/2.0
  else:
    ang=-math.pi/2.0
  a=vecRotateZ(a,ang)
  a=vecAngleXY(a)
  if a == None:
    return None
  return a



#############################################################################
### arcVectorAtPx
###
#############################################################################
def arcVectorAtPx(p1,p2,rad,dir,p):
  pm=arcCenter180XY(p1,p2,rad,dir)
  if pm == None:
    print "arcAngleAtPx: no midpoint: ",p1,p2,rad,dir
    return None
  if p!='p1' and p!='p2':
    print "arcAngleAtPx: point select is not \'p1\' or \'p2\': ",p
    return None
  if p == 'p1':
    a=vecExtract(pm,p1)
  else:
    a=vecExtract(pm,p2)
  if dir == 'cw':
    ang=math.pi/2.0
  else:
    ang=-math.pi/2.0
  a=vecRotateZ(a,ang)
  if a == None:
    return None
  return a



#############################################################################
### arcCenter180XY
###
### Given two tuples, and a radius, this function returns a tuple containing
### the center of the arc. Z axis vector is taken from p1
#############################################################################
def arcCenter180XY(p1,p2,rad,dir):
  if rad<=0.0:
    return None
  pp1=(p1[0],p1[1],0)
  pp2=(p2[0],p2[1],0)
  dist=vecLength(pp1,pp2)
  if rad < dist/2.0:
    print "arcCenter180XY: rad < dist"
    return None
  pm=vecExtract(pp1,pp2)			# get the direction vector
  an=arcAngle(dist,rad)
  if an == None:
    return None
  if dir == 'cw':
#    ann1=(math.pi-an)/2.0
#    pm=vecRotateZ(pm,ann1)		# points to middle
    ann=(math.pi-an)/2.0
  else:
#    ann2=-(math.pi-an)/2.0
#    pm=vecRotateZ(pm,ann2)		# points to middle
    ann=-(math.pi-an)/2.0

  pm=vecRotateZ(pm,ann)
  
  if pm == 0:
    return None
  pm=vecScale(pm,0)
  pm=vecScale(pm,rad)
  pp3=vecAdd(pp1,pm)
  return (pp3[0],pp3[1],p1[2])
