import random
from cmu_graphics import *


class CPU:
    def __init__(self, input):
        f = open(input, 'rb')
        self.v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.vF = 0
        self.I = 0
        self.i = 0

        self.b = (f.read())
        self.opcode = []

    def getLength(self):
        return len(self.b)

    def oneTwoInfo(n):
        info1 = n >> 8
        info2 = n & 255
        return info1, info2
    def twoOneInfo(n):
        info1 = n >> 4
        info2 = n & 15
        return info1, info2
    def one3Info(n):
        info1 = n >> 8
        info2 = n >> 4 & 15
        info3 = n & 15
        return info1, info2, info3

    def code(iterations, run, self):
        for i in range(0 + (run * iterations), iterations * run, 2):
            instruction = self.b[i] >> 4
            information1 = self.b[i] & 15
            information1Shifted = information1 << 8
            information2 = self.b[i+1]
            information = information1Shifted | information2
            match instruction:
                case 0:
                    self.opcode.append([instruction, CPU.one3Info(information)])
                    match CPU.one3Info(information)[2]:
                        case 0:
                            #Clear the display.
                            pass
                        case 14:
                            #The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
                            pass
                case 1:
                    self.opcode.append([instruction, information])
                    #The interpreter sets the program counter to nnn. WHAT DOES THIS MEAN?
                case 2:
                    #The interpreter increments the stack pointer, then puts the current PC on the top of the stack. The PC is then set to nnn.
                    self.pcode.append([instruction, information])
                case 3:
                    self.opcode.append([instruction, CPU.oneTwoInfo(information)])
                    x, k = CPU.oneTwoInfo(information)
                    if self.v[x] == k:
                        print("skip")
                        i += 2
                case 4:
                    self.opcode.append([instruction, CPU.oneTwoInfo(information)])
                    x, k = CPU.oneTwoInfo(information)
                    if self.v[x] != k:
                        print("skip")
                        i += 2
                case 5:
                    self.opcode.append([instruction, CPU.one3Info(information)])
                    x, y, k = CPU.one3Info(information)
                    if self.v[x] == self.v[y]:
                        print("skip")
                        i += 2
                case 6:
                    self.opcode.append([instruction, CPU.oneTwoInfo(information)])
                    x, k = CPU.oneTwoInfo(information)
                    self.v[x] = k
                case 7:
                    self.opcode.append([instruction, CPU.oneTwoInfo(information)])
                    x, k = CPU.oneTwoInfo(information)
                    self.v[x] += k
                case 8:
                    self.opcode.append([instruction, CPU.twoOneInfo(information)])
                    x, y, k = CPU.one3Info(information)
                    match k:
                        case 0:
                            self.v[x] = self.v[y]
                        case 1:
                            self.v[x] = self.v[x] & self.v[y]
                        case 2:
                            self.v[x] = self.v[x] | self.v[y]
                        case 3:
                            self.v[x] = self.v[x] ^ self.v[y]
                        case 4:
                            set = self.v[x] + self.v[y]
                            if set > 255:
                                set | 255
                                self.vF = 1
                            else:
                                self.vF = 0
                            self.v[x] = set
                        case 5:
                            set = self.v[x] - self.v[y]
                            if set > 0:
                                self.vF = 1
                            else:
                                self.vF = 0
                            self.v[x] = set #THIS SEEMS WRONG. WHAT IF SET < 0
                        case 6:
                            if self.v[x] | 1 == 1:
                                vF = 1
                            else:
                                vF = 0
                            self.v[x] /= 2
                            pass
                        case 7:
                            set = self.v[y] - self.v[x]
                            if set > 0:
                                self.vF = 1
                            else:
                                self.vF = 0
                            self.v[x] = set #THIS SEEMS WRONG. WHAT IF SET < 0
                        case 14:
                            #If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
                            pass
                case 9:
                    self.opcode.append([instruction, CPU.one3Info(information)])
                    x, y, k = CPU.one3Info(information)
                    if self.v[x] != self.v[y]:
                        print("skip")
                        i += 2
                case 10:
                    self.opcode.append([instruction, information])
                    I = information
                case 11:
                    self.opcode.append([instruction, information])
                    I = information + self.v[0]
                case 12:
                    self.opcode.append([instruction, CPU.oneTwoInfo(information)])
                    x, k = CPU.oneTwoInfo(information)
                    r = random.randint(0, 255)
                    self.v[x] = r & k
                case 13:
                    self.opcode.append([instruction, CPU.one3Info(information)])
                case 14:
                    self.opcode.append([instruction, CPU.oneTwoInfo(information)])
                    match CPU.oneTwoInfo(information)[1]:
                        case 158:
                            pass
                        case 161:
                            pass
                case 15:
                    self.opcode.append([instruction, CPU.oneTwoInfo(information)])
                    match CPU.oneTwoInfo(information)[1]:
                        case 1:
                            pass
                        case 2:
                            pass
                        case 3:
                            pass
                        case 4:
                            pass
                        case 5:
                            pass
                        case 6:
                            pass
                        case 7:
                            pass
                        case 8:
                            pass
                        case 9:
                            pass

app.cpu = CPU('test_opcode.ch8')


# def onAppStart(app):
#     app.rx = 200
#     app.ry = 200

# def redrawAll(app):
#         pixelSizeX = 399/32
#         pixelSizeY = 399/32
#         drawRect(app.rx, app.ry, pixelSizeX, pixelSizeY, align='center')

j = 0
for i in range(0, length, 100):
    CPU.code(i, j)
    j += 1
