from cmu_graphics import *
import random
import os
import time

def onAppStart(app):
    app.background='black'
    app.v = [0 for i in range(16)]
    app.I = 0
    app.i = 0
    app.opcode = []
    app.rx = 0
    app.ry = 0
    app.pc = 512
    app.screen = [[0 for i in range(64)] for j in range(32)]
    app.setMaxShapeCount(10000)
    app.CPU = 0
    app.stack = []
    app.sPointer = 0
    app.keyValue = None
    app.keyboard = {'1': 1, '2': 2, '3': 3, '4': 0xC,  'q': 4, 'w': 5, 'e': 6, 'r': 0xD,  'a': 7, 's': 8, 'd': 9, 'f': 0xE,  'z': 0xA, 'x': 0, 'c': 0xB, 'v': 0xF}
    app.keyStates = [False] * 16
    app.instruction = 0
    app.command = ''
    app.initMode = True
    app.showFiles = False
    app.showCPU = False
    app.initScreen = True
    app.fileSelected = False
    app.modeSelected = False
    app.gameColor = 'black'
    app.cpuColor = 'black'
    app.gameTextColor = 'white'
    app.cpuTextColor = 'white'
    app.selectFileColor = 'black'
    app.fileTextColor = 'white'
    app.cx = app.width // 2 + app.width // 4
    app.cy = app.height // 2
    app.mouseHasMoved = False
    app.memory = [0 for _ in range(4096)]
    app.files = findCh8Files('.ch8', findPaths('Chip8'))
    app.filesColor = ['white' for _ in range(len(app.files))]
    app.dt = 0
    app.st = 0
    app.lastTimerUpdate = time.time()
    app.lastInstructionTime = time.time()
    app.timerInterval = 1/60
    app.instructionInterval = 1/500
    app.stepsPerSecond = 500

def drawModes(app):
    drawLabel('Select Mode', app.width // 4, app.height // 4, size=app.width//15, fill='white')
    drawRect(0, app.height // 3, app.width//4, app.height // 4, fill=app.gameColor, border='white')
    drawLabel('Play Chip8 Game', app.width//8, app.height // 3 + app.height // 8, fill=app.gameTextColor)
    drawRect(app.width//4, app.height // 3, app.width//4, app.height // 4, fill=app.cpuColor, border='white')
    drawLabel('CPU simulator', app.width // 4 + app.width // 8, app.height // 3 + app.height // 8, fill=app.cpuTextColor)

def drawSelectFile(app):
    drawRect(app.width // 2 + app.width // 12, app.height // 5, app.width // 3, app.height // 10, fill=app.selectFileColor, border='white')
    drawLabel('Select File', 3 * app.width // 4, app.height // 4, size=app.width//15, fill=app.fileTextColor)

def findCh8Files(fileType, paths):
    if len(paths) == 0:
        return []
    _, extension = os.path.splitext(paths[0])
    nextPaths = findCh8Files(fileType, paths[1:])
    if fileType == extension:
        return [paths[0]] + nextPaths
    else:
        return nextPaths

def findFolderDir(folder, path):
    if folder in path:
        return path
    else:
        try:
            for directory in os.listdir(path):
                newPath = os.path.join(path, directory)
                if os.path.isdir(newPath):
                    nextPath = findFolderDir(folder, newPath)
                    if nextPath != None:
                        return nextPath
        except PermissionError:
            pass
        return None

def findPaths(folder):
    result = []
    folderDir = findFolderDir(folder, '/Users')
    for file in os.listdir(folderDir):
        result.append(file)
    return result

def drawFiles(app):
    numOfFiles = len(app.files)
    cols = 8
    rows = (numOfFiles + cols - 1) // cols
    cellWidth = app.width // cols
    cellHeight = app.height // rows
    for row in range(rows):
        for col in range(cols):
            fileIndex = row * cols + col
            if fileIndex < numOfFiles:
                rLeft = col * cellWidth
                rTop = row * cellHeight
                drawRect(rLeft, rTop, cellWidth, cellHeight, fill=app.filesColor[fileIndex], border='black', borderWidth=1)
                drawLabel(app.files[fileIndex][:-4], (rLeft + cellWidth // 2), (rTop + cellHeight // 2), fill='red', size=app.width//60)

def drawFileHoverOverColor(app, mouseX, mouseY):
    numOfFiles = len(app.files)
    cols = 8
    rows = (numOfFiles + cols - 1) // cols
    cellWidth = app.width / cols
    cellHeight = app.height / rows
    for row in range(rows):
        for col in range(cols):
            fileIndex = row * cols + col
            if fileIndex < numOfFiles:
                rLeft = col * cellWidth
                rTop = row * cellHeight
                if (rLeft <= mouseX <= rLeft + cellWidth) and (rTop <= mouseY <= rTop + cellHeight):
                    app.filesColor[fileIndex] = 'black'
                else:
                    app.filesColor[fileIndex] = 'white'

def fileSelected(app, mouseX, mouseY):
    numOfFiles = len(app.files)
    cols = 8
    rows = (numOfFiles + cols - 1) // cols
    cellWidth = app.width / cols
    cellHeight = app.height / rows
    for row in range(rows):
        for col in range(cols):
            fileIndex = row * cols + col
            if fileIndex < numOfFiles:
                rLeft = col * cellWidth
                rTop = row * cellHeight
                if (rLeft <= mouseX <= rLeft + cellWidth) and (rTop <= mouseY <= rTop + cellHeight):
                    return app.files[fileIndex]
    return None

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
    if app.initMode and not app.showFiles:
        drawInitScreen(app)
    elif app.showFiles:
        drawFiles(app)
    else:
        if app.mode == 'CPU':
            drawCPU(app)
        drawPixels(app)

def onStep(app):
    if not app.initMode:
        currentTime = time.time()
        if currentTime - app.lastTimerUpdate >= app.timerInterval:
            if app.dt > 0:
                app.dt -= 1
            if app.st > 0:
                app.st -= 1
            app.lastTimerUpdate = currentTime
        if currentTime - app.lastInstructionTime >= app.instructionInterval:
            app.CPU = app.memory[app.pc] << 8 | app.memory[app.pc + 1]
            readCode(app, app.CPU)
            app.lastInstructionTime = currentTime

def onKeyPress(app, key):
    if key in app.keyboard:
        keyIndex = app.keyboard[key]
        app.keyStates[keyIndex] = True

def onKeyRelease(app, key):
    if key in app.keyboard:
        keyIndex = app.keyboard[key]
        app.keyStates[keyIndex] = False


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
        if clickOnSelectFile(app, mouseX, mouseY) and not app.showFiles:
            app.showFiles = True
        if not clickOnSelectFile(app, mouseX, mouseY) and app.showFiles:
            selectedFile = fileSelected(app, mouseX, mouseY)
            if selectedFile != None:
                filePath = os.path.join(findFolderDir('Chip8', '/Users'), selectedFile)
                f = open(filePath, 'rb')
                program = list(f.read())
                app.memory[512:512 + len(program)] = program
                app.memory[0x1FF] = 1
                app.fileSelected = True
            app.initMode = False
            app.showFiles = False


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
                app.selectFileColor = 'white'
                app.fileTextColor = 'black'
            else:
                app.selectFileColor = 'black'
                app.fileTextColor = 'white'
        if app.showFiles:
            drawFileHoverOverColor(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    if app.width // 2 + app.width // 20 <= mouseX <= app.width - app.width // 20 and app.cy - 20 <= mouseY <= app.cy + 20:
        app.cx = mouseX
        app.mouseHasMoved = True
    # app.stepsPerSecond = app.cx % (app.width // 2 + app.width // 20) if app.cx % (app.width // 2 + app.width // 20) != 0 else 1

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
                    result = app.v[x] + app.v[y]
                    app.v[x] = result & 255
                    app.v[15] = 1 if result > 255 else 0    
                case 5:
                    app.instruction = 8.5
                    app.command = f'v[{x}] -= v[{y}]; Flag = NOT borrow'
                    oldX = app.v[x]
                    app.v[x] = (app.v[x] - app.v[y]) & 255
                    app.v[15] = 1 if oldX >= app.v[y] else 0
                case 6:
                    app.instruction = 8.6
                    app.command = f'V[{x}] shifted right, Flag = LSB'
                    oldX = app.v[x]
                    app.v[x] //= 2
                    app.v[15] = oldX & 1
                case 7:
                    app.instruction = 8.7
                    app.command = f'v[{x}] = v[{y}] - v[{x}]; Flag = NOT borrow'
                    oldX = app.v[x]
                    app.v[x] = (app.v[y] - app.v[x]) & 255
                    app.v[15] = 1 if app.v[y] >= oldX else 0
                case 14:
                    app.instruction = 8.14
                    app.command = f'VY shifted left, stored in VX, Flag = MSB'
                    oldX = app.v[x]
                    app.v[x] *= 2
                    app.v[x] &= 255
                    app.v[15] = oldX >> 7
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
            r = random.randint(0, 255)
            app.instruction = 12
            app.command = f'sets v[{x}] equal to {kk} & {r}'
            app.v[x] = r & kk
            app.pc += 2
        case 13:
            app.instruction = 13
            app.command = f'Draws from memory location {app.I} at coordinate (v[{x}], v[{y}])'
            app.v[15] = 0
            for height in range(n):
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
                    app.instruction = 14.158
                    app.command = f'skips next instruction if key pressed = v[{x}] ({app.v[x]})'
                    if app.keyStates[app.v[x]]:
                        app.pc += 4
                    else:
                        app.pc += 2
                case 161:
                    app.instruction = 14.161
                    app.command = f'skips next instruction if key not pressed = v[{x}] ({app.v[x]})'
                    if not app.keyStates[app.v[x]]:
                        app.pc += 4
                    else:
                        app.pc += 2
        case 15:
            match kk:
                case 10:
                    app.instruction = 15.10
                    app.command = f'wait for key press and store in v[{x}]'
                    pressedKeys = [i for i, pressed in enumerate(app.keyStates) if pressed]
                    if not pressedKeys:
                        return
                    else:
                        app.v[x] = pressedKeys[0]
                        app.pc += 2
                case 7:
                    app.instruction = 15.7
                    app.command = f'set v[{x}] = delay timer'
                    app.v[x] = app.dt
                    app.pc += 2
                case 15:
                    app.instruction = 15.15
                    app.command = f'set delay timer = v[{x}]'
                    app.dt = app.v[x]
                    app.pc += 2
                case 18:
                    app.instruction = 15.18
                    app.command = f'set sound timer = v[{x}]'
                    app.st = app.v[x]
                    app.pc += 2
                case 21:
                    app.dt = app.v[x]
                    app.pc += 2
                case 24:
                    app.st = app.v[x]
                    app.pc += 2
                case 30:
                    app.instruction = 15.30
                    app.command = f'I += v[{x}]'
                    app.I = (app.I + app.v[x]) & 0xFFF
                    app.pc += 2
                case 51:
                    app.instruction = 15.51
                    app.command = f'I, I+1, I+2 = BCD of v{[x]}'
                    hundreds = app.v[x] // 100 % 10
                    tens = app.v[x] // 10 % 10
                    ones = app.v[x] % 10
                    app.memory[app.I] = hundreds
                    app.memory[app.I + 1] = tens
                    app.memory[app.I + 2] = ones
                    app.pc += 2
                case 41:
                    app.instruction = 15.41
                    app.command = f'I = v{[x]} sprite location'
                    app.I = app.v[x] * 5
                    app.pc += 2
                case 85:
                    app.instruction = 15.85
                    app.command = f'writes v[0], v[{x}] in memory I, I + {x}'
                    for i in range(x + 1):
                        app.memory[app.I + i] = app.v[i] % 256
                    app.pc += 2
                case 101:
                    app.instruction = 15.85
                    app.command = f'reads memory I, I + {x} in v[0], v[{x}]'
                    for i in range(x + 1):
                        app.v[i] = app.memory[app.I + i]
                        app.v[i] = app.v[i] % 256
                    app.pc += 2

runApp()