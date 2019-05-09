from tkinter import Tk
from tkinter.filedialog import *
import sys
import pck_tools


# path = "C:/Users/Arsylk/Nox_share/Other/c401_01.pck"
# sys.argv.append(path)

ppp = None
if len(sys.argv) > 1:
    ppp = pck_tools.unpack_pck(sys.argv[1])
else:
    Tk().withdraw()
    path = askopenfilename(title="Open file...")
    pck_tools.clean_up(path)
    ppp = pck_tools.unpack_pck(path)
    pck_tools.pck_to_model(ppp)
input()
