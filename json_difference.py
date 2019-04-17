import json
from tkinter.filedialog import *


def readfile(path):
    with open(path, "r", encoding="utf-8", errors="replace") as file:
        return json.load(file)


def savefile(content):
    file = asksaveasfile(mode="wb", initialfile="differences", defaultextension=".json")
    if file:
        file.write(content)
        file.close()


Tk().withdraw()
base_path = askopenfilename(title="Open base file...")
new_path = askopenfilename(title="Open new file...")

base_json = readfile(base_path)
new_json = readfile(new_path)

found = 0
for hash in base_json["files"]:
    for key in base_json["files"][hash]["dict"]:
        try:
            if base_json["files"][hash]["dict"][key] == new_json["files"][hash]["dict"][key]:
                del new_json["files"][hash]["dict"][key]
            else:
                found += 1
        except:
            pass
    try:
        if len(new_json["files"][hash]["dict"]) == 0:
            del new_json["files"][hash]
    except:
        pass
        
print("Found {:d} differnet keys".format(found))
savefile(json.dumps(new_json, sort_keys=False, indent=4, ensure_ascii=False).encode("utf-8"))
