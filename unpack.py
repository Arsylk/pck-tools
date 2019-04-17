from tkinter import Tk
from tkinter.filedialog import *
import sys
import pck_tools


# path = "E:/Android/AndroidProjects/RIP Banana/files/locale.pck"
# sys.argv.append(path)

ppp = None
if len(sys.argv) > 1:
    ppp = pck_tools.unpack_pck(sys.argv[1])
else:
    Tk().withdraw()
    ppp = pck_tools.unpack_pck(askopenfilename(title="Open file..."))
input()
