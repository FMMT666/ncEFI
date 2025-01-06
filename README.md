ncEFI
=====
>"I did even forget what the name stood for..." -- Me in 2016.

---

A Python programmable G-Code generator for milling machines,  
including a minimalistic OpenGL preview.  
Well, er... The remains of that :)

![Circular Pocket Toolpath](/images/ncEFI_circularPockets.png)  

This is not meant to be a CAM software or for milling parts, but
for preparing the stock or quickly doing other things "live".

I restored these Python fragments from an old CPIOed backup tape.  
The only thing I remember is, that I implemented a quite cool, round
pocket milling algorithm (and much more later on).

As far as I can remember, that was my first contact with Python at all,  
sometime around 1995, lol.  
That's also what the code looks like (o_O)

But I want some quick action buttons in ~~EMC~~ ~~EMC2~~ LinuxCNC.


---
## What Dis?

Fun.

---
## Requirements

- Python 3.x

Only for 'ncEFIDisp2', the viewer:
 - wxPython
 - PyOpenGL
 - PyOpenGL_accelerate

> As of 11/2024 it is recommended to install everything via your system's package manager if available.  
> Especially under macOS on ARM machines.

Installing wxPython will install Numpy and Pillow if not already present.  
The PyOpenGL installation does not have any additional dependencies.

The main app 'ncEFI' does not need any additional libraries, it even comes with its own
vector math lib (yes, another big lol, I know :)

All of the above are available via pip.


### Windows
Installing PyOpenGL via pip will not work. Use the [binaries from here][1] instead
and make sure they match your Python version AND your system. Either 32 or 64 bits.

Install them with (Python 3.7 64-bit example here):

    pip install PyOpenGL‑3.1.5‑cp37‑cp37m‑win_amd64.whl
    pip install PyOpenGL_accelerate‑3.1.5‑cp37‑cp37m‑win_amd64.whl


### macOS

#### Intel

Even though Big Sur brought a lot of OpenGL problems, everything can be easily
installed via pip. That will even work with the (introduced in Catalina (?))
"Apple Python 3.8.x" version ("/usr/bin/python3").  
Will work with X from either MacPorts ("ports") or Homebrew ("brew"), as well as
XQuartz.

The visualiser 'ncEFIDisp2' also works with the macOS-touchpads.  
Three fingers will rotate, two fingers sliding will zoom and two fingers
with pad-press will pan.

The OpenGL library has a bug and requires that the windows is resized once.  
Might add a workaround for this in future versions.

#### ARM

For Apple Silicon, M1..M4 the complete installation needs to be done via MacPorts or Homebrew.
This also requires a Python version from there.

Example packages for Ports with Python 3.12, as of 11/2024:

    py312-opengl                   @3.1.7_0 (active)
    py312-opengl-accelerate        @3.1.7_0 (active)

    py312-wxpython-4.0             @4.2.1_0 (active)

Notice that this might install an insane amount of other dependencies,
e.g. GCC et.al., in case they are missing.

### Linux
That always worked.

As of 11/2024 it's also recommended to install everything via your package manager if available.

#### DevTerm (or possibly other embedded devices)
Just for the fun of it, I tested this on a [clockwerk DevTerm][2].  

> Do not install wxPython via pip on this device.

This thing does not have enough resources to compile it and wheels do
not exist (yet). Install this via ```apt-get``` and lookout for something
that is named
> ```libwxgtk3.x...```  
> ```libwxgtk4.x...``` (unlikely)


---
## News

### CHANGES 2025/01/XX
    - added minimum brightness for random colors
    - added list/check boxes for testing; lol no
    - added some helper functions for parts
    - added filling the CheckList box with parts
    - added a class for the part list
    - began modifying false instance copies, with "no copy" as default
    - began modifying false instance copies for some geoms too


### CHANGES 2024/12/XX
    - started poly offset functionality & tools
    - added some 3D-space distance functions
    - added tColor in element's extras (for viewer)
    - added tSize  in element's extras (for viewer)
    - added split lines function
    - added color cycling in the viewer
    - added some parts count debug prints in the viewer
    - needs changes to highlighting/colorcycling before more offset work


### CHANGES 2024/11/XX
    - added notes for Apple Silicon


### CHANGES 2022/01/XX
    - changes for macOS display


### CHANGES 2021/11/XX
    - now finally with "feed rate vertices", allowing important adjustment or infos
    - added comments for vertices that can appear in the G-code
    - new global base feed rate
    - WARNING: toolFullAuto()'s 1st parameter was changed to be a feed rate; safe Z now 2nd
    - header now parsed to contain GCODE_OP_BFEED; will be replaced by a code set value


### CHANGES 2021/10/XX
    - continuing to add stuff


### CHANGES 2021/09/XX
    - now finally with correct OpenGL view navigation
    - added even more more functions


### CHANGES 2021/09/XX
    - added even more functions


### CHANGES 2021/08/XX
    - I have a stupid idea.
    - ported ncEFI.py to Python 3.x (origins were Python 1.5, lmao)
    - added a lot of new functions


### CHANGES 2016/01/14
    - initial upload of this "whatever"


### CHANGES 2007/11/XX
    - last available code before the computer was destroyed by a fire


---
Have fun (with whatever)  
FMMT666(ASkr)



[1]: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl
[2]: https://www.clockworkpi.com/devterm

