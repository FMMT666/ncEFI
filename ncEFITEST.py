#!/usr/bin/python2.4

# MKPPCAM v0.1
# aka "Mein kleines, pisseliges Python CAM"

import string
import pickle
import math
import sys
import types
from ncVec import *


GCODE_RAPID="G00"
GCODE_LINE="G01"
GCODE_ARC_CW="G02"
GCODE_ARC_CC="G03"

GCODE_PRG_FEEDUNIT='G94 (feedrate in \'units\' per minute)'
GCODE_PRG_UNITS='G21 (units are millimeters)'
GCODE_PRG_PLANE='G17 (working in/on xy-plane)'
GCODE_PRG_PATHMODE='G64P0.05 (continuous mode with \'p\' as tolerance)'
GCODE_PRG_INIT1='T1M06'
GCODE_PRG_INIT2='G00X0Y0 S2000 M03'
GCODE_PRG_INIT3='F900'

GCODE_PRG_ENDPOS='G00X0Y0'
GCODE_PRG_END='M02'

GCODE_OP_SAVEZ='10'

TOOL_CONTINUOUS_TOLERANCE=0.001      # in units; if mm, this makes 1um...


#############################################################################
# elements
# basic geometry
# v1={'type':'v','p1':(0,0,0)}

# l1={'type':'l','p1':(0,0,0),'p2':(100,0,0)}
# l2={'type':'l','p1':(100,0,0),'p2':(100,50,0)}
# l3={'type':'l','p1':(100,50,0),'p2':(0,50,0)}
# l4={'type':'l','p1':(0,50,0),'p2':(0,0,0)}

# a1={'type':'a','p1':(0,0,0),'p2':(100,0,0),'rad':70,'dir':'cw'}
# a2={'type':'a','p1':(100,50,0),'p2':(0,50,0),'rad':70,'dir':'cw'}
# allowed extensions:
# pNr     <- number of element in part
# pNext   <- if chained -> number of next element
# pPrev   <- if chained -> number of previous element



#############################################################################
# part
# contains linked elements, _including_(!) extensions
# p1={'name':'outer','elements':[l1,l2,l3,l4]}
# p2={'name':'altc1','elements':[a1,l2,l3,l4]}
# p3={'name':'altc2','elements':[l1,l2,a2,l4]}



#############################################################################
### elemCreateVertex
###
#############################################################################
def elemCreateVertex(p1,extra={}):
  if isinstance(p1,types.TupleType) == False:
    return {}
  ret={'type':'v','p1':p1}
  for i in extra:
    if i=='pNr':
      ret['pNr']=extra['pNr']
    if i=='pNext':
      ret['pNext']=extra['pNext']
    if i=='pPrev':
      ret['pPrev']=extra['pPrev']
  return ret



#############################################################################
### elemCreateLine
###
#############################################################################
def elemCreateLine(p1,p2,extra={}):
  if isinstance(p1,types.TupleType) == False or isinstance(p2,types.TupleType) == False:
    print "ERR: elemCreateLine: p1 or p2 not tuples"
    return {}
  if p1 == p2:
    print "ERR: elemCreateLine: p1 == p2: ",p1
    return {}
  ret={'type':'l','p1':p1,'p2':p2}
  for i in extra:
    if i=='pNr':
      ret['pNr']=extra['pNr']
    if i=='pNext':
      ret['pNext']=extra['pNext']
    if i=='pPrev':
      ret['pPrev']=extra['pPrev']
  return ret

  
  
#############################################################################
### elemCreateArc180
###
### While rad is taken from a projection to the xy-plane, z may vary but
### will be stepped through linear.
#############################################################################
def elemCreateArc180(p1,p2,rad,dir,extra={}):
  # ToDo:
  # - precision hack sucks...
  if isinstance(p1,types.TupleType) == False or isinstance(p2,types.TupleType) == False:
    print "ERR: elemCreateArc180: no tuples"
    return {}
  if p1 == p2:
    print "ERR: elemCreateArc180: p1==p2: ", p1,p2
    return {}
  if isinstance(dir,types.StringType) == False:
    print "ERR: elemCreateArc180: invalid dir format: ",dir
    return {}
  if dir != 'cw' and dir != 'cc':
    print "ERR: elemCreateArc180: invalid dir command: ",dir
    return {}
  dist=vecLength((p1[0],p1[1],0),(p2[0],p2[1],0))
  if rad < dist/2.0:
    # "precision" hack:
#    if rad+0.0000001 > dist/2.0:
#      rad+=0.0000001
    if rad+RADTOL > dist/2.0:
      rad+=RADTOL
    else:
      print "ERR: elemCreateArc180: rad less than dist/2: rad, dist/2",rad,dist/2.0
      return {}
  ret={'type':'a','p1':p1,'p2':p2,'rad':rad,'dir':dir}
  for i in extra:
    if i=='pNr':
      ret['pNr']=extra['pNr']
    if i=='pNext':
      ret['pNext']=extra['pNext']
    if i=='pPrev':
      ret['pPrev']=extra['pPrev']
  return ret



def elemCreateArc360(p1,p2,rad,dir):
  pass

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




def elemRotate(elem, ang):
  pass


#############################################################################
### elemMove
###
#############################################################################
def elemMove(elem, vec):
  elemn={}
  for i in elem:
    elemn[i]=elem[i]
  # every element has 'p1':
  p1=vecAdd(elemn['p1'],vec)
  elemn['p1']=p1

  if elem.has_key('p2'):
    p2=vecAdd(elemn['p2'],vec)
    elemn['p2']=p2

  return elemn



#############################################################################
### elemReverse
###
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
      if 0.0 <= di2 <= 1.0:
        return [[di,isp]]
    return []

  # line on arc
  if e1['type']=='l' and e2['type']=='a':
    pm=arcCenter180XY(e2['p1'],e2['p2'],e2['rad'],e2['dir'])
    if pm == None:
      return []
    isp=vecArcIntersectXY(e1['p1'],e1['p2'],pm,e2['rad'])
#    print "l on a hits: ",isp
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
#    print "a on l hits: ",isp
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
#    print "a on a hits: ",isp
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

  if e1['type'] == 'l':
    print "LINE %4d: (%8.3f %8.3f %8.2f) (%8.3f %8.3f %8.3f)" % (e1['pNr'], \
      e1['p1'][0],e1['p1'][1],e1['p1'][2],e1['p2'][0],e1['p2'][1],e1['p2'][2])
    return

  if e1['type'] == 'a':
    print "ARC  %4d: (%8.3f %8.3f %8.2f) (%8.3f %8.3f %8.3f) %8.3f %s" % (e1['pNr'], \
      e1['p1'][0],e1['p1'][1],e1['p1'][2],e1['p2'][0],e1['p2'][1],e1['p2'][2],e1['rad'],e1['dir'])
    return
  
  print "UEO  %4d of type %c " % (e1['pNr'],e1['type'])




def elemFindLinked(elem):
  pass
  



#############################################################################
### partCreate
###
#############################################################################
def partCreate(name, extras={}):
  if isinstance(name,types.StringType) == False:
    return {}
  if len(name)<1:
    return {}
  ret={'name':name,'elements':[]}
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
        print "ERR: partCheckUniqueNumbers: already found nr: ",part['elements'][i]['pNr']
        return False
      else:
        nrFound.append(part['elements'][0]['pNr'])
    else:
      print "ERR: partCheckUniqueNumbers: element without \'pNr\' tag found!"
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
    if i.has_key('pNr'):
      if i['pNr'] > nr:
        nr=i['pNr']
        el=i
  if len(el) == 0:
    return None
  if el.has_key('p2'):
    return el['p2']
  if el.has_key('p1'):
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
  if el.has_key('p2'):
    return el['p2']
  if el.has_key('p1'):
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
  if el.has_key('p1'):
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
    print "ERR: partCheckContinuous: no elements in part!"
    return False
  if len(li) == 1:
    return True
  e1=partGetElement(part,li[0])
  if e1['type']=='v':
    print "ERR: partCheckContinuous: vertex found!"
    return False
  for i in range(1,len(li)):
    e2=partGetElement(part,li[i])
    if e2['type']=='v':
      print "ERR: partCheckContinuous: vertex found!"
      return False
    if not e1['p2']==e2['p1']:
      ez=math.fabs(vecLength(e1['p2'],e2['p1']))
      if ez > TOOL_CONTINUOUS_TOLERANCE:
        print "ERR: partCheckContinuous: p2!=p1 at number: ",i
        print "                        : e1['p2']: ",e1['p2']
        print "                        : e2['p1']: ",e2['p1']
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
    print "ERR: geomCreateHelix: depth == 0"
    return []
  if depthSteps < 1.0:
    print "ERR: geomCreateHelix: steps < 0"
    return []
  if dia <= 0.0:
    print "ERR: geomCreateHelix: dia <= 0"
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
    print "ERR: geomCreateHelix: skipped one or more arcs (helix)"
    return[]

  if finish=='finish':
    el=elemCreateArc180(p1,p2,dia/2.0,dir,{'pNr':nr})
    nr+=1
    if el==[]:
      print "ERR: geomCreateHelix: skipped first finishing arc"
      return []
    hel.append(el)

    el=elemCreateArc180(p2,p1,dia/2.0,dir,{'pNr':nr})
    nr+=1
    if el==[]:
      print "ERR: geomCreateHelix: skipped second finishing arc"
      return []
    hel.append(el)
  # end if 'finish'

  return hel
    


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
    print "ERR: geomCreateConcentricCircles: diaStart <= 0"
    return []
  if diaEnd <= 0.0:
    print "ERR: geomCreateConcentricCircles: diaStart <= 0"
    return []
  if diaSteps < 1:
    print "ERR: geomCreateConcentricCircles: diaSteps < 1"
    return []
  diaPerRev=(diaEnd-diaStart)/diaSteps
  y=p1[1]
  z=p1[2]
  if basNr==0:
    nr=1
  else:
    nr=basNr
  for i in range(0,diaSteps):
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
    print "ERR: geomCreateConcentricCircles: number of circles: needed vs. made. ",nr-1,len(con)
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
    print "ERR: geomCreateCircRingHole: depth <= 0 :",depth
    return []
  if depthSt < 1:
    print "ERR: geomCreateCircRingHole: depthSt < 1 :",depthSt
    return []
  if hDepth < 0:
    print "ERR: geomCreateCircRingHole: hDepth < 0 :",hDepth
    return []
  if hDepthSt < 1:
    print "ERR: geomCreateCircRingHole: hDepthSt < 1 :",hDepthSt
    return []
  if clear < p1[2]:
    print "ERR: geomCreateCircRingHole: clear < workpos :",clear,p1[2]
    return []
  if diaStart <= 0:
    print "ERR: geomCreateCircRingHole: diaStart < 0 :",diaStart
    return []
  if diaEnd <= 0:
    print "ERR: geomCreateCircRingHole: diaStart < 0 :",diaEnd
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
      print "ERR: geomCreateCircRingHole: error creating helix"
      return []
    # we are now on pWork(x,y) but already cut depth/depthSt of the material
    for j in hel:
      ccrh.append(j)
    nr+=len(hel)
  
    pWork=(p1[0]-(diaStart/2.0),p1[1],p1[2]-((i+1)*(depth/(depthSt*1.0))))
    poc=geomCreateConcentricCircles(pWork,diaStart,diaEnd,diaSt,dir,nr)
    if poc==[]:
      print "ERR: geomCreateCircRingHole: error creating concentric circles"
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
        print "ERR: geomCreateCircRingHole: error creating helix back line 1 in: ",i
        return []
      ccrh.append(lin)
      pWork1=pWork2
      pWork2=(p1[0]-(diaStart/2.0),p1[1],p1[2]+hDepth-((i+2)*(depth/(depthSt*1.0))))
      lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
      nr+=1
      if lin==[]:
        print "ERR: geomCreateCircRingHole: error creating helix back line 2 in: ",i
        return []
      ccrh.append(lin)
    else:
      # now, "back" to the starting point
      pWork1=partGetLastPositionFromElements(poc)
      pWork2=(pWork1[0],pWork1[1],pWork1[2]+(i+1)*(depth/(depthSt*1.0)))
      lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
      nr+=1
      if lin==[]:
        print "ERR: geomCreateCircRingHole: error creating back line 1"
        return []
      ccrh.append(lin)
      pWork1=pWork2
      pWork2=(p1[0]-(diaStart/2.0),p1[1],p1[2]+hDepth-((depth/(depthSt*1.0))))
      lin=elemCreateLine(pWork1,pWork2,{'pNr':nr})
      nr+=1
      if lin==[]:
        print "ERR: geomCreateCircRingHole: error creating back line 2"
        return []
      ccrh.append(lin)
  return ccrh



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
    print "ERR: geomCreateContour: part not continuous"
    return []
  if dist==0.0:
    print "ERR: geomCreateContour: distance is 0"
    return []
  # ToDo:
  partIsClosed=partCheckClosed(part)

  CoarseCont=[]

  for i in range(1,len(part['elements'])+1):
    el=partGetElement(part,i)
    if el==[]:
      print "ERR: geomCreateContour: empty element at pos.: ",i
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
      eln=elemMove(el,vecN)

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
    print "ERR: geomCreateSlotContour: distance is 0"
    return []
  
  if basNr==0:
    Nr=1
  else:
    Nr=basNr

  slo=[]

  for i in range(1,len(part['elements'])+1):
    el=partGetElement(part,i)
    if el==[]:
      print "ERR: geomCreateSlotContour: empty element at pos.: ",i
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
    print "ERR: geomCreateSlotContourFromElement: distance is 0"
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
      print "ERR: geomCreateSlotContourFromElement: no length in xy-plane projection"
      return []
    if not el['p1'][2] == el['p2'][2]:
      print "ERR: geomCreateSlotContourFromElement: element not in xy-plane or parallel: ",el
      return []
    
    if dist < 0.0:
      an=-math.pi/2.0
    else:
      an=math.pi/2.0
    vecN=vecRotateZ(vecL,an)
    vecN=vecScale(vecN,0)
    vecN=vecScale(vecN,math.fabs(dist))
    l1=elemMove(el,vecN)
    l2=elemMove(el,vecReverse(vecN))
    l2=elemReverse(l2)
    if dist < 0.0:
      dir='cw'
    else:
      dir='cc'

    a1=elemCreateArc180(l1['p2'],l2['p1'],math.fabs(dist),dir,{'pNr':0})
    a2=elemCreateArc180(l2['p2'],l1['p1'],math.fabs(dist),dir,{'pNr':0})

    if a1==[] or a2==[]:
      print "ERR: geomCreateSlotContourFromElement: error creating a1 with dir: ",dir
      if a1==[]:
        print "ERR: geomCreateSlotContourFromElement: error creating a1: ",l1['p2'],l2['p1']
      else:
        print "ERR: geomCreateSlotContourFromElement: error creating a2: ",l2['p2'],l1['p1']
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
      print "ERR: geomCreateSlotContourFromElement: unable to calc arc mispoint from: ",el
      return []

    vec1=vecExtract(el['p1'],pm)
    vec1=(vec1[0],vec1[1],0)
    vec2=vecExtract(el['p2'],pm)
    vec2=(vec2[0],vec2[1],0)
    if vecLength(vec1) <= 0.0 or vecLength(vec2) <= 0.0:
      print "ERR: geomCreateSlotContourFromElement: no length in xy-plane projection"
      return []
    if not el['p1'][2] == el['p2'][2]:
      print "ERR: geomCreateSlotContourFromElement: element not in xy-plane or parallel: ",el
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
      if a1.has_key('p2'):   # could be a vertex
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
      if a2.has_key('p2'):   # could be a vertex
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
    if elOut[i].has_key('p2'):
      elOut[i+1]['p1']=elOut[i]['p2']
    else:
      elOut[i+1]['p1']=elOut[i]['p1']
    
  if isClosed != 'notClosed':
    if elOut[maxLen].has_key('p2'):
      elOut[0]['p1']=elOut[maxLen]['p2']
    else:
      elOut[0]['p1']=elOut[maxLen]['p1']

  return elOut



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
    print "ERR: geomCreateLeftContour: distance is not negative: ",dist
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
      print "ERR: geomCreateLeftContour: empty element at pos.: ",i
      return []

    # create a slot around the first element
    slo1=geomCreateSlotContourFromElement(el1,dist)
    if slo1==[]:
      print "ERR: geomCreateLeftContour: unable to create slot for first element: ",i
      return []

    if len(slo1)!=4:
      print "ERR: geomCreateLeftContour: slot has less than 4 elements for first elem: ",i
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
      print "ERR: geomCreateLeftContour: empty element at pos.: ",i+1
      return []

    # create a slot around the second element
    slo2=geomCreateSlotContourFromElement(el2,dist)
    if slo2==[]:
      print "ERR: geomCreateLeftContour: unable to create slot for second element: ",i
      return []

    if len(slo2)!=4:
      print "ERR: geomCreateLeftContour: slot has less than 4 elements for second elem: ",i
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
    print "*** angle: i,ang: ",i,ang*360/(2.0*math.pi)
    if ang==None:
      print "ERR: geomCreateLeftContour: no angle after element: ",i
      return []

    # easy operations first =)
    if math.fabs(ang) < RADTOL:
      print "op == 0"
      ee=elemCopy(slo1[0])
      ee['p2']=slo2[0]['p1']
      ee['pNr']=conNr
      conNr+=1
      con.append(ee)

    if ang <= -RADTOL:
      print "op < 0"
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
      print "op > 0"

#     old style
#      hi=elemIntersectsElemXY(slo1[0],slo2[0])
#      print "hi: ",hi

      hi=elemIntersectsElemXY(slo1[0],slo2[1])
      hiX=1
      print "hi(1): ",hi
      elemDebugPrint(slo1[0])      
      elemDebugPrint(slo2[1])

      if hi==[]:
        hi=elemIntersectsElemXY(slo1[0],slo2[0])
        hiX=2
        print "hi(0): ",hi
        elemDebugPrint(slo1[0])      
        elemDebugPrint(slo2[0])

      if hi==[]:
        print "ERR: geomCreateLeftContour: no intersections on left turn at elem nr: ",i
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
    print "ERR: geomCreateLeftContour: error while creating slot elements from part "
    return []

  slo=geomExtractSlotDirVecs(slo)
  
  print "len(slo): ",len(slo)

  # process all elements in the list
  for i in range(len(slo)):

    if i < conSkip:
      print "."
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
      print "**********"
      print "*** NR ***",i
      elemDebugPrint(slo[i])
  #    print "len",len(his)
      
      for j in his:
        print j

      sdi=999999999999999.9
      eleCount=0
      eleTarget=None
      eleInt=None
      
      for j in his:
        for k in j:
          print "k[0] / sdi ",k[0]," / ",sdi
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
      
      print "FOUND El Nr:  ",eleTarget
      print "FOUND eleInt: ",eleInt

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
    print "ERR: toolRapidToNextPart: part has no first point"
    return []
    
  if part.has_key('name'):
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
    print "ERR: toolCreateFromPart: part \""+part['name']+"\" not continuous"
    return []

  # If "partCheckContinuous" returned no error, it should (SHOULD!) be
  # ok to skip further tests concerning the geometry...
  part=partRenumber(part)
  
  if part.has_key('name'):
    tops.append('('+part['name']+')')
  else:
    tops.append('(unnamed part)')

  lastCmd=''
  for i in range(1,len(part['elements'])+1):
    el=partGetElement(part,i)
    if len(el)==0:
      print "ERR: toolCreateFromPart: partGetElement returned zero length at ",i
      return[]
      
    if not el.has_key('type'):
      print "ERR: toolCreateFromPart: element nr. ",i," has no \'type\' attribute"
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
      print "ERR: toolCreateFromPart: empty nc-code line at: ",el
      return[]
    
    tops.append(cxyz)

  return tops



if __name__ == '__main__':
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



  f=open('gcode.nc','w+t')
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

  print "p1 closed :",partCheckClosed(p1)

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
  #  print "i: ",i," -> ",ips


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

  f=open('data.txt','w+t')
  pickle.dump(partlist,f)
  f.close()

  print "SLOT CONTOUR:"
  for i in p62['elements']:
    print i
