import serial
import time

class ModbusRTU(object):

    def __init__(self, port, speed):
        self.serialModbusRTU = None
        self.serialModbusRTU = serial.Serial(port, speed, timeout=1)

        if(self.serialModbusRTU is not None):
            if(self.serialModbusRTU.isOpen() is False):
                self.serialModbusRTU.open()

        time.sleep(5)

    def readCoils(self, ID, registerNumber, registerQuantity):
        dataWrite = bytearray([ID, 0x01, 0x00, registerNumber, 0x00, registerQuantity, 0, 0])
        dataRead = bytearray()
        lenDataRead = 0

        if(registerQuantity % 8 != 0):
            lenDataRead = 6 + int(registerQuantity / 8)
        else:
            lenDataRead = 5 + int(registerQuantity / 8)

        CRCWrite = self.calculateCRC(dataWrite, len(dataWrite) - 2)
        crcLSBWrite = CRCWrite & 0xFF
        crcMSBWrite = (CRCWrite & 0xFF00) >> 8
        dataWrite[6] = crcLSBWrite
        dataWrite[7] = crcMSBWrite

        self.serialModbusRTU.write(dataWrite)
        dataRead = self.serialModbusRTU.read(lenDataRead)

        CRCRead = self.calculateCRC(dataRead[:(len(dataRead) - 2)], len(dataRead) - 2)
        crcLSBRead = CRCRead & 0xFF
        crcMSBRead = (CRCRead & 0xFF00) >> 8

        if((0x01 == dataRead[1]) & (crcLSBRead == dataRead[(len(dataRead) - 2)]) & (crcMSBRead == dataRead[(len(dataRead) - 1)])):
            coilsList = list()

            for i in range(0, registerQuantity):
                coilsList.append(bool((dataRead[int(i/8)+3] >> int(i%8)) & 0x1))

            return coilsList

    def readInputs(self, ID, registerNumber, registerQuantity):
        dataWrite = bytearray([ID, 0x02, 0x00, registerNumber, 0x00, registerQuantity, 0, 0])
        dataRead = bytearray()
        lenDataRead = 0

        if(registerQuantity % 8 != 0):
            lenDataRead = 6 + int(registerQuantity / 8)
        else:
            lenDataRead = 5 + int(registerQuantity / 8)

        CRCWrite = self.calculateCRC(dataWrite, len(dataWrite) - 2)
        crcLSBWrite = CRCWrite & 0xFF
        crcMSBWrite = (CRCWrite & 0xFF00) >> 8
        dataWrite[6] = crcLSBWrite
        dataWrite[7] = crcMSBWrite

        self.serialModbusRTU.write(dataWrite)
        dataRead = self.serialModbusRTU.read(lenDataRead)

        CRCRead = self.calculateCRC(dataRead[:(len(dataRead) - 2)], len(dataRead) - 2)
        crcLSBRead = CRCRead & 0xFF
        crcMSBRead = (CRCRead & 0xFF00) >> 8

        if((0x02 == dataRead[1]) & (crcLSBRead == dataRead[(len(dataRead) - 2)]) & (crcMSBRead == dataRead[(len(dataRead) - 1)])):
            inputsList = list()

            for i in range(0, registerQuantity):
                inputsList.append(bool((dataRead[int(i / 8) + 3] >> int(i % 8)) & 0x1))

            return inputsList

    def readHoldingRegisters(self, ID, registerNumber, registerQuantity):
        dataWrite = bytearray([ID, 0x03, 0x00, registerNumber, 0x00, registerQuantity, 0, 0])
        dataRead = bytearray()
        lenDataRead = 5 + (registerQuantity * 2)

        CRCWrite = self.calculateCRC(dataWrite, len(dataWrite) - 2)
        crcLSBWrite = CRCWrite & 0xFF
        crcMSBWrite = (CRCWrite & 0xFF00) >> 8
        dataWrite[6] = crcLSBWrite
        dataWrite[7] = crcMSBWrite

        self.serialModbusRTU.write(dataWrite)
        dataRead = self.serialModbusRTU.read(lenDataRead)

        CRCRead = self.calculateCRC(dataRead[:(len(dataRead) - 2)], len(dataRead) - 2)
        crcLSBRead = CRCRead & 0xFF
        crcMSBRead = (CRCRead & 0xFF00) >> 8

        if((0x03 == dataRead[1]) & (crcLSBRead == dataRead[(len(dataRead) - 2)]) & (crcMSBRead == dataRead[(len(dataRead) - 1)])):
            HoldingRegistersList = list()

            for i in range(0, registerQuantity):
                HoldingRegistersList.append((dataRead[i*2+3] << 8) + dataRead[i*2+4])

            return HoldingRegistersList

    def readInputRegisters(self, ID, registerNumber, registerQuantity):
        dataWrite = bytearray([ID, 0x04, 0x00, registerNumber, 0x00, registerQuantity, 0, 0])
        dataRead = bytearray()
        lenDataRead = 5 + (registerQuantity * 2)

        CRCWrite = self.calculateCRC(dataWrite, len(dataWrite) - 2)
        crcLSBWrite = CRCWrite & 0xFF
        crcMSBWrite = (CRCWrite & 0xFF00) >> 8
        dataWrite[6] = crcLSBWrite
        dataWrite[7] = crcMSBWrite

        self.serialModbusRTU.write(dataWrite)
        dataRead = self.serialModbusRTU.read(lenDataRead)

        CRCRead = self.calculateCRC(dataRead[:(len(dataRead) - 2)], len(dataRead) - 2)
        crcLSBRead = CRCRead & 0xFF
        crcMSBRead = (CRCRead & 0xFF00) >> 8

        if((0x04 == dataRead[1]) & (crcLSBRead == dataRead[(len(dataRead) - 2)]) & (crcMSBRead == dataRead[(len(dataRead) - 1)])):
            InputRegistersList = list()

            for i in range(0, registerQuantity):
                InputRegistersList.append((dataRead[i*2+3] << 8) + dataRead[i*2+4])

            return InputRegistersList

    def writeSingleCoil(self, ID, registerNumber, registerStatus):
        dataWrite = bytearray([ID, 0x05, 0x00, registerNumber, registerStatus, 0x00, 0, 0])
        dataRead = bytearray()

        CRCWrite = self.calculateCRC(dataWrite, len(dataWrite) - 2)
        crcLSBWrite = CRCWrite & 0xFF
        crcMSBWrite = (CRCWrite & 0xFF00) >> 8
        dataWrite[6] = crcLSBWrite
        dataWrite[7] = crcMSBWrite

        self.serialModbusRTU.write(dataWrite)
        dataRead = self.serialModbusRTU.read(8)

        CRCRead = self.calculateCRC(dataRead[:(len(dataRead) - 2)], len(dataRead) - 2)
        crcLSBRead = CRCRead & 0xFF
        crcMSBRead = (CRCRead & 0xFF00) >> 8

        if((0x05 == dataRead[1]) & (crcLSBRead == dataRead[(len(dataRead) - 2)]) & (crcMSBRead == dataRead[(len(dataRead) - 1)])):
            return True
        else:
            return False

    def writeSingleRegister(self, ID, registerNumber, registerValue):
        dataWrite = bytearray([ID, 0x06, 0x00, registerNumber, 0x00, registerValue, 0, 0])
        dataRead = bytearray()

        CRCWrite = self.calculateCRC(dataWrite, len(dataWrite) - 2)
        crcLSBWrite = CRCWrite & 0xFF
        crcMSBWrite = (CRCWrite & 0xFF00) >> 8
        dataWrite[6] = crcLSBWrite
        dataWrite[7] = crcMSBWrite

        self.serialModbusRTU.write(dataWrite)
        dataRead = self.serialModbusRTU.read(8)

        CRCRead = self.calculateCRC(dataRead[:(len(dataRead) - 2)], len(dataRead) - 2)
        crcLSBRead = CRCRead & 0xFF
        crcMSBRead = (CRCRead & 0xFF00) >> 8

        if((0x06 == dataRead[1]) & (crcLSBRead == dataRead[(len(dataRead) - 2)]) & (crcMSBRead == dataRead[(len(dataRead) - 1)])):
            return True
        else:
            return False

    def calculateCRC(self, dataToCheck, numberOfBytesDataToCheck):
        crc = 0xFFFF
        for x in range(0, numberOfBytesDataToCheck):
            crc = crc ^ dataToCheck[x]
            for i in range(0, 8):
                if((crc & 0x0001) != 0):
                    crc = crc >> 1
                    crc = crc ^ 0xA001
                else:
                    crc = crc >> 1
        return crc

