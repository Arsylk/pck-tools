from tkinter import Tk
from tkinter.filedialog import *
import pck_tools


def header_gui():
    print()
    print("MergePCK  -  a tool for combining locale.pck files from Destiny Child")
    print("v0.0.1")
    print("by Arsylk")
    print("discord: Arsylk#8993")
    print()
    print("     This tool will merge korean file with older english patch!")
    print("     Translate values will be changed, while keeping new values untouched.")
    print()
    print()

Tk().withdraw()
header_gui()

print("-Select korean locale.pck")
kr_file = askopenfilename(title="Open korean locale...")
if not kr_file:
    exit(-1)
print(kr_file)
print()
print("-Select english locale.pck")
en_file = askopenfilename(title="Open english locale...")
if not en_file:
    exit(-1)
print(en_file)
print()
print("-Save merged file as")
fl_file = asksaveasfilename(title="Save file as...", initialfile="locale.pck")
if not fl_file:
    exit(-1)
print(fl_file)
print()
print()

if os.path.isfile(kr_file) and os.path.isfile(en_file):
    fl_pck = pck_tools.merge_pck(kr_file, en_file, fl_file)
    pck_tools.save_file(pck_tools.pack_pck(fl_pck), fl_file[:fl_file.rfind("/")], fl_file[fl_file.rfind("/")+1:])
    print()
    print("Finished!")