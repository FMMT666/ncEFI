#!/usr/bin/python

from Tkinter import *
import Image
import ImageTk
import Pmw

from ncEFI import *




class PyMillWin:

  ############################################################################
  ### __init__
  ###
  ### The mother of all (secondary) processes...
  ############################################################################
  def __init__ (self):
    self.initCreateWidgets()



  ############################################################################
  ### initCreateWidgets
  ###
  ### Some stinky menus, buttons, etc...
  ############################################################################
  def initCreateWidgets(self):
  
    self.PMtkRoot=Tk()
    Pmw.initialise(self.PMtkRoot)

    # MENUs
    self.PMmenu=Menu(self.PMtkRoot)
    self.PMtkRoot.config(menu=self.PMmenu)

    # menu "FILE"
    self.PMmenuFile=Menu(self.PMmenu)
    self.PMmenu.add_cascade(label="File", menu=self.PMmenuFile)
    self.PMmenuFile.add_command(label="New", command=self.PMcallback)
    self.PMmenuFile.add_command(label="Open", command=self.PMcallback)
    self.PMmenuFile.add_command(label="Save", command=self.PMcallback)
    self.PMmenuFile.add_command(label="Save As...", command=self.PMcallback)
    self.PMmenuFile.add_separator()
    self.PMmenuFile.add_command(label="Import", command=self.PMcallback)
    self.PMmenuFile.add_command(label="Export", command=self.PMcallback)
    self.PMmenuFile.add_separator()
    self.PMmenuFile.add_command(label="Exit", command=self.PMcallback)

    # menu "TOOLS"
    self.PMmenuTools=Menu(self.PMmenu)
    self.PMmenu.add_cascade(label="Tools", menu=self.PMmenuTools)
    self.PMmenuTools.add_command(label="Edit", command=self.PMcallback)
    self.PMmenuFile.add_separator()
    self.PMmenuTools.add_command(label="Load", command=self.PMcallback)
    self.PMmenuTools.add_command(label="Save", command=self.PMcallback)


    # frame for buttons (tools)
    self.PMframe=Frame(self.PMtkRoot,width=100)
    self.balloon = Pmw.Balloon(self.PMframe)

    self.PMbutNames=['butSelect','butCreatePart','butEmpty1',
    'butDrill','butMillHole', 'butMillRing',
    'butMillPocket','butMillPocketAround','butEngrave',
    'butOutline','butEmpty2','butEmpty3',
    'but3D','butEmpty4','butEmpty5']
    x=y=i=0
    self.PMbutPics={}
    self.PMbutButts={}
    for nam in self.PMbutNames:
      self.PMbutPics[nam]=ImageTk.PhotoImage(file='pix/'+nam+'.gif',master=self.PMframe)
      self.PMbutButts[nam]=Button(self.PMframe,image=self.PMbutPics[nam],command=lambda nnam=nam:self.PMcallback(nnam))
      self.PMbutButts[nam].grid(row=y,column=x)
      if nam=='butSelect':
        tooltip='select'
      if nam=='butCreatePart':
        tooltip='create part from elements'
      if nam=='but3D':
        tooltip='show OpenGL 3D preview'
      self.balloon.bind(self.PMbutButts[nam], tooltip)
      x+=1
      if x > 2:
        x=0
        y+=1

    self.PMframe.pack(expand=0,side='left',fill='none',anchor='n',pady=1)

    # CANVAS
    self.PMcanvas=Canvas(self.PMtkRoot)
    self.PMcanvas.pack(expand=1,fill='both')
    self.PMcanvas.config(relief=SUNKEN,background="#333333")

    self.PMcanvas.create_line(10,10,100,10)  
    self.PMcanvas.create_line(10,10,100,20)  
    self.PMcanvas.create_line(10,10,100,30)  
    self.PMcanvas.create_line(10,10,100,40)  

    self.PMcanvas.bind("<Configure>",self.PMredraw)
    self.PMcanvas.bind("<Button-1>",self.PMcallbackMouse)
    self.PMcanvas.bind("<Button-3>", self.PMcallbackMouse)
    self.PMcanvas.bind("<Shift-Button-1>", self.PMcallbackMouse)
    self.PMcanvas.bind("<Shift-Button-3>", self.PMcallbackMouse)

    self.MB=Pmw.MessageBar()
    self.MB.pack(side='bottom',fill='x')


  ############################################################################
  ### PMcallback
  ###
  ###
  ############################################################################
  def PMcallback(self,nam=''):
    print "CALLBACK:"
    print nam


  ############################################################################
  ### PMredraw
  ###
  ###
  ############################################################################
  def PMredraw(self,event):
    print "REDRAW"



  ############################################################################
  ### PMcallbackMouse
  ###
  ###
  ############################################################################
  def PMcallbackMouse(self,event):
#    print self.PMcanvas.find_closest(event.x,event.y)
    print event.type
    
    




if __name__== '__main__':
  MillWin=PyMillWin()
  MillWin.PMtkRoot.mainloop()

