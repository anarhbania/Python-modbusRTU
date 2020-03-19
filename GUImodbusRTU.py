
from tkinter import *
from threading import Thread
from subprocess import call
from lib.modbusRTU import *

win = Tk()

quantityCoilsRead = 10
quantityInputsRead = 10
quantityHoldingRegistersRead = 10
quantityInputsRegistersRead = 10

win.overrideredirect(1)
win.geometry("480x320")
win.configure(bg="#FFFFFF")

title = Entry(win, width=10)
title.configure(bd=0, highlightbackground="white", highlightcolor="white")
title.place(bordermode=OUTSIDE, height=20, width=440, x=50, y=10)
title.insert(0, "{}".format("WCZYTUJE: MODBUS RTU"))

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

titleCoils = Entry(win, width=10)
titleCoils.configure(bd=0, highlightbackground="white", highlightcolor="white")
titleCoils.place(bordermode=OUTSIDE, height=20, width=50, x=0, y=40)
titleCoils.insert(0, "COILS:")

titleInputs = Entry(win, width=10)
titleInputs.configure(bd=0, highlightbackground="white", highlightcolor="white")
titleInputs.place(bordermode=OUTSIDE, height=20, width=60, x=70, y=40)
titleInputs.insert(0, "INPUTS:")

titleHoldingRegisters = Entry(win, width=10)
titleHoldingRegisters.configure(bd=0, highlightbackground="white", highlightcolor="white")
titleHoldingRegisters.place(bordermode=OUTSIDE, height=20, width=140, x=140, y=40)
titleHoldingRegisters.insert(0, "HOLDING REGISTERS:")

titleInputsRegisters = Entry(win, width=10)
titleInputsRegisters.configure(bd=0, highlightbackground="white", highlightcolor="white")
titleInputsRegisters.place(bordermode=OUTSIDE, height=20, width=140, x=300, y=40)
titleInputsRegisters.insert(0, "INPUTS REGISTERS:")

quantityCoils = bytearray(quantityCoilsRead)
quantityInputs = bytearray(quantityInputsRead)
quantityHoldingRegisters = bytearray(quantityHoldingRegistersRead)
quantityInputsRegisters = bytearray(quantityInputsRegistersRead)

dataCoils = {}
dataInputs = {}
dataHoldingRegisters = {}
dataInputsRegisters = {}

dataQuantityCoils = 0
for coilsCreateEntry in quantityCoils:
    dataCoils[dataQuantityCoils] = Entry(win, width=10)
    dataCoils[dataQuantityCoils].configure(bd=0, highlightbackground="white", highlightcolor="white")
    dataCoils[dataQuantityCoils].place(bordermode=OUTSIDE, height=20, width=50, x=0, y=60+(dataQuantityCoils*20))
    dataQuantityCoils += 1

dataQuantityInputs = 0
for inputsCreateEntry in quantityInputs:
    dataInputs[dataQuantityInputs] = Entry(win, width=10)
    dataInputs[dataQuantityInputs].configure(bd=0, highlightbackground="white", highlightcolor="white")
    dataInputs[dataQuantityInputs].place(bordermode=OUTSIDE, height=20, width=50, x=70, y=60+(dataQuantityInputs*20))
    dataQuantityInputs += 1

dataQuantityHoldingRegisters = 0
for holdingRegistersCreateEntry in quantityHoldingRegisters:
    dataHoldingRegisters[dataQuantityHoldingRegisters] = Entry(win, width=10)
    dataHoldingRegisters[dataQuantityHoldingRegisters].configure(bd=0, highlightbackground="white", highlightcolor="white")
    dataHoldingRegisters[dataQuantityHoldingRegisters].place(bordermode=OUTSIDE, height=20, width=50, x=140, y=60+(dataQuantityHoldingRegisters*20))
    dataQuantityHoldingRegisters += 1

dataQuantityInputsRegisters = 0
for inputsRegistersCreateEntry in quantityInputsRegisters:
    dataInputsRegisters[dataQuantityInputsRegisters] = Entry(win, width=10)
    dataInputsRegisters[dataQuantityInputsRegisters].configure(bd=0, highlightbackground="white", highlightcolor="white")
    dataInputsRegisters[dataQuantityInputsRegisters].place(bordermode=OUTSIDE, height=20, width=50, x=300, y=60+(dataQuantityInputsRegisters*20))
    dataQuantityInputsRegisters += 1

def readModbusRTU():
    RS485 = ModbusRTU("/dev/ttyACM0", 9600)

    title.delete(0, "end")
    title.insert(0, "{}".format("URUCHOMIONA APLIKACJA: MODBUS RTU"))

    while True:
        try:
            Coils = RS485.readCoils(10, 1, quantityCoilsRead)
            Inputs = RS485.readInputs(10, 1, quantityInputsRead)
            HoldingRegisters = RS485.readHoldingRegisters(10, 1, quantityHoldingRegistersRead)
            InputsRegisters = RS485.readInputRegisters(10, 1, quantityInputsRegistersRead)

            dataQuantityCoils = 0
            dataQuantityInputs = 0
            dataQuantityHoldingRegisters = 0
            dataQuantityInputsRegisters = 0

            for coilsCreateEntry in quantityCoils:
                dataCoils[dataQuantityCoils].delete(0, END)
                dataCoils[dataQuantityCoils].insert(0, "{}".format(Coils[dataQuantityCoils]))
                dataQuantityCoils += 1

            for inputsCreateEntry in quantityInputs:
                dataInputs[dataQuantityInputs].delete(0, END)
                dataInputs[dataQuantityInputs].insert(0, "{}".format(Inputs[dataQuantityInputs]))
                dataQuantityInputs += 1

            for holdingRegistersCreateEntry in quantityHoldingRegisters:
                dataHoldingRegisters[dataQuantityHoldingRegisters].delete(0, END)
                dataHoldingRegisters[dataQuantityHoldingRegisters].insert(0, "{}".format(HoldingRegisters[dataQuantityHoldingRegisters]))
                dataQuantityHoldingRegisters += 1

            for inputsRegistersCreateEntry in quantityInputsRegisters:
                dataInputsRegisters[dataQuantityInputsRegisters].delete(0, END)
                dataInputsRegisters[dataQuantityInputsRegisters].insert(0, "{}".format(InputsRegisters[dataQuantityInputsRegisters]))
                dataQuantityInputsRegisters += 1

        except:
            break

def runThreadModbusRTU():
    enableThreadModbusRTU = Thread(target=readModbusRTU)
    enableThreadModbusRTU.start()

if __name__ == "__main__":
    runThreadModbusRTU()
    win.mainloop()
