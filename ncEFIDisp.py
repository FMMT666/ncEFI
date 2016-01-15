#!/usr/bin/python2.4


# Just playing around with python...

if __name__ == '__build__':
  raise Exception


import string
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.Tk import *
import Tkinter, sys
import pickle

from ncVec import *

__version__ = string.split('$Revision: 0.1 $')[1]
__date__    = string.join(string.split('$Date: 2007/04/12 $')[1:3], ' ')
__author__  = 'nobody <nobody@nowhere.net>'




#############################################################################
### createArc180
###
### Creates line elements that follow an arc path.
### Radius is given in x,y plane, Z will change it's height in a linear way.
### Angle is limited to 180 degrees
###
#############################################################################
def createArc180(p1,p2,rad,step,dir):
  pm=arcCenter180XY(p1,p2,rad,dir)
  
  if pm==None:
    print "ERR: createArc180: no center; p1,p2: ",p1,p2
    return []
  dArc=[]
  sta_an=vecAngleXY((p1[0]-pm[0],p1[1]-pm[1],0))
  end_an=vecAngleXY((p2[0]-pm[0],p2[1]-pm[1],0))
  spa_an=end_an-sta_an		# positive for clockwise direction

  if end_an==0.0 and dir=='cc':	# 2pi patch
    end_an=math.pi*2
    spa_an=end_an-sta_an	# positive for clockwise direction

  if sta_an==0.0 and dir =='cw':
    sta_an=2*math.pi
    spa_an=end_an-sta_an	# positive for clockwise direction

  # ToDo:
  # this sucks...
  if spa_an > math.pi + 0.01:
    spa_an=2.0*math.pi-spa_an

  if spa_an == 0.0:
    print "ERR: createArc180: no angle"
    return []

  if spa_an > math.pi + 0.01:
    spa_an-=math.pi
  else:
    if spa_an < -(math.pi+0.01):
#      print "spa_an < -(math.pi+0.01)"
#      spa_an+=math.pi
      spa_an=2.0*math.pi+spa_an

  if dir=='cw' and spa_an > 0.0 or dir=='cc' and spa_an < 0.0:
    spa_an*=-1

  stp_an=spa_an/step

  print "spa_an: ",spa_an
               
  count=2
  lp=p1			# the last point
  zs=p1[2]		# z start value
  ze=p2[2]		# z end value
  zi=(ze-zs)/step	# z increment
  bp=vecExtract((pm[0],pm[1],0),(p1[0],p1[1],0))
  for i in range(1,step+1):
    dp=vecRotateZ(bp,-i*stp_an)	# positive now means counter clockwise
    dArc.append((lp[0],lp[1],lp[2]))
    lp=(pm[0]+dp[0],pm[1]+dp[1],lp[2]+zi)
    count+=1
  dArc.append((lp[0],lp[1],lp[2]))
  return dArc




#############################################################################
### class Canvas
###
###
###
#############################################################################
class Canvas:

  ###########################################################################
  ### __init__
  ###
  ###########################################################################
  def __init__(self,master):

    self.o=Opengl(master, width = 640, height = 400, double = 1, depth = 1)
    self.o.pack(expand = 1, fill = 'both')

    glutInit(sys.argv)

    self.o.redraw = self.redraw
#    self.o.after_idle(self.bastel)
#    self.o.after(500,self.bastel)
#    self.o.pick = self.pick

    self.o.bind("<Control-Button-1>", self.select)

    self.o.set_centerpoint(0,0,0)
    self.o.set_eyepoint(30.)

    # disabled
    self.o.autospin_allowed = 0

    self.o.PartList=partlist
    self.drawall(self.o)

    





  ###########################################################################
  ### drawall
  ###
  ###########################################################################
  def drawall(self,o):

    o.grob = glGenLists(10)
    glNewList(o.grob, GL_COMPILE)

    glOrtho(-50.0, 50.0, -50.0, 50.0, 50.0, -50.0);

    glDisable(GL_DEPTH_TEST)
#    glEnable(GL_LINE_SMOOTH)
#    glClearDepth(1.0)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glClearColor(0,0,0,0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.3, 0.9, 0.3, 0.])

    # draw "axes"
    glDisable(GL_LIGHTING)

    glPushMatrix()
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(20,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,20,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,20)
    glEnd()

    glColor3f(0,1,1)
    glBegin(GL_POINTS)
    for x in range(-500,500,10):
      for y in range(-500,500,10):
        glVertex3f(x,y,0)
    glEnd()
    glPopMatrix()

    glColor3f(1,1,1)

    dNr=1

    for iPart in partlist:
      for iElem in iPart['elements']:
        if iElem['type']=='l':
          p1=iElem['p1']
          p2=iElem['p2']
          glDisable(GL_LIGHTING)
          glPushMatrix()
          glBegin(GL_LINES)
          glVertex3f(p1[0],p1[1],p1[2])
          glVertex3f(p2[0],p2[1],p2[2])
          glEnd()
          glPopMatrix()
          glEnable(GL_LIGHTING)

        if iElem['type']=='a':
          p1=iElem['p1']
          p2=iElem['p2']
          rad=iElem['rad']
          dir=iElem['dir']
          print "arc pNr: ",iElem['pNr'],p1,p2
          lines=createArc180(p1,p2,rad,20,dir)
          glDisable(GL_LIGHTING)
          glColor3f(1, 1, 1)
          glPushMatrix()
          glBegin(GL_LINES)
          for i in range(0,len(lines)-1):
            glVertex3f(lines[i][0],lines[i][1],lines[i][2])
            glVertex3f(lines[i+1][0],lines[i+1][1],lines[i+1][2])
          glEnd()
          glPopMatrix()
          glEnable(GL_LIGHTING)
          
    glEndList()
    glFlush()




  ###########################################################################
  ### drawall_pick
  ###
  ###########################################################################
  def drawall_pick(self):

    dNr=0
    glInitNames()

    for iPart in partlist:
      for iElem in iPart['elements']:
        if iElem['type']=='l':
          p1=iElem['p1']
          p2=iElem['p2']
          glPushName(dNr)
          dNr+=1
          glPushMatrix()
          glBegin(GL_LINES)
          glVertex3f(p1[0],p1[1],p1[2])
          glVertex3f(p2[0],p2[1],p2[2])
          glEnd()
          glPopMatrix()
          glPopName()

        if iElem['type']=='a':
          p1=iElem['p1']
          p2=iElem['p2']
          rad=iElem['rad']
          dir=iElem['dir']
          lines=createArc180(p1,p2,rad,20,dir)
          glPushName(dNr)
          dNr+=1
          glPushMatrix()
          glBegin(GL_LINES)
          for i in range(0,len(lines)-1):
            glVertex3f(lines[i][0],lines[i][1],lines[i][2])
            glVertex3f(lines[i+1][0],lines[i+1][1],lines[i+1][2])
          glEnd()
          glPopMatrix()
          glPopName()

    glFlush()          
#    hits=glRenderMode(GL_RENDER)
#    print "HITS: ",hits



  ###########################################################################
  ### redraw
  ###
  ###########################################################################
  def redraw(self,o):

    glClearColor(1., 0., 1., 0.)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1., 1., 1.)
    glCallList(o.grob)




  ###########################################################################
  ### pick_redraw
  ###
  ###########################################################################
  def pick_redraw(self):
    # glPushName(dElem[1])
    pass


  ###########################################################################
  ### bastel
  ###
  ###########################################################################
  def bastel(self):
    pass


  ###########################################################################
  ### pick
  ###
  ###########################################################################
  def pick(self,o, p1, p2, event=None):
    print "."
    return 1    


  ###########################################################################
  ### select
  ###
  ###########################################################################
  def select(self,event):
#    result = glSelectWithCallback(event.x,event.y, self.pick_redraw)
    result = glSelectWithCallback(event.x,event.y, self.drawall_pick)

    print "result:      ",str(result)

    if result and result[0][2]:
      sel=result[0][2][-1]
      print "SELECT: ",sel
#      for iParts in self.o.parts:
#        if iParts[0]=='geom':
#          iParts[1].sel_element_toggle(sel)

#    self.drawall(self.o)



if __name__ == '__main__':

  try:
    f=open('data.txt','r+t')
  except:
    print 'ERROR: file not found'
    sys.exit()

  try:
    partlist=pickle.load(f)
#    print partlist
  except:
    print "ERROR loading data"

  kekse=0

  f.close()

#  for i in partlist:
#    for j in i['elements']:
#      print j


#  dGeom.add_line(0,0,0,100,0,0)
#  dGeom.add_line(100,0,0,100,50,0)
#  dGeom.add_line(100,50,0,0,50,0)
#  dGeom.add_line(0,50,0,0,0,0)
#  dGeom.add_line(0,0,20,100,0,20)
#  dGeom.add_line(100,0,20,100,50,20)
#  dGeom.add_line(100,50,20,0,50,20)
#  dGeom.add_line(0,50,20,0,0,20)
  
#  dTool.add_line(0,0,0,100,50,0)
#  dTool.add_line(0,50,0,100,0,0)
  

  f=Frame(None,borderwidth='5',relief='groove')
  f.pack(side='top',expand=0,fill='both')

  mFile=Tkinter.Menubutton(f,text='File')
  mFile.pack(side='left',expand=0,fill='x')
  filemenu = Menu(mFile, tearoff=0)
  filemenu.add_command(label="Open")
  filemenu.add_command(label="Save")
  filemenu.add_separator()
  filemenu.add_command(label="Exit")

  mFile.config(menu=filemenu)

  mTool=Tkinter.Menubutton(f,text='Tools')
  mTool.pack(side='left',expand=0,fill='x')

  ff=Frame(None,cursor='crosshair',borderwidth='5',relief='groove')
  myCan=Canvas(ff)
  ff.pack(side='top',expand=1,fill='both')

  Tkinter.mainloop()

