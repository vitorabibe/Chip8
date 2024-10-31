from cmu_graphics import *
import random

def onAppStart(app):
    app.background='black'
    app.f = open('test_opcode.ch8', 'rb')
    app.v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    app.I = 0
    app.i = 0
    app.b = (app.f.read())
    print(len(app.b))
    app.opcode = []
    app.rx = 0
    app.ry = 0
    app.stepsPerSecond = 100
    app.pc = 1
    app.screen = [[0 for i in range(64)] for j in range(32)]
    app.setMaxShapeCount(10000)


def redrawAll(app):
        pixelX = 400/32
        pixelY = 400/64
        print
        for column in range(len(app.screen)):
            for pixel in range(len(app.screen[column])):
                if app.screen[column][pixel] == 1:
                    drawRect(pixel * pixelX, column * pixelY, pixelX, pixelY, align='center', fill='white')
                else:
                    drawRect(pixel * pixelX, column * pixelY, pixelX, pixelY, align='center', fill='black')

def onStep(app):
    readCode(app, app.pc, (app.pc - 1))
    app.pc += 2

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


def readCode(app, iteration, prevIteration):
    if iteration < len(app.b):
        for i in range(prevIteration, iteration):
            instruction = app.b[i] >> 4
            information1 = app.b[i] & 15
            information1Shifted = information1 << 8
            information2 = app.b[i+1]
            information = information1Shifted | information2
            match instruction:
                case 0:
                    app.opcode.append([instruction, one3Info(information)])
                    match one3Info(information)[2]:
                        case 0:
                            #Clear the display.
                            pass
                        case 14:
                            #The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
                            pass
                case 1:
                    i = information - 512
                    app.opcode.append([instruction, information])
                    #The interpreter sets the program counter to nnn. WHAT DOES THIS MEAN?
                case 2:
                    #The interpreter increments the stack pointer, then puts the current PC on the top of the stack. The PC is then set to nnn.
                    app.opcode.append([instruction, information])
                case 3:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    if app.v[x] == k:
                        print("skip")
                        i += 2
                case 4:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    if app.v[x] != k:
                        print("skip")
                        i += 2
                case 5:
                    app.opcode.append([instruction, one3Info(information)])
                    x, y, k = one3Info(information)
                    if app.v[x] == app.v[y]:
                        print("skip")
                        i += 2
                case 6:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    app.v[x] = k
                case 7:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    app.v[x] += k
                case 8:
                    app.opcode.append([instruction, twoOneInfo(information)])
                    x, y, k = one3Info(information)
                    match k:
                        case 0:
                            app.v[x] = app.v[y]
                        case 1:
                            app.v[x] = app.v[x] & app.v[y]
                        case 2:
                            app.v[x] = app.v[x] | app.v[y]
                        case 3:
                            app.v[x] = app.v[x] ^ app.v[y]
                        case 4:
                            set = app.v[x] + app.v[y]
                            if set > 255:
                                set | 255
                                app.v[0xF] = 1
                            else:
                                app.v[0xF] = 0
                            app.v[x] = set
                        case 5:
                            set = app.v[x] - app.v[y]
                            if set > 0:
                                app.v[0xF] = 1
                            else:
                                app.v[0xF] = 0
                            app.v[x] = set #THIS SEEMS WRONG. WHAT IF SET < 0
                        case 6:
                            if app.v[x] | 1 == 1:
                                app.v[0xF] = 1
                            else:
                                app.v[0xF] = 0
                            app.v[x] /= 2
                            pass
                        case 7:
                            set = app.v[y] - app.v[x]
                            if set > 0:
                                app.v[0xF] = 1
                            else:
                                app.v[0xF] = 0
                            app.v[x] = set #THIS SEEMS WRONG. WHAT IF SET < 0
                        case 14:
                            #If the most-significant bit of Vx is 1, then app.v[0xF] is set to 1, otherwise to 0. Then Vx is multiplied by 2.
                            pass
                case 9:
                    app.opcode.append([instruction, one3Info(information)])
                    x, y, k = one3Info(information)
                    if app.v[x] != app.v[y]:
                        print("skip")
                        i += 2
                case 10:
                    app.opcode.append([instruction, information])
                    app.I = information
                case 11:
                    app.opcode.append([instruction, information])
                    app.I = information + app.v[0]
                case 12:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    r = random.randint(0, 255)
                    app.v[x] = r & k
                case 13:
                    print("aaa")
                    app.v[0xF] = 0
                    x, y, n = one3Info(information)
                    print(n)
                    for height in range(n):
                        location = app.I & 0xFFF
                        print(location)
                        sprite = app.b[location + height - 512]
                        for bit in range(8):
                            screenX = (app.v[x] + bit) % 64
                            screenY = (app.v[y] + height) % 32
                            spritePixel = (sprite >> (7 - bit)) & 1
                            was0 = app.screen[screenY][screenX] == 0
                            app.screen[screenY][screenX] ^= spritePixel
                            if app.screen[screenY][screenX] == 0 and was0 == False:
                                app.v[0xF] = 1
                    app.opcode.append([instruction, one3Info(information)])
                case 14:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    match oneTwoInfo(information)[1]:
                        case 158:
                            pass
                        case 161:
                            pass
                case 15:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    match oneTwoInfo(information)[1]:
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
    # print(app.opcode)
    # print(app.v)
    # print(app.screen)
    
runApp()