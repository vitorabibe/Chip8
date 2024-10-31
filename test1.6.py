from cmu_graphics import *
import random
import copy

def onAppStart(app):
    app.background='black'
    app.f = open('3-corax+.ch8', 'rb')
    app.v = [0 for i in range(16)]
    app.I = 0
    app.i = 0
    app.a = list((app.f.read()))
    program = copy.copy(app.a)
    app.memory = [0 for i in range(4096)]
    app.memory[512:512 + len(program)] = program
    app.opcode = []
    app.rx = 0
    app.ry = 0
    app.pc = 512
    app.screen = [[0 for i in range(64)] for j in range(32)]
    app.setMaxShapeCount(10000)
    app.CPU = 0
    app.stack = []
    app.sPointer = 0
    app.keyboard = {'1': 1, '2': 2, '3': 3, '4': 12, 'q': 4, 'w': 5, 'e': 6, 'r': 13, 'a': 7, 's': 8, 'd': 9, 'f': 14, 'z': 10, 'x': 0, 'c': 11, 'v': 15}
    app.keyValue = 0
    app.instruction = 0
    app.command = ''
    app.initMode = True
    app.showCPU = False
    app.initScreen = True
    app.fileSelected = False
    app.modeSelected = False
    app.gameColor = 'black'
    app.cpuColor = 'black'
    app.gameTextColor = 'white'
    app.cpuTextColor = 'white'
    app.fileColor = 'black'
    app.fileTextColor = 'white'
    app.cx = app.width // 2 + app.width // 4
    app.cy = app.height // 2
    app.mouseHasMoved = False

def drawModes(app):
    drawLabel('Select Mode', app.width // 4, app.height // 4, size=app.width//15, fill='white')
    drawRect(0, app.height // 3, app.width//4, app.height // 4, fill=app.gameColor, border='white')
    drawLabel('Play Chip8 Game', app.width//8, app.height // 3 + app.height // 8, fill=app.gameTextColor)
    drawRect(app.width//4, app.height // 3, app.width//4, app.height // 4, fill=app.cpuColor, border='white')
    drawLabel('CPU simulator', app.width // 4 + app.width // 8, app.height // 3 + app.height // 8, fill=app.cpuTextColor)

def drawSelectFile(app):
    drawRect(app.width // 2 + app.width // 12, app.height // 5, app.width // 3, app.height // 10, fill=app.fileColor, border='white')
    drawLabel('Select File', 3 * app.width // 4, app.height // 4, size=app.width//15, fill=app.fileTextColor)

def drawStepsPerSecond(app):
    r = app.width // 60
    n = app.stepsPerSecond if app.mouseHasMoved else app.cx % (app.width // 2 + app.width // 20)
    drawLine(app.width // 2 + app.width // 20, app.height // 2, app.width - app.width // 20, app.height // 2, fill='white')
    drawCircle(app.cx, app.cy, r, fill='white')
    drawLabel(f'{n} steps per second', app.width // 2 + app.width // 4, app.height // 2 - app.height // 8, fill='white')

def drawInitScreen(app):
    drawModes(app)
    drawSelectFile(app)
    drawStepsPerSecond(app)

def drawPixels(app):
    if app.mode == 'game':
        xInit = 0
        yInit = 0
        width, height = app.width, app.height
    else:
        xInit = app.width // 6 + 20
        yInit = app.height // 10 + 20
        width, height = app.width - xInit, app.height - yInit
    pixelX = (width) // 64
    pixelY = (height) // 32
    for row in range(len(app.screen)):
        for pixel in range(len(app.screen[row])):
            if app.screen[row][pixel] == 1:
                drawRect(xInit + (pixel * pixelX), yInit + row * pixelY, pixelX, pixelY, align='center', fill='white')
            else:
                drawRect(xInit + (pixel * pixelX), yInit + row * pixelY, pixelX, pixelY, align='center', fill='black')

def drawPC(app):
    pcX = 0
    pcY = 0
    pcLen = app.width // 6
    pcHeight = app.height // 20
    drawRect(pcX, pcY, pcLen, pcHeight, fill=None, border='white')
    if 'PC' in app.command:
        color = 'red'
    else:
        color = 'white'
    drawLabel(f'PC: {app.pc}', pcX + (pcLen) // 2, pcY + (pcHeight // 2), size = pcLen // 5, fill=color)

def drawOpcode(app, opcode):
    opcodeX = app.width // 6
    opcodeY = 0
    opcodeLen = app.width - app.width // 6
    opcodeHeight = app.height // 20
    opcode = f'{opcode:016b}'
    drawRect(opcodeX, opcodeY, opcodeLen, opcodeHeight, fill=None, border='white')
    drawLabel(f'Opcode: {opcode}', opcodeX + (opcodeLen) // 2, opcodeY + (opcodeHeight // 2), size = opcodeLen // 20, fill='white')

def drawInstruction(app):
    opcodeX = 0
    opcodeY = app.height // 20
    opcodeLen = app.width
    opcodeHeight = app.height // 20
    drawRect(opcodeX, opcodeY, opcodeLen, opcodeHeight, fill=None, border='white')
    drawLabel(f'Instruction: {app.instruction}, {app.command}', opcodeX + (opcodeLen) // 2, opcodeY + (opcodeHeight // 2), size = opcodeLen // 30, fill='white')

def drawI(app):
    x = 0
    y = app.height // 10
    len = app.width // 6
    height = app.height // 20
    drawRect(x, y, len, height, fill=None, border='white')
    if 'I' in app.command:
        color = 'red'
    else:
        color = 'white'
    drawLabel(f'I: {app.I}', x + (len) // 2, y + (height // 2), size = len // 5, fill=color)

def drawRegisters(app):
    xInit = 0
    yInit = 3 * (app.height // 20)
    len = app.width // 6
    height = app.height // 20
    drawRect(xInit, yInit, len, height, fill=None, border='white')
    drawLabel('Registers:', xInit + len // 2, yInit + height // 2, size = len // 7, fill='white')
    for i in range(16):
        y = yInit + (height * i) + height
        if f'v[{i}]' in app.command:
            color = 'red'
        else:
            color = 'white'
        if not i == 15:
            drawRect(xInit, y, len, height, fill=None, border='white')
            drawLabel(f'v[{i}] = {app.v[i]}', xInit + len // 2, y + height // 2, size = len // 7, fill=color)
        else:
            drawRect(xInit, y, len, height, fill=None, border='white')
            drawLabel(f'Flag: {app.v[i]}', xInit + len // 2, y + height // 2, size = len // 7, fill=color)

def drawCPU(app):
    opcode = app.memory[app.pc] << 8 | app.memory[app.pc + 1]
    drawRect(0, 0, app.width, app.height, fill=None, border='white')
    drawPC(app)
    drawOpcode(app, opcode)
    drawInstruction(app)
    drawI(app)
    drawRegisters(app)

def redrawAll(app):
    if app.initMode:
        drawInitScreen(app)
    else:
        if app.mode == 'CPU':
            drawCPU(app)
        drawPixels(app)

def onStep(app):
    if app.initMode == False:
        app.CPU = app.memory[app.pc] << 8 | app.memory[app.pc + 1]
        print(app.pc)
        readCode(app, app.CPU)

def onKeyPress(app, key):
    app.keyValue = app.keyboard[key]

def onKeyRelease(app, key):
    app.keyValue = 0

def clickOnMode(app, mouseX, mouseY):
        if not app.modeSelected:
            if app.height // 3 <= mouseY <= ((app.height // 3) + (app.height // 4)):
                if 0 < mouseX < app.width // 4:
                    app.mode = 'game'
                    app.modeSelected = True

                elif app.width // 4 < mouseX < app.width // 2:
                    app.mode = 'CPU'
                    app.modeSelected = True

def clickOnSelectFile(app, mouseX, mouseY):
    if not app.fileSelected and app.width // 2 + app.width // 12 < mouseX <  app.width // 2 + app.width // 12 + app.width // 3 and app.height // 5 < mouseY < app.height // 5 + app.height // 10:
        return True

def onMousePress(app, mouseX, mouseY):
    if app.initScreen:
        clickOnMode(app, mouseX, mouseY)
        if clickOnSelectFile(app, mouseX, mouseY):
            #open File picker
            #app.file = file opened
            app.fileSelected = True
        if app.modeSelected and app.fileSelected:
            app.initMode = False

def onMouseMove(app, mouseX, mouseY):
    if app.initScreen:
        if not app.modeSelected:
            if app.height // 3 <= mouseY <= ((app.height // 3) + (app.height // 4)):
                if 0 < mouseX < app.width // 4:
                    app.gameColor = 'white'
                    app.gameTextColor = 'black'
                    app.cpuColor = 'black'
                    app.cpuTextColor = 'white'

                elif app.width // 4 < mouseX < app.width // 2:
                    app.gameColor = 'black'
                    app.gameTextColor = 'white'
                    app.cpuColor = 'white'
                    app.cpuTextColor = 'black'
                else:
                    app.gameColor = 'black'
                    app.gameTextColor = 'white'
                    app.cpuColor = 'black'
                    app.cpuTextColor = 'white'
            else:
                app.gameColor = 'black'
                app.gameTextColor = 'white'
                app.cpuColor = 'black'
                app.cpuTextColor = 'white'
        if not app.fileSelected:
            if app.width // 2 + app.width // 12 < mouseX <  app.width // 2 + app.width // 12 + app.width // 3 and app.height // 5 < mouseY < app.height // 5 + app.height // 10:
                app.fileColor = 'white'
                app.fileTextColor = 'black'
            else:
                app.fileColor = 'black'
                app.fileTextColor = 'white'

def onMouseDrag(app, mouseX, mouseY):
    if app.width // 2 + app.width // 20 <= mouseX <= app.width - app.width // 20 and app.cy - 20 <= mouseY <= app.cy + 20:
        app.cx = mouseX
        app.mouseHasMoved = True
    app.stepsPerSecond = app.cx % (app.width // 2 + app.width // 20) if app.cx % (app.width // 2 + app.width // 20) != 0 else 1

def readCode(app, opcode):
    instruction = opcode >> 12
    x = (opcode >> 8) & 0x0F
    y = (opcode >> 4) & 0x0F
    n = opcode & 0x000F
    kk = opcode & 0x00FF
    nnn = opcode & 0x0FFF
    match instruction:
        case 0:
            if opcode == 0x00E0:
                app.instruction = 0.0
                app.command = 'clears screen'
                app.screen = [[0 for _ in range(64)] for _ in range(32)]
                app.pc += 2
            elif opcode == 0x00EE:
                app.instruction = 0.14
                app.command = 'returns from subroutine'
                app.pc = app.stack.pop()
            else:
                app.pc += 2          
        case 1:
            app.instruction = 1
            app.command = f'set PC to {nnn}'
            app.pc = nnn
        case 2:
            app.instruction = 2
            app.command = f'append PC to stack, set PC to {nnn}'
            app.stack.append(app.pc + 2)
            app.pc = nnn
        case 3:
            app.instruction = 3
            app.command = f'skips next instruction if v[{x}] == {kk}'
            if app.v[x] == kk:
                app.pc += 4
            else:
                app.pc += 2
        case 4:
            app.instruction = 4
            app.command = f'skips next instruction if v[{x}] != {kk}'
            if app.v[x] != kk:
                app.pc += 4
            else:
                app.pc += 2
        case 5:
            app.instruction = 5
            app.command = f'skips next instruction if v[{x}] == v[{y}]'
            if app.v[x] == app.v[y]:
                app.pc += 4
            else:
                app.pc += 2
        case 6:
            app.instruction = 6
            app.command = f'set v[{x}] = {kk}'
            app.v[x] = kk
            app.pc += 2
        case 7:
            app.instruction = 7
            app.command = f'adds {kk} to v[{x}]'
            app.v[x] += kk
            app.v[x] = app.v[x] % 256
            app.pc += 2
        case 8:
            match n:
                case 0:
                    app.instruction = 8.0
                    app.command = f'v[{x}] = v[{y}]'
                    app.v[x] = app.v[y]
                case 1:
                    app.instruction = 8.1
                    app.command = f'v[{x}] is ORed by v[{y}]'
                    app.v[x] |= app.v[y]
                case 2:
                    app.instruction = 8.2
                    app.command = f'v[{x}] is ANDed by v[{y}]'
                    app.v[x] &= app.v[y]
                case 3:
                    app.instruction = 8.3
                    app.command = f'v[{x}] is XORed by v[{y}]'
                    app.v[x] ^= app.v[y]
                case 4:
                    app.instruction = 8.4
                    app.command = f'v[{x}] += v[{y}]; Flag = carry'
                    set = app.v[x] + app.v[y]
                    if set > 255:
                        app.v[15] = 1
                    else:
                        app.v[15] = 0
                    app.v[x] = set & 255
                case 5:
                    app.instruction = 8.5
                    app.command = f'v[{x}] -= v[{y}]; Flag = NOT sign bit'
                    set = app.v[x] - app.v[y]
                    if app.v[x] >= app.v[y]:
                        app.v[15] = 1
                    else:
                        app.v[15] = 0
                    app.v[x] = set & 255
                case 6:
                    app.instruction = 8.6
                    app.command = f'Flag = v[{x}] LSB; v[{x}] is shifted right by 1'
                    app.v[15] = app.v[x] & 1
                    app.v[x] //= 2
                case 7:
                    app.instruction = 8.7
                    app.command = f'v[{y}] -= v[{x}]; Flag = NOT sign bit'                    
                    set = app.v[y] - app.v[x]
                    if app.v[y] > app.v[x]:
                        app.v[15] = 1
                    else:
                        app.v[15] = 0
                    app.v[x] = set & 255
                case 14:
                    app.instruction = 8.14
                    app.command = f'Flag = v[{x}] MSB; v[{x}] is shifted left by 1'
                    app.v[15] = app.v[x] & 128
                    app.v[x] = app.v[x] * 2
                    app.v[x] %= 256
            app.pc += 2
        case 9:
            app.instruction = 9
            app.command = f'skips next instruction if v[{x}] != v[{y}]'
            if app.v[x] != app.v[y]:
                app.pc += 4
            else:
                app.pc += 2
        case 10:
            app.instruction = 10
            app.command = f'sets I = {nnn}'
            app.I = nnn
            app.pc += 2
        case 11:
            app.instruction = 11
            app.command = f'sets PC to {nnn} + v[0]({app.v[0]})'
            app.pc = nnn + app.v[0]
        case 12:
            app.instruction = 12
            app.command = f'sets v[{x}] equal to {kk} & {r}'
            r = random.randint(0, 255)
            app.v[x] = r & kk
            app.pc += 2
        case 13:
            app.instruction = 13
            app.command = f'Draws from memory location {app.I} at coordinate (v[{x}], v[{y}])'
            app.v[15] = 0
            for height in range(n):
                print(app.I + height)
                sprite = app.memory[app.I + height]
                for bit in range(8):
                    screenX = (app.v[x] + bit) % 64
                    screenY = (app.v[y] + height) % 32
                    spritePixel = (sprite >> (7 - bit)) & 1
                    was0 = app.screen[screenY][screenX] == 0
                    app.screen[screenY][screenX] ^= spritePixel
                    if app.screen[screenY][screenX] == 0 and was0 == False:
                        app.v[15] = 1
            app.pc += 2
        case 14:
            match kk:
                case 158:
                    if app.keyValue == app.v[x]:
                        app.instruction = 14.158
                        app.command = f'skips next instruction if key pressed = {app.keyboard[app.keyValue]}'
                        app.pc += 4
                    else:
                        app.pc += 2
                case 161:
                    app.instruction = 14.161
                    app.command = f'skips next instruction if key pressed != {app.keyboard[app.keyValue]}'
                    if app.keyValue != app.v[x]:
                        app.pc += 4
                    else:
                        app.pc += 2
        case 15:
            match kk:
                case 10:
                    app.instruction = 15.10
                    app.command = f'sets v[{x}] = {app.keyboard[app.keyValue]}'
                    if app.keyValue == None:
                        pass
                    else:
                        app.v[x] = app.keyValue
                case 7:
                    app.v[x] = app.dt
                case 21:
                    app.dt = app.v[x]
                case 24:
                    app.st = app.v[x]
                case 30:
                    app.instruction = 15.10
                    app.command = f'I += v[{x}]'
                    app.I += app.v[x]
                case 51:
                    app.instruction = 15.51
                    app.command = f'I, I+1, I+2 = BCD of v{[x]}'
                    hundreds = app.v[x] // 100 % 10
                    tens = app.v[x] // 10 % 10
                    ones = app.v[x] % 10
                    app.memory[app.I] = hundreds
                    app.memory[app.I + 1] = tens
                    app.memory[app.I + 2] = ones
                case 41:
                    app.instruction = 15.41
                    app.command = f'I = v{[x]} sprite location'
                    app.I = app.v[x] * 5
                case 85:
                    app.instruction = 15.85
                    app.command = f'writes v[0], v[{x}] in memory I, I + {x}'
                    for i in range(x + 1):
                        app.memory[app.I + i] = app.v[i] % 256
                case 101:
                    app.instruction = 15.85
                    app.command = f'reads memory I, I + {x} in v[0], v[{x}]'
                    for i in range(x + 1):
                        app.v[i] = app.memory[app.I + i]
                        app.v[i] = app.v[i] % 256
            app.pc += 2

runApp()