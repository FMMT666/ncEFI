#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math


LINTOL = 0.0001        # 100nm (if units are "mm")
FINTOL = 0.0000000001  # 0.1nm a finer tolerance (NTOL)
RADTOL = 0.0001        # < 1m Grad




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
### vecLengthXY
###
#############################################################################
def vecLengthXY(p1,p2=None):
	if p2 == None:
		return ( p1[0]**2 + p1[1]**2 )**0.5
	else:
		return ( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 )**0.5


#############################################################################
### vecExtract
###
#############################################################################
def vecExtract(p1,p2):
	return (p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2])


#############################################################################
### vecExtractMid
###
#############################################################################
def vecExtractMid(p1,p2):
	return ( (p2[0]+p1[0])/2.0 , (p2[1]+p1[1])/2.0, (p2[2]+p1[2])/2.0 )


#############################################################################
### vecAdd
###
#############################################################################
def vecAdd(p1,p2):
	return (p1[0]+p2[0],p1[1]+p2[1],p1[2]+p2[2])


#############################################################################
### vecSub
###
#############################################################################
def vecSub(p1,p2):
	return (p1[0]-p2[0],p1[1]-p2[1],p1[2]-p2[2])


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
### vecRotateZAt
###
#############################################################################
def vecRotateZAt(vec,pos,ang):
	vec = vecSub( vec, pos )
	vec = vecRotateZ( vec, ang )
	vec = vecAdd( vec, pos )
	return vec


#############################################################################
### vecPointsInDirectionXY
###
#############################################################################
def vecPointsInDirectionXY(v1):
	ang = vecAngleXY(v1)
	if ang == None:
		return '0'

	ffd = math.pi / 8.0
	if ang < 1 * ffd or  ang > 7 * ffd:
		return '+x'
	if ang < 3 * ffd and ang > 1 * ffd:
		return '+y'
	if ang < 5 * ffd and ang > 3 * ffd:
		return '-x'
	if ang < 7 * ffd and ang > 5 * ffd:
		return '-y'
	return '0'


#############################################################################
### vecCrossProduct
###
#############################################################################
def vecCrossProduct(v1, v2):
	cp = (	v1[1]*v2[2] - v1[2]*v2[1],
			v1[2]*v2[0] - v1[0]*v2[2],
			v1[0]*v2[1] - v1[1]*v2[0] )
	return cp


#############################################################################
### vecDotProduct
###
### TODO: UNCHECKED!
#############################################################################
def vecDotProduct(v1, v2):
	dp = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
	return dp


#############################################################################
### vecDistPoint
###
### TODO: UNCHECKED!
#############################################################################
def vecDistPoint(p1, v1):
	# if v1 has zero length, return the distance between p1 and the origin
	if v1 == (0,0,0):
		return vecLength(p1)
	
	# project point p1 onto vector v1
	proj_len = vecDotProduct(p1,v1) / vecDotProduct(v1,v1)
	proj_point = (v1[0] * proj_len, v1[1] * proj_len, v1[2] * proj_len)

	# distance between p1 and the projection point
	dist = math.sqrt((p1[0] - proj_point[0])**2 + (p1[1] - proj_point[1])**2 + (p1[2] - proj_point[2])**2)

	return dist


#############################################################################
### vecDistPointLine
###
#############################################################################
def vecDistPointLine(p1: tuple, pv1: tuple, pv2: tuple) -> float:
	"""
	Calculate minimum distance from a point to a line segment in 3D space.
	
	Args:
		p1: Point coordinates (x,y,z)
		pv1: Line start point (x,y,z)
		pv2: Line end point (x,y,z)
	
	Returns:
		float: Minimum distance from point to line segment
	"""
	# if the line has zero length, return the distance between p1 and the origin
	if pv1 == pv2:
		return vecLength(p1)

	# Vector from pv1 to pv2
	line_vec = (pv2[0] - pv1[0], pv2[1] - pv1[1], pv2[2] - pv1[2])

	# Vector from pv1 to p1
	point_vec = (p1[0] - pv1[0], p1[1] - pv1[1], p1[2] - pv1[2])

	# Project point_vec onto line_vec
	proj_len = vecDotProduct(point_vec, line_vec) / vecDotProduct(line_vec, line_vec)
	proj_point = (pv1[0] + line_vec[0] * proj_len, pv1[1] + line_vec[1] * proj_len, pv1[2] + line_vec[2] * proj_len)

	# Check if the projection point is outside the line segment
	if proj_len < 0:
		proj_point = pv1
	elif proj_len > 1:
		proj_point = pv2
	# Calculate the distance between p1 and the projection point
	dist = math.sqrt((p1[0] - proj_point[0])**2 + (p1[1] - proj_point[1])**2 + (p1[2] - proj_point[2])**2)

	return dist


#############################################################################
### vecDistPointLineXY
###
#############################################################################
def vecDistPointLineXY(pt: tuple, l1: tuple, l2: tuple) -> float:
	"""
	Calculate minimum distance from point to line segment in XY plane.
	Actually rendundant, as the "true 3D" vecDistPointLine() function can do the same.
	But, anyway ...
	
	Args:
		pt: Point coordinates (x,y,z)
		l1: Line start point (x,y,z)
		l2: Line end point (x,y,z)
	
	Returns:
		float: Minimum distance from point to line segment
	"""
	# Check if line points are identical
	if vecLength(l1, l2) < FINTOL:
		return vecLength(pt, l1)
		
	# Line vector and point-to-line-start vector
	v = vecSub(l2, l1)
	w = vecSub(pt, l1)
	
	# Project w onto v
	len_sq = v[0]*v[0] + v[1]*v[1]  # Only XY components
	if len_sq < LINTOL:
		return vecLength(pt, l1)
		
	# Calculate projection parameter
	t = (w[0]*v[0] + w[1]*v[1]) / len_sq
	
	# Check if projection is beyond line segment
	if t <= 0.0:
		return vecLength(pt, l1)
	if t >= 1.0:
		return vecLength(pt, l2)
		
	# Calculate projection point and distance
	proj = (l1[0] + t*v[0], l1[1] + t*v[1], l1[2])
	return vecLength(pt, proj)


#############################################################################
### vecDistLineLineXY
###
### TODO: UNCHECKED!
#############################################################################
def vecDistLineLineXY(l1p1: tuple, l1p2: tuple, l2p1: tuple, l2p2: tuple) -> float:
	"""
	Calculate minimum distance between two lines in XY plane.
	Uses only vector operations, no dependencies on higher-level functions.
	
	Args:
		l1p1, l1p2: First line points (x,y,z)
		l2p1, l2p2: Second line points (x,y,z)
	
	Returns:
		float: Minimum distance between lines
	"""
	# vectors of the lines
	v1 = vecSub(l1p2, l1p1)
	v2 = vecSub(l2p2, l2p1)
	
	# cross product to test if lines are parallel
	cross = v1[0]*v2[1] - v1[1]*v2[0]
	
	# if they are parallel, calculate distance between lines
	if abs(cross) < LINTOL:
		# Berechne minimale Distanz von Endpunkten zur anderen Linie
		d1 = vecDistPointLineXY(l2p1, l1p1, l1p2)
		d2 = vecDistPointLineXY(l2p2, l1p1, l1p2)
		d3 = vecDistPointLineXY(l1p1, l2p1, l2p2)
		d4 = vecDistPointLineXY(l1p2, l2p1, l2p2)
		return min(d1, d2, d3, d4)
	
	# Linien schneiden sich
	return 0.0


#############################################################################
### vecDistLineLine
###
### Does not work 100% correctly. Use vecDistLineLine4 instead.
#############################################################################
def vecDistLineLine(l1p1: tuple, l1p2: tuple, l2p1: tuple, l2p2: tuple) -> float:
	"""
	Calculate minimum distance between two line segments in 3D space.
	
	Args:
		l1p1, l1p2: First line points (x,y,z)
		l2p1, l2p2: Second line points (x,y,z)
	
	Returns:
		float: Minimum distance between lines
	"""
	# Direction vectors
	v1 = vecSub(l1p2, l1p1)
	v2 = vecSub(l2p2, l2p1)
	
	# Vector between line starts
	r = vecSub(l1p1, l2p1)
	
	# Squared lengths
	a = vecDotProduct(v1, v1)
	b = vecDotProduct(v1, v2)
	c = vecDotProduct(v2, v2)
	d = vecDotProduct(v1, r)
	e = vecDotProduct(v2, r)
	
	# Check for zero lengths
	if a < LINTOL or c < LINTOL:
		return vecLength(l1p1, l2p1)
	
	# Parameters of closest points
	det = a*c - b*b
	s = 0.0
	t = 0.0
	
	if det < LINTOL:  # Lines are parallel
		d1 = vecDistPointLine(l2p1, l1p1, l1p2)
		d2 = vecDistPointLine(l2p2, l1p1, l1p2)
		d3 = vecDistPointLine(l1p1, l2p1, l2p2)
		d4 = vecDistPointLine(l1p2, l2p1, l2p2)
		return min(d1, d2, d3, d4)
	else:
		s = (b*e - c*d) / det
		t = (a*e - b*d) / det
		
	# Clamp s and t to [0,1]
	s = max(0.0, min(1.0, s))
	t = max(0.0, min(1.0, t))
	
	# Closest points on lines
	p1 = vecAdd(l1p1, vecScale(v1, s))  # vecScale statt vecMult
	p2 = vecAdd(l2p1, vecScale(v2, t))  # vecScale statt vecMult
	
	return vecLength(p1, p2)


#############################################################################
### vecDistLineLine2
###
### Does not work 100% correctly. Use vecDistLineLine4 instead.
#############################################################################
def vecDistLineLine2(l1p1: tuple, l1p2: tuple, l2p1: tuple, l2p2: tuple) -> float:
	"""
	Calculate minimum distance between two line segments in 3D space.
	Handles special cases like parallel lines and very short segments.
	
	Args:
		l1p1, l1p2: First line points (x,y,z)
		l2p1, l2p2: Second line points (x,y,z)
	
	Returns:
		float: Minimum distance between lines
	"""
	# Check for degenerate lines
	l1_len = vecLength(l1p1, l1p2)
	l2_len = vecLength(l2p1, l2p2)
	if l1_len < LINTOL or l2_len < LINTOL:
		return vecLength(l1p1, l2p1)

	# Direction vectors
	v1 = vecSub(l1p2, l1p1)
	v2 = vecSub(l2p2, l2p1)
	
	# Vector between line starts
	r = vecSub(l1p1, l2p1)
	
	# Squared lengths
	a = vecDotProduct(v1, v1)
	b = vecDotProduct(v1, v2)
	c = vecDotProduct(v2, v2)
	d = vecDotProduct(v1, r)
	e = vecDotProduct(v2, r)
	
	# Check for parallel lines
	det = a*c - b*b
	if abs(det) < LINTOL*max(a,c):
		# Use endpoint distances for parallel lines
		d1 = vecDistPointLine(l2p1, l1p1, l1p2)
		d2 = vecDistPointLine(l2p2, l1p1, l1p2)
		d3 = vecDistPointLine(l1p1, l2p1, l2p2)
		d4 = vecDistPointLine(l1p2, l2p1, l2p2)
		return min(d1, d2, d3, d4)
	
	# Parameters of closest points
	s = (b*e - c*d) / det
	t = (a*e - b*d) / det
	
	# Clamp parameters to [0,1]
	s = max(0.0, min(1.0, s))
	t = max(0.0, min(1.0, t))
	
	# Closest points on lines
	p1 = vecAdd(l1p1, vecScale(v1, s))
	p2 = vecAdd(l2p1, vecScale(v2, t))
	
	return vecLength(p1, p2)


#############################################################################
### vecDistLineLine3
###
### Does not work 100% correctly. Use vecDistLineLine4 instead.
#############################################################################
def vecDistLineLine3(l1p1: tuple, l1p2: tuple, l2p1: tuple, l2p2: tuple) -> float:
	"""
	Calculate minimum distance between two line segments in 3D space.
	Enhanced endpoint checking for near-parallel cases.
	
	Args:
		l1p1, l1p2: First line points (x,y,z)
		l2p1, l2p2: Second line points (x,y,z)
	
	Returns:
		float: Minimum distance between lines
	"""
	# Check endpoints first
	d_endpoints = min(
		vecLength(l1p1, l2p1),
		vecLength(l1p1, l2p2),
		vecLength(l1p2, l2p1),
		vecLength(l1p2, l2p2)
	)

	# Check if endpoints are very close
	if d_endpoints < LINTOL:
		return d_endpoints

	# Direction vectors
	v1 = vecSub(l1p2, l1p1)
	v2 = vecSub(l2p2, l2p1)
	
	# Vector between line starts
	r = vecSub(l1p1, l2p1)
	
	# Squared lengths
	a = vecDotProduct(v1, v1)
	b = vecDotProduct(v1, v2)
	c = vecDotProduct(v2, v2)
	d = vecDotProduct(v1, r)
	e = vecDotProduct(v2, r)
	
	# Check for degenerate/short lines
	if a < LINTOL or c < LINTOL:
		return d_endpoints

	# Parameters of closest points
	det = a*c - b*b
	if det < LINTOL*max(a,c):  # Nearly parallel
		return min(
			vecDistPointLine(l2p1, l1p1, l1p2),
			vecDistPointLine(l2p2, l1p1, l1p2),
			vecDistPointLine(l1p1, l2p1, l2p2),
			vecDistPointLine(l1p2, l2p1, l2p2)
		)

	s = (b*e - c*d) / det
	t = (a*e - b*d) / det
	
	# Clamp s and t to [0,1]
	s = max(0.0, min(1.0, s))
	t = max(0.0, min(1.0, t))
	
	# Calculate closest points
	p1 = vecAdd(l1p1, vecScale(v1, s))
	p2 = vecAdd(l2p1, vecScale(v2, t))
	
	return min(vecLength(p1, p2), d_endpoints)


#############################################################################
### vecDistLineLine4
###
### Seems to work, phew.
#############################################################################
def vecDistLineLine4(l1p1: tuple, l1p2: tuple, l2p1: tuple, l2p2: tuple) -> float:
	"""
	Calculate minimum distance between two line segments in 3D space.
	
	Args:
		l1p1, l1p2: First line points (x,y,z)
		l2p1, l2p2: Second line points (x,y,z)
	
	Returns:
		float: Minimum distance between lines
	"""
	# Calculate endpoint to line distances first
	d1 = vecDistPointLine(l2p1, l1p1, l1p2)
	d2 = vecDistPointLine(l2p2, l1p1, l1p2)
	d3 = vecDistPointLine(l1p1, l2p1, l2p2)
	d4 = vecDistPointLine(l1p2, l2p1, l2p2)
	d_min = min(d1, d2, d3, d4)

	# Direction vectors
	v1 = vecSub(l1p2, l1p1)
	v2 = vecSub(l2p2, l2p1)
	r = vecSub(l1p1, l2p1)
	
	# Check for degenerate lines
	a = vecDotProduct(v1, v1)
	b = vecDotProduct(v1, v2)
	c = vecDotProduct(v2, v2)
	if a < LINTOL or c < LINTOL:
		return d_min
		
	d = vecDotProduct(v1, r)
	e = vecDotProduct(v2, r)
	
	# Calculate parameters
	det = a*c - b*b
	if det < LINTOL*max(a,c):  # Nearly parallel
		return d_min
		
	s = (b*e - c*d) / det
	t = (a*e - b*d) / det
	
	# Clamp parameters
	s = max(0.0, min(1.0, s))
	t = max(0.0, min(1.0, t))
	
	# Calculate closest points
	p1 = vecAdd(l1p1, vecScale(v1, s))
	p2 = vecAdd(l2p1, vecScale(v2, t))
	
	# Return minimum of calculated distances
	return min(vecLength(p1, p2), d_min)


#############################################################################
### vecScale
### 0 = normalized
#############################################################################
def vecScale(p1,fac):
	if fac != 0:
		pr=(p1[0]*fac,p1[1]*fac,p1[2]*fac) 
		return pr

	len = vecLength(p1)
	if len == 0:
		return (0,0,0)

	return (p1[0]/len,p1[1]/len,p1[2]/len)


#############################################################################
### vecSetLength
###
#############################################################################
def vecSetLength(p1,len):
	if len == 0:
		return (0,0,0)
	v1 = vecScale(p1,0)
	return vecScale(v1,len)


#############################################################################
### vecAngleXY
###
### Returns angle of given vector in radians
### (100,0,0) -> 0 
### (0,100,0) -> pi/2 (90°)
#############################################################################
def vecAngleXY(p1):
	len=vecLength((p1[0],p1[1],0))
	if len == 0:
		print( "vecAngleXY: vector has zero length" )
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
### Returns the angle between two vectors in radians.
###	 0 -> p2 is parallel to p1
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
	
	ad=2.0*math.pi-a1+a2
	if ad >= 2.0*math.pi:
		ad-=2.0*math.pi

	if ad <= math.pi:
		return ad
	else:
		return -(2.0*math.pi-ad)



#############################################################################
### vecHasPoint
###
### Returns true if px is on a infinite line through p1 and p2
#############################################################################
def vecHasPointXY(p1,p2,px):
	if not p1[2]==p2[2]==px[2]:
		print( "vecHasPointXY: line and point not in same plane (xy)" )
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
### vecHasPointLeftOrRight
###
### Ignores any z-values; only xy plane!
### Returns if a point 'px' is on the left or the right of a line,
### a point 'p1' with a direction 'v1'.
### If viewed, on the vec, from p1 to p2:
###   d < 0: pt is to the left
###   d = 0: pt is "exactly" [tm] on the vector
###   d > 0: pt is to the right
#############################################################################
def vecHasPointLeftOrRight(p1,v1,px):
	# normalize vector and also shift point
	ptx = vecAdd( px, vecReverse(p1) )
	return -vecAngleDiffXY( v1, ptx )


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
		print( "vecIntersectXYpts: lines not in same plane (xy)" )
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

	if not p1[2] == p2[2] == pc[2]:	
		print( "INF: vecIntersectXY: line and arc not in same plane (xy); ignoring!" )

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
		print( "arcIntersectXY: arcs not in same plane (xy)" )
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
#	c=math.sqrt(c)
	if c < 0.0:
		return []
	c=math.sqrt(math.fabs(c))

	xs1=(x2+x1)/2.0+((x2-x1)*(r1**2-r2**2))/(2*(d**2))+(y2-y1)/(2*(d**2))*c
	xs2=(x2+x1)/2.0+((x2-x1)*(r1**2-r2**2))/(2*(d**2))-(y2-y1)/(2*(d**2))*c
	ys1=(y2+y1)/2.0+((y2-y1)*(r1**2-r2**2))/(2*(d**2))+(x2-x1)/(2*(d**2))*c
	ys2=(y2+y1)/2.0+((y2-y1)*(r1**2-r2**2))/(2*(d**2))-(x2-x1)/(2*(d**2))*c

	return [(xs1,ys1,p1[2]),(xs2,ys2,p2[2])]



#############################################################################
### circleHasPointXY
###
### Checks if a point is on a circle
#############################################################################
def circleHasPointXY(center,rad,pt):
	if rad < RADTOL:
		if vecLength( center, pt ) < LINTOL:
			# trololol, but true :)
			return True
		return False
	if center[2] != pt[2]:
		# TODO: This might be an issue. Should use LINTOL
		print( "INF: arcHasPoint: arcs and point in same plane or height (xy)" )
		return False

	# this simplifies our equations a lot =)
	xm,ym,zm = center
	x1,y1,z1 = pt

	d = math.sqrt( (x1-xm)**2 + (y1-ym)**2 )
	if d+RADTOL > rad and d-RADTOL < rad:
		return True
	else:
		return False



#############################################################################
### arcHasPointInSegmentXY
###
### Returns True if px is in a segment between p1 and p2
#############################################################################
def arcHasPointInSegmentXY(p1,p2,rad,dir,px):

	pm=arcCenter180XY(p1,p2,rad,dir)
	if pm == None:
		print( "arcHasPointInSegmentXY: no midpoint: ",p1,p2,rad,dir )
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

#	print
#	print( "pm   ",pm )
#	print( "p1   ",p1 )
#	print( "p2   ",p2 )
#	print( "px   ",px )
#	print( "p1px ",360.0/(2.0*math.pi)*p1px )
#	print( "p2px ",360.0/(2.0*math.pi)*p2px )
#	print( "dir  ",dir )

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
### Returns the normalized angle (d) in radians between pm->p1 and pm->px.
###  d < 0       -> "before" p1
###  0 <= d <= 1 -> between p1 and p2
###  d > 1       -> "beyond" p2
###
### ATTENTION:
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
### !!! Make sure this point _IS_ on a circle given by p1, p2 and rad !!!
### !!!           Otherwise, this may return crap!                    !!!
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#############################################################################
def arcDistPointOnBowXY(p1,p2,rad,dir,px):
	# ToDo:
	# - This routine really sucks...
	# - This won't work for very small arcs (length between p1 p2)

	# check if it is between p1 and p2
	chkIn=arcHasPointInSegmentXY(p1,p2,rad,dir,px)
	if chkIn==None:
		print( "arcDistPointOnBowXY: arcHasPointInSegment error" )
		return None

	pm=arcCenter180XY(p1,p2,rad,dir)
	if pm == None:
		print( "arcDistPointOnBowXY: no midpoint: ",p1,p2,rad,dir )
		return None
	 
	# quick hack:
	if vecInSnapToleranceXY(p1,px):
		return 0.0
	if vecInSnapToleranceXY(p2,px):
		return 1.0

	p1p2=math.fabs(vecAngleDiffXY(vecExtract(pm,p1),vecExtract(pm,p2)))
	pxp2=math.fabs(vecAngleDiffXY(vecExtract(pm,px),vecExtract(pm,p2)))

	if p1p2==0.0:
		print( "arcDistPointOnBowXY: length between p1 and p2 is 0.0" )
		return None

#	print( "pm:   ",pm )
#	print( "p1p2: ",p1p2*360.0/(math.pi*2.0) )
#	print( "pxp2: ",pxp2*360.0/(math.pi*2.0) )

	erg=(p1p2-pxp2)/p1p2

	if chkIn==False:
		erg*=-1.0

	return erg



#############################################################################
### arcAngle /\(°-°)/\
###
### Returns something in radians. What? TODO!
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
### Returns something in radians. What? TODO!
#############################################################################
def arcAngleAtPx(p1,p2,rad,dir,p):
	pm=arcCenter180XY(p1,p2,rad,dir)
	if pm == None:
		print( "arcAngleAtPx: no midpoint: ",p1,p2,rad,dir )
		return None
	if p!='p1' and p!='p2':
		print( "arcAngleAtPx: point select is not a string with \'p1\' or \'p2\': ", p )
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
### arcLengthXY
###
### Returns the length of an arc in the XY plane.
### As all the arcs in here cannot be >180°, this should be safe to use.
#############################################################################
def arcLengthXY(p1,p2,rad):

	if rad <= 0.0:
		print( "arcLengthXY: rad must not be <=0: ", rad )
		return None

	len = vecLengthXY( p1, p2 )
	try:
		arg = len / (2.0 * rad)
		ang = 2.0 * rad * math.asin( arg )
	except:
		print( "arcLengthXY: error while calculating arcsin; arg, len, rad: ", arg, len, rad )
		return None
	
	return ang



#############################################################################
### arcVectorAtPx
###
#############################################################################
def arcVectorAtPx(p1,p2,rad,dir,p):
	pm=arcCenter180XY(p1,p2,rad,dir)
	if pm == None:
		print( "arcAngleAtPx: no midpoint: ",p1,p2,rad,dir )
		return None
	if p!='p1' and p!='p2':
		print( "arcAngleAtPx: point select is not \'p1\' or \'p2\': ",p )
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
		if rad + RADTOL > dist / 2.0:
			rad = dist/2.0
		else:
			print( "arcCenter180XY: rad < dist/2: ", rad, dist/2.0 )
			return None

	pm=vecExtract(pp1,pp2)          # get the direction vector
	an=arcAngle(dist,rad)
	if an == None:
		return None
	if dir == 'cw':
#		ann1=(math.pi-an)/2.0
#		pm=vecRotateZ(pm,ann1)      # points to middle
		ann=(math.pi-an)/2.0
	else:
#		ann2=-(math.pi-an)/2.0
#		pm=vecRotateZ(pm,ann2)      # points to middle
		ann=-(math.pi-an)/2.0

	pm=vecRotateZ(pm,ann)
	
	if pm == 0:
		return None
	pm=vecScale(pm,0)
	pm=vecScale(pm,rad)
	pp3=vecAdd(pp1,pm)
	return (pp3[0],pp3[1],p1[2])



#############################################################################
### arcCenter180XY3P
###
### Given three tuples, this function returns a tuple containing
### the center of the arc. Stupid things might happen here.
### On error, None is returned.
### TODO: Returned z will be p1[2] for now.
#############################################################################
def arcCenter180XY3P(p1,p2,p3):
	x1, y1, z1 = p1
	x2, y2, z2 = p2
	x3, y3, z3 = p3

	ym_nom   = ( x3**2 - x1**2 + y3**2 - y1**2 ) * (x2-x1) - (x2**2 - x1**2 + y2**2 - y1**2) * (x3-x1)
	ym_denom = 2 * (  (y3-y1) * (x2-x1) - (y2-y1) * (x3-x1)  )

	if ym_denom == 0:
		print( "ERR: arcCenter180XY3P: ym_denom zero" )
		return None

	ym = ym_nom / ym_denom

	xm_nom   = ( x3**2 - x1**2 + y3**2 - y1**2 ) - 2*ym*(y3-y1)
	xm_denom = 2 * (x3-x1)

	if xm_denom == 0:
		print( "ERR: arcCenter180XY3P: xm_denom zero" )
		return None
	
	xm = xm_nom / xm_denom

	# print( "INF: arcCenter180XY3P: xm_nom  :", ym_nom )
	# print( "INF: arcCenter180XY3P: xm_denom:", ym_denom )
	# print( "INF: arcCenter180XY3P: ym_nom  :", ym_nom )
	# print( "INF: arcCenter180XY3P: ym_denom:", ym_denom )
	# print( "INF: arcCenter180XY3P: xm, ym  :", xm, ym )

	return ( xm, ym, p1[2] )


