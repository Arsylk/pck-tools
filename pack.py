from tkinter import Tk
from tkinter.filedialog import *
import sys
import pck_tools


# path = "E:/Android/AndroidProjects/RIP Banana/files/locale.pck"
# sys.argv.append(path)

path = None
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    Tk().withdraw()
    path = askopenfilename(title="Open _header file...")
if path:
    pck = pck_tools.from_header(path)
    pck_path = pck_tools.save_file(pck_tools.pack_pck(pck), pck.path, pck.path[pck.path.rfind("/")+1:]+".pck")
    input()
