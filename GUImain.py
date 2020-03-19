from tkinter import *
from subprocess import call

win = Tk()

win.overrideredirect(1)
win.geometry("480x320")
win.configure(bg="#FFFFFF")

title = Entry(win, width=10)
title.configure(bd=0, highlightbackground="white", highlightcolor="white")
title.place(bordermode=OUTSIDE, height=20, width=440, x=50, y=10)
title.insert(0, "{}".format("STRONA GLOWNA"))

def shutDownFunction():
    call("sudo poweroff", shell=True)

shutDownButton = Button(win, command=shutDownFunction)
shutDownImage = PhotoImage(file="/home/pi/Program/img/shutdown.png")
shutDownButton.config(image=shutDownImage)
shutDownButton.configure(highlightbackground="white", highlightcolor="white")
shutDownButton.place(bordermode=OUTSIDE, height=40, width=40, x=0, y=0)

def closeFunction():
    win.destroy()

closeButton = Button(win, command=closeFunction)
closeImage = PhotoImage(file="/home/pi/Program/img/close.png")
closeButton.config(image=closeImage)
closeButton.configure(highlightbackground="white", highlightcolor="white")
closeButton.place(bordermode=OUTSIDE, height=40, width=40, x=440, y=0)

def openGUImodbusRTU():
    call("python3 /home/pi/Program/GUImodbusRTU.py", shell=True)

openGUImodbusRTUButton = Button(win, text="URUCHOM MODBUS", command=openGUImodbusRTU)
openGUImodbusRTUButton.configure(highlightbackground="white", highlightcolor="white")
openGUImodbusRTUButton.place(bordermode=OUTSIDE, height=40, width=140, x=0, y=50)

if __name__ == "__main__":
    win.mainloop()
