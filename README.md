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
pocket milling algorithm.

As far as I can remember, that was my first contact with Python at all,  
sometime around 1995, lol.  
That's also what the code looks like (o_O)

But I want that in ~~EMC~~ ~~EMC2~~ LinuxCNC.


---
## Wtf?

Move on, there is nothing to see here, yet...

---
## Requirements

t.b.d...

...

Only for the viewer:
 - PyOpenGL
 - PyOpenGL_accelerate

### Windows specific issues
Installing PyOpenGL via pip will not work. Use the [binaries from here][1] instead
and make sure they match your Python version AND your system. Either 32 or 64 bits.

Install them with (Python 3.7 64-bit example here):

    pip install PyOpenGL‑3.1.5‑cp37‑cp37m‑win_amd64.whl
    pip install PyOpenGL_accelerate‑3.1.5‑cp37‑cp37m‑win_amd64.whl

---
## News

### CHANGES 2021/08/XX
    - I have a stupid idea.
    - ported ncEFI.py to Python 3.x (origins were Python 1.5, lmao)
    - added some new functions

### CHANGES 2016/01/14
    - initial upload of this "whatever"

### CHANGES 2007/11/XX
    - last available code before the computer was destroyed by a fire

---

Have fun (with whatever)  
FMMT666(ASkr)



[1]: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl

