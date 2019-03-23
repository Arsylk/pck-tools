from tkinter import Tk
from tkinter.filedialog import *
import sys
import pck_tools
import json


#path = "E:/Android/AndroidProjects/RIP Banana/files/c401_02.pck"
#sys.argv.append(path)

ppp = None
if len(sys.argv) > 1:
    ppp = pck_tools.unpack_pck(sys.argv[1])
else:
    Tk().withdraw()
    ppp = pck_tools.unpack_pck(askopenfilename(title="Open file..."))
	
file = ppp.path
content = json.dumps(ppp.get_file(hash="F80A001A49CFDA65").to_json(), sort_keys=False, indent=4).encode("utf-8")
print(pck_tools.save_file(content, file[:file.rfind("/")], file[file.rfind("/") + 1:file.rfind(".")]+".json"))
input()