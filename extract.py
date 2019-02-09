from tkinter import Tk
from tkinter.filedialog import *
import sys
import pck_tools






#path = "E:/Android/AndroidProjects/RIP Banana/files/c401_02.pck"
#sys.argv.append(path)

if len(sys.argv) > 1:
    pck_tools.unpack_pck(sys.argv[1])
else:
    Tk().withdraw()
    pck_tools.unpack_pck(askopenfilename(title="Open file..."))
input();