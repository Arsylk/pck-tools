from tkinter import *
from tkinter.ttk import *
import pck_tools


def make_entry(key, value):
    entry_frame = Frame(bot_frame)
    entry_frame.pack(side=TOP, fill="x")
    entry_key = Label(entry_frame, text=key, style="Dict.TLabel")
    entry_key.pack(side=TOP, fill="x")
    entry_value = Entry(entry_frame)
    entry_value.delete(0, END)
    entry_value.insert(0, value)
    entry_value.pack(side=TOP, fill="x")


fp = "E:/Android/AndroidProjects/RIP Banana/files/locale_kr.pck"
pck = pck_tools.unpack_pck(fp)

window = Tk()
window.title("Locale.pck translate tool!")
window.geometry("350x200")


style = Style()
style.configure("Dict.TLabel", background="red")

frame = Frame(window)
frame.pack(fill="both", expand=True)

top_frame = Frame(frame)
top_frame.pack(side=TOP, fill="x")

bot_frame = Frame(frame)
bot_frame.pack(side=BOTTOM, fill="both", expand=True)

scroll = Scrollbar(bot_frame)
scroll.pack(side=RIGHT, fill="y", expand=False)

button = Button(top_frame, text="Save")
button.pack(side=RIGHT)

combo = Combobox(top_frame, state="readonly", values=[x.hash.upper() for x in pck.get_files()])
combo.pack(side=LEFT, fill="x", expand=True)
def switch_file(event):
    hash = combo.get()
    file = pck.get_file(hash=hash)
    for key in file.to_dict():
        print(key, file.dict[key])
        make_entry(key, file.dict[key])
    scroll.update()


combo.bind("<<ComboboxSelected>>", switch_file)

window.mainloop()