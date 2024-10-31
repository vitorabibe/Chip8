from cmu_graphics import *
import random
import copy

def onAppStart(app):
    app.background='black'
    app.f = open('5-quirks.ch8', 'rb')
    app.v = [0 for i in range(16)]
    app.I = 0
    app.i = 0
    app.a = list((app.f.read()))
    app.b = copy.copy(app.a)
    print(len(app.b))
    app.opcode = []
    app.rx = 0
    app.ry = 0
    app.stepsPerSecond = 100
    app.pc = 0
    app.screen = [[0 for i in range(64)] for j in range(32)]
    app.setMaxShapeCount(10000)
    app.CPU = []
    app.stack = []
    app.sPointer = 0
    app.keyboard = {'1': 1, '2': 2, '3': 3, '4': 12, 'q': 4, 'w': 5, 'e': 6, 'r': 13, 'a': 7, 's': 8, 'd': 9, 'f': 14, 'z': 10, 'x': 0, 'c': 11, 'v': 15}
    app.keyValue = 0

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
        drawLabel(f'PC = {app.pc}', 450, 450, fill='white')

def onStep(app):
    readCode(app)
    app.CPU = app.b[app.pc:app.pc + 2]
    app.pc += 2

def onKeyPress(app, key):
    app.keyValue = app.keyboard[key]

def onKeyRelease(app, key):
    app.keyValue = 0

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


def readCode(app):
    if len(app.CPU) > 0:
        for byte in range(0, len(app.CPU), 2):
            instruction = app.CPU[byte] >> 4
            information1 = app.CPU[byte] & 15
            information1Shifted = information1 << 8
            information2 = app.CPU[byte + 1]
            information = information1Shifted | information2
            match instruction:
                case 0:
                    app.opcode.append([instruction, one3Info(information)])
                    match one3Info(information)[2]:
                        case 0:
                            app.screen = [[0 for i in range(64)] for j in range(32)]
                            pass
                        case 14:
                            if app.sPointer > 0:
                                app.sPointer -= 1
                            if len(app.stack) > 0:
                                app.pc = app.stack[app.sPointer]
                case 1:
                    app.pc = information - 512
                    app.opcode.append([instruction, information])
                case 2:
                    if len(app.stack) < 16:
                        app.stack.append(app.pc)
                        app.sPointer += 1
                    app.pc = information - 512
                    app.opcode.append([instruction, information])
                case 3:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    if app.v[x] == k:
                        print("skip")
                        app.pc += 2
                case 4:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    if app.v[x] != k:
                        print("skip")
                        app.pc += 2
                case 5:
                    app.opcode.append([instruction, one3Info(information)])
                    x, y, k = one3Info(information)
                    if app.v[x] == app.v[y]:
                        print("skip")
                        app.pc += 2
                case 6:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    app.v[x] = k
                case 7:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, k = oneTwoInfo(information)
                    app.v[x] += k
                    app.v[x] = app.v[x] % 256
                case 8:
                    app.opcode.append([instruction, twoOneInfo(information)])
                    x, y, k = one3Info(information)
                    match k:
                        case 0:
                            app.v[x] = app.v[y]
                        case 1:
                            app.v[x] = app.v[x] | app.v[y]
                        case 2:
                            app.v[x] = app.v[x] & app.v[y]
                        case 3:
                            app.v[x] = app.v[x] ^ app.v[y]
                        case 4:
                            set = app.v[x] + app.v[y]
                            if set >> 8 > 0:
                                app.v[15] = 1
                            else:
                                app.v[15] = 0
                            app.v[x] = set & 255
                        case 5:
                            set = app.v[x] - app.v[y]
                            if app.v[x] > app.v[y]:
                                app.v[15] = 1
                            else:
                                app.v[15] = 0
                            app.v[x] = set & 255
                        case 6:
                            app.v[x] = app.v[y] // 2
                            if app.v[x] & 1 == 1:
                                app.v[15] = 1
                            else:
                                app.v[15] = 0
                        case 7:
                            set = app.v[y] - app.v[x]
                            if app.v[y] > app.v[x]:
                                app.v[15] = 1
                            else:
                                app.v[15] = 0
                            app.v[x] = set & 255
                        case 14:
                            app.v[x] = app.v[y] * 2
                            app.v[x] %= 256
                            if app.v[x] & 128 == 1:
                                app.v[15] = 1
                            else:
                                app.v[15] = 0
                case 9:
                    app.opcode.append([instruction, one3Info(information)])
                    x, y, k = one3Info(information)
                    if app.v[x] != app.v[y]:
                        print("skip")
                        app.pc += 2
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
                    app.v[15] = 0
                    x, y, n = one3Info(information)
                    for height in range(n):
                        print(app.I + height - 512)
                        print(len(app.b))
                        sprite = app.b[app.I + height - 512]
                        for bit in range(8):
                            screenX = (app.v[x] + bit) % 64
                            screenY = (app.v[y] + height) % 32
                            spritePixel = (sprite >> (7 - bit)) & 1
                            was0 = app.screen[screenY][screenX] == 0
                            app.screen[screenY][screenX] ^= spritePixel
                            if app.screen[screenY][screenX] == 0 and was0 == False:
                                app.v[15] = 1
                    app.opcode.append([instruction, one3Info(information)])
                case 14:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    match oneTwoInfo(information)[1]:
                        case 158:
                            if app.keyValue != app.v[x]:
                                pc += 2
                        case 161:
                            if app.keyValue == app.v[x]:
                                pc += 2
                case 15:
                    app.opcode.append([instruction, oneTwoInfo(information)])
                    x, y = oneTwoInfo(information)
                    match y:
                        case 10:
                            while app.keyValue != 0:
                                continue
                            app.v[x] = app.keyValue
                        case 7:
                            app.v[x] = app.dt
                        case 21:
                            app.dt = app.v[x]
                        case 24:
                            app.st = app.v[x]
                        case 30:
                            app.I += app.v[x]
                        case 30:
                            app.I += app.v[x]
                        case 51:
                            hundreds = app.v[x] // 100 % 10
                            tens = app.v[x] // 10 % 10
                            ones = app.v[x] % 10
                            app.b[app.I - 512] = hundreds
                            app.b[app.I + 1 - 512] = tens
                            app.b[app.I + 2 - 512] = ones
                        case 41:
                            app.I = app.v[x] * 5
                        case 85:
                            for i in range(x + 1):
                                app.b[app.I + i - 512] = app.v[i] % 256
                        case 101:
                            for i in range(x + 1):
                                app.v[i] = app.b[app.I + i - 512]
                                app.v[i] = app.v[i] % 256
        # print(app.opcode)
        # print(app.v)
        # print(app.screen)
    
runApp()