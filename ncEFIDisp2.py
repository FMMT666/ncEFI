#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from OpenGL.GLUT import *
from OpenGL.GLU  import *
from OpenGL.GL   import *
from wx.glcanvas import GLCanvas
from ncVec       import *
import wx
import pickle
import math


MOUSE_ZOOM_FACTOR_WHEEL   = 0.1
MOUSE_DRAG_FACTOR         = 0.001

ARC_LINES_INTERPOLATION   = 10    # arcs are drawn with lines; this specifies how many are used per 180°

DRAW_GRID_SIZE            = 1.0
DRAW_GRID_COLOR           = ( 0.0, 0.5, 1.0 )

DRAW_VERTEX_SIZE          = 5.0
DRAW_VERTEX_COLOR         = ( 0.8, 0.8, 0.0 )
DRAW_VERTEX_COLOR_ENGAGE  = ( 1.0, 0.0, 0.0 )
DRAW_VERTEX_COLOR_NORMAL  = ( 0.7, 0.7, 0.0 )
DRAW_VERTEX_COLOR_RETRACT = ( 0.0, 1.0, 0.0 )
DRAW_LINE_SIZE            = 1.0
DRAW_LINE_COLOR           = ( 0.8, 0.8, 0.8 )
DRAW_ARC_SIZE             = 1.0
DRAW_ARC_COLOR            = ( 0.8, 0.8, 0.8 )



# TODO
#  - check if 'tColor' is a tuple with 3 elements; could be used for highlighting, color cycling or other stuff
#  - maybe rename cbCheckAutoRefresh to better reflect what it does, cycling the colors
#  - implement color cycling for some parts; to improve debug & visibility
#  - ...


# everyone loves global vars <3
PartList = None



#############################################################################
### createArc180
###
### Creates line elements that follow an arc path.
### Radius is given in x,y plane, Z will change it's height in a linear way.
### Angle is limited to 180 degrees
### Todo: This is slooow if many arc are in the part list.
#############################################################################
def createArc180(p1,p2,rad,step,dir):
	pm=arcCenter180XY(p1,p2,rad,dir)

	if pm==None:
		print( "ERR: createArc180: no center; p1,p2: ",p1,p2 )
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
		print( "ERR: createArc180: no angle" )
		return []

	if spa_an > math.pi + 0.01:
		spa_an-=math.pi
	else:
		if spa_an < -(math.pi+0.01):
#			print( "spa_an < -(math.pi+0.01)" )
#			spa_an+=math.pi
			spa_an=2.0*math.pi+spa_an

	if dir=='cw' and spa_an > 0.0 or dir=='cc' and spa_an < 0.0:
		spa_an*=-1

	stp_an=spa_an/step

#	print( "spa_an: ",spa_an )

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





#===================================================================================================
class myGLCanvas(GLCanvas):
	def __init__(self, *args, **kwargs):

		# TODO: probably not necessary (needs testing)
		glutInit(['lmfao'])

		GLCanvas.__init__(self, *args, **kwargs)
		self.Bind(wx.EVT_PAINT,          self.OnPaint)
		self.Bind(wx.EVT_SIZE,           self.OnResize)
		self.Bind(wx.EVT_LEFT_DOWN,      self.OnLeftDown)
		self.Bind(wx.EVT_RIGHT_DOWN,     self.OnRightDown)
		self.Bind(wx.EVT_LEFT_UP,        self.OnLeftUp)
		self.Bind(wx.EVT_RIGHT_UP,       self.OnRightUp)
		self.Bind(wx.EVT_MOTION,         self.OnMouse)
		self.Bind(wx.EVT_MOUSEWHEEL,     self.OnWheel)
		# self.Bind(wx.EVT_CLOSE,          self.OnClose) # not working in macOS (not sure about others)
		# self.Bind(wx.EVT_WINDOW_DESTROY, self.OnClose)

		self.init = False
		self.width, self.height = self.GetSize()

		self.alpha     = 0
		self.beta      = 0
		self.distance  = 100.0

		self.viewX = 0
		self.viewY = 0
		self.viewZ = 0

		self.oldX = 0
		self.oldY = 0
		self.oldZ = 0

		self.leftDown  = False
		self.rightDown = False

		self.colorCycling = False



	################################################################################################
	### DrawAxes
	################################################################################################
	def DrawAxes(self):
		glBegin(GL_LINES)
		# x axis
		glColor3f( 1, 0, 0 )
		glVertex3f( 0, 0, 0 )
		glVertex3f( 20, 0, 0 )
		# y axis
		glColor3f( 0, 1, 0 )
		glVertex3f( 0, 0, 0 )
		glVertex3f( 0, 20, 0 )
		# z axis
		glColor3f( 0, 0, 1 )
		glVertex3f( 0, 0, 0 )
		glVertex3f( 0, 0, 20 )
		glEnd()

		# labes for the axes (looks a bit stupid :)
		# glColor3f( 1.0, 1.0, 0.0 )
		# glRasterPos3f( 22, 0.0, 0.0 )
		# glutBitmapCharacter( GLUT_BITMAP_9_BY_15, ord('x') )
		# glRasterPos3f( 0.0, 22, 0.0 )
		# glutBitmapCharacter( GLUT_BITMAP_9_BY_15, ord('y') )
		# glRasterPos3f( 0.0, 0.0, 22 )
		# glutBitmapCharacter( GLUT_BITMAP_9_BY_15, ord('z') )


	################################################################################################
	### DrawElement
	################################################################################################
	def DrawElement(self, elem ):

		# TODO: Actually it's not a super brilliant idea to have the colors in here.
		#       Especially if (at any later point of development) parts or geometries
		#       can be selected, this is more than hindering.
		#       Mhh, otherwise one could use the 'extra' parameters for this ...
		#
		#       Upd.:
		#       Now it is an extra parameter, see ['tColor'].
		#       Unfortunatly, I now had the brilliant idea to also implement a "color cycling" feature.
		#       This might require a major overhaul of the color handling (and probably everything else too, lol).
		#       Also: The viewer also supports pure "geoms", lists of elements without a part tag ('p').
		#       To make color cycling work for specific elements, it would be necessary to add a tag to the elements.

		if elem['type']=='v':
			p1 = elem['p1']
			glDisable(GL_LIGHTING)
			if 'tSize' in elem:
				glPointSize( elem['tSize'] )
			else:
				glPointSize( DRAW_VERTEX_SIZE )
			if 'tColor' in elem:
				glColor3f( elem['tColor'][0], elem['tColor'][1], elem['tColor'][2] )
			elif 'tFeed' in elem:
				if   elem['tFeed'] == "FEED_ENGAGE":
					glColor3f( DRAW_VERTEX_COLOR_ENGAGE[0], DRAW_VERTEX_COLOR_ENGAGE[1], DRAW_VERTEX_COLOR_ENGAGE[2] )
				elif elem['tFeed'] == "FEED_NORMAL":
					glColor3f( DRAW_VERTEX_COLOR_NORMAL[0], DRAW_VERTEX_COLOR_NORMAL[1], DRAW_VERTEX_COLOR_NORMAL[2] )
				elif elem['tFeed'] == "FEED_RETRACT":
					glColor3f( DRAW_VERTEX_COLOR_RETRACT[0], DRAW_VERTEX_COLOR_RETRACT[1], DRAW_VERTEX_COLOR_RETRACT[2] )
				else:
					glColor3f( DRAW_VERTEX_COLOR[0], DRAW_VERTEX_COLOR[1], DRAW_VERTEX_COLOR[2] )
			else:
				glColor3f( DRAW_VERTEX_COLOR[0], DRAW_VERTEX_COLOR[1], DRAW_VERTEX_COLOR[2] )
			glPushMatrix()
			glBegin(GL_POINTS)
			glVertex3f(p1[0],p1[1],p1[2])
			glEnd()
			glPopMatrix()
			glEnable(GL_LIGHTING)

		if elem['type'] == 'l':
			p1 = elem['p1']
			p2 = elem['p2']
			glDisable(GL_LIGHTING)
			if 'tSize' in elem:
				glLineWidth( elem['tSize'] )
			else:
				glLineWidth( DRAW_LINE_SIZE )
			if 'tColor' in elem:
				glColor3f( elem['tColor'][0], elem['tColor'][1], elem['tColor'][2] )
			else:
				glColor3f( DRAW_LINE_COLOR[0], DRAW_LINE_COLOR[1], DRAW_LINE_COLOR[2] )
			glPushMatrix()
			glBegin(GL_LINES)
			glVertex3f(p1[0],p1[1],p1[2])
			glVertex3f(p2[0],p2[1],p2[2])
			glEnd()
			glPopMatrix()
			glEnable(GL_LIGHTING)

		if elem['type'] == 'a':
			p1 = elem['p1']
			p2 = elem['p2']
			rad = elem['rad']
			dir = elem['dir']
			# TODO: adapt number of lines according to diameter (waste of resources)
			lines = createArc180(p1,p2,rad,ARC_LINES_INTERPOLATION,dir)
			glDisable(GL_LIGHTING)
			glLineWidth( DRAW_ARC_SIZE )
			if 'tColor' in elem:
				glColor3f( elem['tColor'][0], elem['tColor'][1], elem['tColor'][2] )
			else:
				glColor3f( DRAW_ARC_COLOR[0], DRAW_ARC_COLOR[1], DRAW_ARC_COLOR[2] )
			glPushMatrix()
			glBegin(GL_LINES)
			for i in range(0,len(lines)-1):
				glVertex3f(lines[i][0],lines[i][1],lines[i][2])
				glVertex3f(lines[i+1][0],lines[i+1][1],lines[i+1][2])
			glEnd()
			glPopMatrix()
			glEnable(GL_LIGHTING)


	################################################################################################
	### DrawPartList
	### 
	### For debug purposes, this now also supports elements in directories and elements in lists.
	################################################################################################
	def DrawPartList(self):
		for iPart in PartList:
			if iPart == {}:
				continue
			# check if that's something we know
			if 'type' not in iPart:
				# that's super ugly, yes; also not sure whether or not this works in all cases
				if isinstance(iPart,list) and len(iPart) > 0:
					for unp in iPart:
						if 'type' in unp:
							if unp['type'] == 'v' or unp['type'] == 'l' or unp['type'] == 'a':
									self.DrawElement(unp)
				continue
			if iPart['type'] != 'p':
				# this seems to be an element, not a part list
				if iPart['type'] == 'v' or iPart['type'] == 'l' or iPart['type'] == 'a':
					self.DrawElement(iPart)
				else:
					continue
			else:
				# this could use some additional error checks, but well ...
				for iElem in iPart['elements']:
					self.DrawElement(iElem)

	#-----------------------------------------------------------------------------------------------
	def SetColorCycling(self, cyclingOn: bool) -> None:
		self.colorCycling = cyclingOn

	#-----------------------------------------------------------------------------------------------
	def GetColorCycling(self) -> bool:
		return self.colorCycling

	#-----------------------------------------------------------------------------------------------
	def OnDraw(self):

		# DEBUG
		print("OnDraw")

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
		glEnable ( GL_COLOR_MATERIAL )
		glDisable( GL_LIGHTING )

		#---------------------------------
		# draw the axes
		glLineWidth(3)
		self.DrawAxes()

		#---------------------------------
		# draw the grid
		glPointSize( DRAW_GRID_SIZE )
		glColor3f( DRAW_GRID_COLOR[0], DRAW_GRID_COLOR[1], DRAW_GRID_COLOR[2] )
		glBegin(GL_POINTS)
		for x in range(-100,110,10):
			for y in range(-100,110,10):
				glVertex3f(x,y,0)
		glEnd()

		#---------------------------------
		# draw parts
		if PartList is not None:
			glLineWidth(2)
			glPointSize(4)
			glColor3f( 0.8, 0.8, 0.8)
			self.DrawPartList()

		self.SwapBuffers()

	#-----------------------------------------------------------------------------------------------
	def ChangeView(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		# --- ORIGINAL
		# glTranslate(self.viewX, self.viewY, -self.distance)
		# glRotate(-90, 0.0, 1.0, 0.0)
		# glRotate(-90, 1.0, 0.0, 0.0)
		# glRotate(self.alpha, 0.0, 0.0, 1.0)
		# glRotate(self.beta, 0.0, 1.0, 0.0)

		# --- Z Up, but translation is done along the axes, not the viewport; a bit weird
		# glTranslate(self.viewX, self.viewY, -self.distance)
		# glTranslate(-self.viewX, -self.viewY, 0)
		# glRotate(self.beta, 1.0, 0.0, 0.0)
		# glRotate(90, 1.0, 0.0, 0.0)
		# glRotate(self.alpha, 0.0, 1.0, 0.0)
		# glRotate(-90, 1.0, 0.0, 0.0)
		# glTranslate(self.viewX, self.viewY, 0)

		# --- same as above with with redundant code removed
		# glTranslate(self.viewX, self.viewY, -self.distance)
		# glTranslate(-self.viewX, -self.viewY, 0)
		# glRotate(self.beta, 1.0, 0.0, 0.0)
		# glRotate(self.alpha, 0.0, 0.0, 1.0)
		# glTranslate(self.viewX, self.viewY, 0)


		# --- lol feck this; that's exactly the same shit as above 😭
		# gluLookAt( -self.viewX,-self.viewY,self.distance,    -self.viewX,-self.viewY,0,     0,1,0)
		# glTranslate(-self.viewX, -self.viewY, 0)
		# glRotate( self.beta, 1,0,0 )
		# glRotate(90, 1.0, 0.0, 0.0)
		# glRotate( self.alpha, 0,1,0 )
		# glRotate(-90, 1.0, 0.0, 0.0)
		# glTranslate(self.viewX, self.viewY, 0)

		# --- KEEP THIS
		oX =  self.viewX
		oY =  self.viewY
		nX =  self.viewX * math.cos( math.radians(self.alpha) ) + self.viewY * math.sin( math.radians(self.alpha) )
		nY = -self.viewX * math.sin( math.radians(self.alpha) ) + self.viewY * math.cos( math.radians(self.alpha) )

		# --- ok; not good, has some issues but somewhat working
		#  - if rotated, the translation follows the model coordinates and not the screen
		#  - if z is negative, translation is inverted
		glTranslate(self.viewX, self.viewY, -self.distance)
		glTranslate(-self.viewX, -self.viewY, 0)
		glRotate(self.beta, 1.0, 0.0, 0.0)
		glRotate(self.alpha, 0.0, 0.0, 1.0)
		glTranslate(self.viewX, self.viewY, self.viewZ)

		# a = (GLfloat * 16)()
		# mvm = glGetFloatv(GL_MODELVIEW_MATRIX, a)
		# print( list(a) )

		self.OnDraw()


	#-----------------------------------------------------------------------------------------------
	def Resize(self):

		ratio = float(self.width) / self.height

		self.SetCurrent(self.context)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glViewport(0, 0, self.width, self.height)
		gluPerspective(45, ratio, 1, 10000)

		self.ChangeView()

	#-----------------------------------------------------------------------------------------------
	def OnPaint(self, event):
		wx.PaintDC(self)

		self.SetCurrent(self.context)

		if not self.init:
			self.InitGL()
			self.init = True
		self.OnDraw()

	#-----------------------------------------------------------------------------------------------
	def OnLeftDown(self, event):
		self.oldX, self.oldY = event.GetPosition()
		self.leftDown = True

	def OnRightDown(self, event):
		self.oldX, self.oldY = event.GetPosition()
		self.rightDown = True

	def OnLeftUp(self, event):
		self.leftDown = False

	def OnRightUp(self, event):
		self.rightDown = False

	def OnMouse(self, event):
		if self.leftDown or self.rightDown:
			X, Y = event.GetPosition()

			if self.rightDown:
				xadd = (X - self.oldX) * self.distance * MOUSE_DRAG_FACTOR
				yadd = (Y - self.oldY) * self.distance * MOUSE_DRAG_FACTOR
				self.viewX += xadd * math.cos( math.radians( self.alpha ) ) - ( yadd * math.sin( math.radians( self.alpha ) ) ) * math.cos( math.radians( self.beta ) )
				self.viewY -= xadd * math.sin( math.radians( self.alpha ) ) + ( yadd * math.cos( math.radians( self.alpha ) ) ) * math.cos( math.radians( self.beta ) )
				self.viewZ += yadd * math.sin( math.radians( self.beta ) )

			if self.leftDown:
				self.alpha += (X - self.oldX) * 0.5
				self.beta  += (Y - self.oldY) * 0.5

			self.ChangeView()
			self.oldX, self.oldY = X, Y


	def OnWheel(self, event):
		scrollFac = abs( self.distance * MOUSE_ZOOM_FACTOR_WHEEL )
		if scrollFac < 1:
			scrollFac = 1
		if event.GetWheelRotation() > 0:
			self.distance -= scrollFac
		else:
			self.distance += scrollFac

		self.ChangeView()



	#-----------------------------------------------------------------------------------------------
	def OnResize( self, e ):
		self.width, self.height = e.GetSize()
		self.Resize()


	#-----------------------------------------------------------------------------------------------
	# def OnClose( self, e ):
	# 	self.Destroy()


	#-----------------------------------------------------------------------------------------------
	def InitGL( self ):
		glLightfv( GL_LIGHT0, GL_DIFFUSE,  (0.8, 0.8, 0.8, 1.0) )
		glLightfv( GL_LIGHT0, GL_AMBIENT,  (0.2, 0.2, 0.2, 1.0) )
		glLightfv( GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0 ))
		glEnable( GL_LIGHT0)

#		glShadeModel( GL_SMOOTH )
		glEnable( GL_LIGHTING )
		glEnable( GL_DEPTH_TEST )
		glClearColor( 0.0, 0.0, 0.0, 1.0 )
		glClearDepth( 1.0 )

		self.Resize()

#===================================================================================================
class ToolPanel(wx.Panel):
	def __init__(self, parent, canvas, *args, **kwargs):

		# for the timer
		self.mainWin = parent

		wx.Panel.__init__(self, parent, *args, **kwargs)
		self.canvas = canvas

		self.button1        = wx.Button  ( self, label="Button 1" )
		self.button2        = wx.Button  ( self, label="Button 2" )
		self.button3        = wx.Button  ( self, label="Button 3" )
		self.button4        = wx.Button  ( self, label="Button 4" )
		self.button5        = wx.Button  ( self, label="Button 5" )
		self.chkAutoRefresh = wx.CheckBox( self, label="Colorcycle" )

		self.Bind(wx.EVT_CHECKBOX,       self.cbCheckAutoRefresh)
		# self.Bind(wx.EVT_CLOSE,          self.OnClose) # not working in macOS (not sure about others)
		# self.Bind(wx.EVT_WINDOW_DESTROY, self.OnClose)

		self.sizer = wx.BoxSizer( wx.VERTICAL )

		self.sizer.Add( self.button1, flag=wx.BOTTOM, border=5 )
		self.sizer.Add( self.button2, flag=wx.BOTTOM, border=5 )
		self.sizer.Add( self.button3, flag=wx.BOTTOM, border=5 )
		self.sizer.Add( self.button4, flag=wx.BOTTOM, border=5 )
		self.sizer.Add( self.button5, flag=wx.BOTTOM, border=5 )
		
		self.sizer.Add( self.chkAutoRefresh )

		self.border = wx.BoxSizer()
		self.border.Add( self.sizer, flag=wx.ALL | wx.EXPAND, border=5 )

		self.SetSizerAndFit(self.border)

	#-----------------------------------------------------------------------------------------------
	def cbCheckAutoRefresh(self, e):

		if self.chkAutoRefresh.IsChecked():
			self.mainWin.canvas.SetColorCycling( True )
			self.mainWin.timer.Start(100)
		else:
			self.mainWin.canvas.SetColorCycling( False )
			self.mainWin.timer.Stop()

	#-----------------------------------------------------------------------------------------------
	def OnClose( self, e ):
	# 	self.Destroy()
		pass


#===================================================================================================
class MainWin(wx.Frame):
	def __init__(self, *args, **kwargs):
		wx.Frame.__init__(self, title='OpenGL', *args, **kwargs)

		self.Bind(wx.EVT_CLOSE,          self.OnClose) # not working in macOS (not sure about others)
		self.Bind(wx.EVT_WINDOW_DESTROY, self.OnClose)

		self.canvas = myGLCanvas(self, size=(640, 480))

		self.context = wx.glcanvas.GLContext(self.canvas)
		self.canvas.context = self.context

		self.panel = ToolPanel(self, canvas=self.canvas)

		self.sizer = wx.BoxSizer()

		self.sizer.Add(self.panel, 0, wx.EXPAND)
		self.sizer.Add(self.canvas, 1, wx.EXPAND)

		self.SetSizerAndFit(self.sizer)


		# TODO: new timer for color cycling or other animations
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer)


		self.Show()


	#-----------------------------------------------------------------------------------------------
	def OnTimer(self, event):

		# DEBUG
		# print("timer triggered")

		self.canvas.Refresh()


	#-----------------------------------------------------------------------------------------------
	def OnClose( self, e ):
		self.timer.Stop()
#		self.panel.Destroy()
#		self.sizer.Destroy()
#		self.canvas.Destroy()
		self.Destroy()

		pass


#===================================================================================================


if __name__ == '__main__':

	if len(sys.argv) > 1:

		# use last argument as file name and open it
		fname = sys.argv[ len(sys.argv)-1 ]

		try:
			f = open( fname, 'r+b')
		except:
			print( "ERROR: file not found (%s)" % fname )
			sys.exit()

		try:
			PartList = pickle.load(f)
		except:
			print( "ERROR loading data (%s)" % fname )
			f.close()
			sys.exit()

		if f:
			f.close()


	app = wx.App(False)
	main_win = MainWin(None)
	app.MainLoop()

