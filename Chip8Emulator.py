from cmu_graphics import *
import random
import os
import time
import copy

class Cpu:
    def __init__(self):
        self.v = [0 for i in range(16)]
        self.I = 0
        self.i = 0
        self.opcode = []
        self.CPU = 0
        self.pc = 512
        self.stack = []
        self.sPointer = 0
        self.keyValue = None
        self.keyboard = {'1': 1, '2': 2, '3': 3, '4': 0xC,  'q': 4, 'w': 5, 'e': 6, 'r': 0xD,  'a': 7, 's': 8, 'd': 9, 'f': 0xE,  'z': 0xA, 'x': 0, 'c': 0xB, 'v': 0xF}
        self.keyStates = [False] * 16
        self.screen = [[0 for _ in range(64)] for _ in range(32)]
        self.instruction = 0
        self.command = ''
        self.memory = [0 for _ in range(4096)]
        self.dt = 0
        self.st = 0
    
    def write(self, program):
        self.memory[512:] = program
    
    def read(self, opcode):
        instruction = opcode >> 12
        x = (opcode >> 8) & 0x0F
        y = (opcode >> 4) & 0x0F
        n = opcode & 0x000F
        kk = opcode & 0x00FF
        nnn = opcode & 0x0FFF
        match instruction:
            case 0:
                if opcode == 0x00E0:
                    self.instruction = 0.0
                    self.command = 'clears screen'
                    self.screen = [[0 for _ in range(64)] for _ in range(32)]
                    self.pc += 2
                elif opcode == 0x00EE:
                    self.instruction = 0.14
                    self.command = 'returns from subroutine'
                    self.pc = self.stack.pop()
                else:
                    self.pc += 2          
            case 1:
                self.instruction = 1
                self.command = f'set PC to {nnn}'
                self.pc = nnn
            case 2:
                self.instruction = 2
                self.command = f'append PC to stack, set PC to {nnn}'
                self.stack.append(self.pc + 2)
                self.pc = nnn
            case 3:
                self.instruction = 3
                self.command = f'skips next instruction if v[{x}] == {kk}'
                if self.v[x] == kk:
                    self.pc += 4
                else:
                    self.pc += 2
            case 4:
                self.instruction = 4
                self.command = f'skips next instruction if v[{x}] != {kk}'
                if self.v[x] != kk:
                    self.pc += 4
                else:
                    self.pc += 2
            case 5:
                self.instruction = 5
                self.command = f'skips next instruction if v[{x}] == v[{y}]'
                if self.v[x] == self.v[y]:
                    self.pc += 4
                else:
                    self.pc += 2
            case 6:
                self.instruction = 6
                self.command = f'set v[{x}] = {kk}'
                self.v[x] = kk
                self.pc += 2
            case 7:
                self.instruction = 7
                self.command = f'adds {kk} to v[{x}]'
                self.v[x] += kk
                self.v[x] = self.v[x] % 256
                self.pc += 2
            case 8:
                match n:
                    case 0:
                        self.instruction = 8.0
                        self.command = f'v[{x}] = v[{y}]'
                        self.v[x] = self.v[y]
                    case 1:
                        self.instruction = 8.1
                        self.command = f'v[{x}] is ORed by v[{y}]'
                        self.v[x] |= self.v[y]
                    case 2:
                        self.instruction = 8.2
                        self.command = f'v[{x}] is ANDed by v[{y}]'
                        self.v[x] &= self.v[y]     
                    case 3:
                        self.instruction = 8.3
                        self.command = f'v[{x}] is XORed by v[{y}]'
                        self.v[x] ^= self.v[y]   
                    case 4:
                        self.instruction = 8.4
                        self.command = f'v[{x}] += v[{y}]; Flag = carry'
                        result = self.v[x] + self.v[y]
                        self.v[x] = result & 255
                        self.v[15] = 1 if result > 255 else 0    
                    case 5:
                        self.instruction = 8.5
                        self.command = f'v[{x}] -= v[{y}]; Flag = NOT borrow'
                        oldX = self.v[x]
                        self.v[x] = (self.v[x] - self.v[y]) & 255
                        self.v[15] = 1 if oldX >= self.v[y] else 0
                    case 6:
                        self.instruction = 8.6
                        self.command = f'V[{x}] shifted right, Flag = LSB'
                        oldX = self.v[x]
                        self.v[x] //= 2
                        self.v[15] = oldX & 1
                    case 7:
                        self.instruction = 8.7
                        self.command = f'v[{x}] = v[{y}] - v[{x}]; Flag = NOT borrow'
                        oldX = self.v[x]
                        self.v[x] = (self.v[y] - self.v[x]) & 255
                        self.v[15] = 1 if self.v[y] >= oldX else 0
                    case 14:
                        self.instruction = 8.14
                        self.command = f'VY shifted left, stored in VX, Flag = MSB'
                        oldX = self.v[x]
                        self.v[x] *= 2
                        self.v[x] &= 255
                        self.v[15] = oldX >> 7
                self.pc += 2
            case 9:
                self.instruction = 9
                self.command = f'skips next instruction if v[{x}] != v[{y}]'
                if self.v[x] != self.v[y]:
                    self.pc += 4
                else:
                    self.pc += 2
            case 10:
                self.instruction = 10
                self.command = f'sets I = {nnn}'
                self.I = nnn
                self.pc += 2
            case 11:
                self.instruction = 11
                self.command = f'sets PC to {nnn} + v[0]({self.v[0]})'
                self.pc = nnn + self.v[0]
            case 12:
                r = random.randint(0, 255)
                self.instruction = 12
                self.command = f'sets v[{x}] equal to {kk} & {r}'
                self.v[x] = r & kk
                self.pc += 2
            case 13:
                self.instruction = 13
                self.command = f'Draws from memory location {self.I} at coordinate (v[{x}], v[{y}])'
                self.v[15] = 0
                for height in range(n):
                    sprite = self.memory[self.I + height]
                    for bit in range(8):
                        screenX = (self.v[x] + bit) % 64
                        screenY = (self.v[y] + height) % 32
                        spritePixel = (sprite >> (7 - bit)) & 1
                        was0 = self.screen[screenY][screenX] == 0
                        self.screen[screenY][screenX] ^= spritePixel
                        if self.screen[screenY][screenX] == 0 and was0 == False:
                            self.v[15] = 1
                self.pc += 2
            case 14:
                match kk:
                    case 158:
                        self.instruction = 14.158
                        self.command = f'skips next instruction if key pressed = v[{x}] ({self.v[x]})'
                        if self.keyStates[self.v[x]]:
                            self.pc += 4
                        else:
                            self.pc += 2
                    case 161:
                        self.instruction = 14.161
                        self.command = f'skips next instruction if key not pressed = v[{x}] ({self.v[x]})'
                        if not self.keyStates[self.v[x]]:
                            self.pc += 4
                        else:
                            self.pc += 2
            case 15:
                match kk:
                    case 10:
                        self.instruction = 15.10
                        self.command = f'wait for key press and store in v[{x}]'
                        pressedKeys = [i for i, pressed in enumerate(self.keyStates) if pressed]
                        if not pressedKeys:
                            return
                        else:
                            self.v[x] = pressedKeys[0]
                            self.pc += 2
                    case 7:
                        self.instruction = 15.7
                        self.command = f'set v[{x}] = delay timer'
                        self.v[x] = self.dt
                        self.pc += 2
                    case 15:
                        self.instruction = 15.15
                        self.command = f'set delay timer = v[{x}]'
                        self.dt = self.v[x]
                        self.pc += 2
                    case 18:
                        self.instruction = 15.18
                        self.command = f'set sound timer = v[{x}]'
                        self.st = self.v[x]
                        self.pc += 2
                    case 21:
                        self.dt = self.v[x]
                        self.pc += 2
                    case 24:
                        self.st = self.v[x]
                        self.pc += 2
                    case 30:
                        self.instruction = 15.30
                        self.command = f'I += v[{x}]'
                        self.I = (self.I + self.v[x]) & 0xFFF
                        self.pc += 2
                    case 51:
                        self.instruction = 15.51
                        self.command = f'I, I+1, I+2 = BCD of v{[x]}'
                        hundreds = self.v[x] // 100 % 10
                        tens = self.v[x] // 10 % 10
                        ones = self.v[x] % 10
                        self.memory[self.I] = hundreds
                        self.memory[self.I + 1] = tens
                        self.memory[self.I + 2] = ones
                        self.pc += 2
                    case 41:
                        self.instruction = 15.41
                        self.command = f'I = v{[x]} sprite location'
                        self.I = self.v[x] * 5
                        self.pc += 2
                    case 85:
                        self.instruction = 15.85
                        self.command = f'writes v[0], v[{x}] in memory I, I + {x}'
                        for i in range(x + 1):
                            self.memory[self.I + i] = self.v[i] % 256
                        self.pc += 2
                    case 101:
                        self.instruction = 15.85
                        self.command = f'reads memory I, I + {x} in v[0], v[{x}]'
                        for i in range(x + 1):
                            self.v[i] = self.memory[self.I + i]
                            self.v[i] = self.v[i] % 256
                        self.pc += 2

class Screen:
    def __init__(self, app):
        self.rx = 0
        self.ry = 0
        self.cx = app.width // 2 + app.width // 4
        self.cy = app.height // 2
        self.screen = [[0 for i in range(64)] for j in range(32)]
        self.gameColor = 'black'
        self.cpuColor = 'black'
        self.gameTextColor = 'white'
        self.cpuTextColor = 'white'
        self.selectFileColor = 'black'
        self.fileTextColor = 'white'
        self.width = app.width
        self.height = app.height
        self.stepsPerSecond = app.stepsPerSecond
        self.mouseHasMoved = app.mouseHasMoved
    
    def drawInitScreen(self):
        Screen.drawModes(self)
        Screen.drawSelectFile(self)
        Screen.drawStepsPerSecond(self)
    
    def drawModes(self):
        drawLabel('Select Mode', self.width // 4, self.height // 4, size=self.width//15, fill='white')
        drawRect(0, self.height // 3, self.width//4, self.height // 4, fill=self.gameColor, border='white')
        drawLabel('Play Chip8 Game', self.width//8, self.height // 3 + self.height // 8, fill=self.gameTextColor)
        drawRect(self.width//4, self.height // 3, self.width//4, self.height // 4, fill=self.cpuColor, border='white')
        drawLabel('CPU simulator', self.width // 4 + self.width // 8, self.height // 3 + self.height // 8, fill=self.cpuTextColor)

    def drawSelectFile(self):
        drawRect(self.width // 2 + self.width // 12, self.height // 5, self.width // 3, self.height // 10, fill=self.selectFileColor, border='white')
        drawLabel('Select File', 3 * self.width // 4, self.height // 4, size=self.width//15, fill=self.fileTextColor)

    def drawStepsPerSecond(self):
        r = self.width // 60
        n = str(self.stepsPerSecond)[:-2] if self.mouseHasMoved else (3.125 * (self.cx % (self.width // 2 + self.width // 20))) // 1
        drawLine(self.width // 2 + self.width // 20, self.height // 2, self.width - self.width // 20, self.height // 2, fill='white')
        drawCircle(self.cx, self.cy, r, fill='white')
        drawLabel(f'{n} steps per second', self.width // 2 + self.width // 4, self.height // 2 - self.height // 8, fill='white')

    def drawFiles(self, app):
        if app.displayedFiles != []:
            numOfFiles = len(app.displayedFiles)
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
                        drawLabel(app.displayedFiles[fileIndex], (rLeft + cellWidth // 2), (rTop + cellHeight // 2), fill='red', size=self.width//60)

    def drawCPU(self, app):
        opcode = app.cpu.memory[app.cpu.pc] << 8 | app.cpu.memory[app.cpu.pc + 1]
        drawRect(0, 0, self.width, self.height, fill=None, border='white')
        Screen.drawPC(self, app)
        Screen.drawOpcode(self, opcode)
        Screen.drawInstruction(self, app)
        Screen.drawI(self, app)
        Screen.drawRegisters(self, app)
    
    def drawPC(self, app):
        pcX = 0
        pcY = 0
        pcLen = self.width // 6
        pcHeight = self.height // 20
        drawRect(pcX, pcY, pcLen, pcHeight, fill=None, border='white')
        if 'PC' in app.cpu.command:
            color = 'red'
        else:
            color = 'white'
        drawLabel(f'PC: {app.cpu.pc}', pcX + (pcLen) // 2, pcY + (pcHeight // 2), size = pcLen // 5, fill=color)

    def drawOpcode(self, opcode):
        opcodeX = self.width // 6
        opcodeY = 0
        opcodeLen = self.width - self.width // 6
        opcodeHeight = self.height // 20
        opcode = f'{opcode:016b}'
        drawRect(opcodeX, opcodeY, opcodeLen, opcodeHeight, fill=None, border='white')
        drawLabel(f'Opcode: {opcode}', opcodeX + (opcodeLen) // 2, opcodeY + (opcodeHeight // 2), size = opcodeLen // 20, fill='white')

    def drawInstruction(self, app):
        opcodeX = 0
        opcodeY = self.height // 20
        opcodeLen = self.width
        opcodeHeight = self.height // 20
        drawRect(opcodeX, opcodeY, opcodeLen, opcodeHeight, fill=None, border='white')
        drawLabel(f'Instruction: {app.cpu.instruction}, {app.cpu.command}', opcodeX + (opcodeLen) // 2, opcodeY + (opcodeHeight // 2), size = opcodeLen // 30, fill='white')

    def drawI(self, app):
        x = 0
        y = self.height // 10
        len = self.width // 6
        height = self.height // 20
        drawRect(x, y, len, height, fill=None, border='white')
        if 'I' in app.cpu.command:
            color = 'red'
        else:
            color = 'white'
        drawLabel(f'I: {app.cpu.I}', x + (len) // 2, y + (height // 2), size = len // 5, fill=color)

    def drawRegisters(self, app):
        xInit = 0
        yInit = 3 * (self.height // 20)
        len = self.width // 6
        height = self.height // 20
        drawRect(xInit, yInit, len, height, fill=None, border='white')
        drawLabel('Registers:', xInit + len // 2, yInit + height // 2, size = len // 7, fill='white')
        for i in range(16):
            y = yInit + (height * i) + height
            if f'v[{i}]' in app.cpu.command:
                color = 'red'
            else:
                color = 'white'
            if not i == 15:
                drawRect(xInit, y, len, height, fill=None, border='white')
                drawLabel(f'v[{i}] = {app.cpu.v[i]}', xInit + len // 2, y + height // 2, size = len // 7, fill=color)
            else:
                drawRect(xInit, y, len, height, fill=None, border='white')
                drawLabel(f'Flag: {app.cpu.v[i]}', xInit + len // 2, y + height // 2, size = len // 7, fill=color)    

    def drawPixels(self, app):
        if app.mode == 'game':
            xInit = 0
            yInit = 0
            width, height = self.width, self.height
        else:
            xInit = self.width // 6 + 20
            yInit = self.height // 10 + 20
            width, height = self.width - xInit, self.height - yInit
        pixelX = (width) // 64
        pixelY = (height) // 32
        for row in range(len(app.cpu.screen)):
            for pixel in range(len(app.cpu.screen[row])):
                if app.cpu.screen[row][pixel]:
                    drawRect(xInit + (pixel * pixelX), yInit + row * pixelY, pixelX, pixelY, align='center', fill='white')

    def drawModesHoverOvers(self, mouseX, mouseY):
        if self.height // 3 <= mouseY <= ((self.height // 3) + (self.height // 4)):
                if 0 < mouseX < self.width // 4:
                    Screen.hoverOverGame(self)
                elif self.width // 4 < mouseX < self.width // 2:
                    Screen.hoverOverCpu(self)
                else:
                    Screen.notHoveringOver(self)
        else:
            Screen.notHoveringOver(self)
    
    def drawFilesHoverOvers(self, app, mouseX, mouseY):
        if not app.showFiles:
            Screen.hoveringOverSelectFile(self, app, mouseX, mouseY)
        if app.showFiles:
            Screen.drawFileHoverOverColor(self, app, mouseX, mouseY)

    def hoverOverGame(self):
        self.gameColor = 'white'
        self.gameTextColor = 'black'
        self.cpuColor = 'black'
        self.cpuTextColor = 'white'

    def hoverOverCpu(self):
        self.gameColor = 'black'
        self.gameTextColor = 'white'
        self.cpuColor = 'white'
        self.cpuTextColor = 'black'

    def notHoveringOver(self):
        self.gameColor = 'black'
        self.gameTextColor = 'white'
        self.cpuColor = 'black'
        self.cpuTextColor = 'white'

    def hoveringOverSelectFile(self, app, mouseX, mouseY):
        if not app.fileSelected:
            if self.width // 2 + self.width // 12 < mouseX <  self.width // 2 + self.width // 12 + self.width // 3 and self.height // 5 < mouseY < self.height // 5 + self.height // 10:
                self.selectFileColor = 'white'
                self.fileTextColor = 'black'
            else:
                self.selectFileColor = 'black'
                self.fileTextColor = 'white'
        if app.showFiles:
            Screen.drawFileHoverOverColor(app, app, mouseX, mouseY)
    
    def drawFileHoverOverColor(self, app, mouseX, mouseY):
        numOfFiles = len(app.displayedFiles)
        cols = 8
        rows = (numOfFiles + cols - 1) // cols
        cellWidth = self.width / cols
        cellHeight = self.height / rows
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


def onAppStart(app):
    app.background='black'
    app.setMaxShapeCount(10000)
    app.initMode = True
    app.showFiles = False
    app.showCPU = False
    app.initScreen = True
    app.fileSelected = False
    app.modeSelected = False
    app.mouseHasMoved = False
    app.files = os.listdir('/Users')
    app.displayedFiles = copy.copy(app.files)
    app.currPath = '/Users'
    app.filesColor = ['white' for _ in range(len(app.displayedFiles))]
    app.lastTimerUpdate = time.time()
    app.lastInstructionTime = time.time()
    app.timerInterval = 1/60
    app.instructionInterval = 1/500
    app.selectedFile = ['/Users']
    app.query = ''
    app.cpu = Cpu()
    app.screen = Screen(app)

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

def fileSelected(app, mouseX, mouseY):
    if app.displayedFiles != []:
        numOfFiles = len(app.displayedFiles)
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
                        return app.displayedFiles[fileIndex]
    return None

def redrawAll(app):
    if app.initScreen and not app.showFiles:
        app.screen.drawInitScreen()
    elif app.showFiles:
        app.screen.drawFiles(app)
    else:
        if app.mode == 'CPU':
            app.screen.drawCPU(app)
        app.screen.drawPixels(app)

def onStep(app):
    if not app.initScreen:
        currentTime = time.time()
        if currentTime - app.lastTimerUpdate >= app.timerInterval:
            if app.cpu.dt > 0:
                app.cpu.dt -= 1
            if app.cpu.st > 0:
                app.cpu.st -= 1
            app.lastTimerUpdate = currentTime
        if currentTime - app.lastInstructionTime >= app.instructionInterval:
            opcode = app.cpu.memory[app.cpu.pc] << 8 | app.cpu.memory[app.cpu.pc + 1]
            app.cpu.read(opcode)
            app.lastInstructionTime = currentTime

def onKeyPress(app, key):
    if app.showFiles:
        if key == 'left':
            try:
                app.selectedFile.pop()
                app.currPath = '/'.join(app.selectedFile)
                app.files = os.listdir(findFolderDir(app.selectedFile[-1], app.currPath))
                app.displayedFiles = copy.copy(app.files)
                app.filesColor = ['white' for _ in range(len(app.displayedFiles))]
            except Exception as e:
                pass
        elif key == 'backspace' and app.query != '':
            app.query = app.query[:-1]
            for file in app.files:
                searchedFile = file.lower()
                if app.query in searchedFile:
                    app.displayedFiles.append(file)
                    app.filesColor.append('white')
        elif key.isalpha():
            key = key.lower()
            app.query += key
            app.displayedFiles = []
            app.filesColor = []
            for file in app.files:
                searchedFile = file.lower()
                if app.query in searchedFile:
                    app.displayedFiles.append(file)
                    app.filesColor.append('white')

    if not app.initScreen:
        if key in app.cpu.keyboard:
            keyIndex = app.cpu.keyboard[key]
            app.cpu.keyStates[keyIndex] = True

def onKeyRelease(app, key):
    if not app.initScreen:
        if key in app.cpu.keyboard:
            keyIndex = app.cpu.keyboard[key]
            app.cpu.keyStates[keyIndex] = False

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
            if app.selectedFile == []:
                app.selectedFile = ['/Users']
            app.selectedFile.append(fileSelected(app, mouseX, mouseY))
            if app.selectedFile[-1] == None:
                app.selectedFile.pop()
            app.currPath = '/'.join(app.selectedFile)
            if app.selectedFile[-1][-4:] == '.ch8':
                    filePath = '/'.join(app.selectedFile)
                    f = open(filePath, 'rb')
                    program = list(f.read())
                    app.cpu.write(program)
                    app.fileSelected = True
                    app.initScreen = False
                    app.showFiles = False
            elif app.selectedFile != []:
                app.files = os.listdir(findFolderDir(app.selectedFile[-1], app.currPath))
                app.displayedFiles = copy.copy(app.files)
                app.filesColor = ['white' for _ in range(len(app.displayedFiles))]

def onMouseMove(app, mouseX, mouseY):
    if app.initScreen:
        if not app.modeSelected:
            app.screen.drawModesHoverOvers(mouseX, mouseY)
        if not app.fileSelected:
            app.screen.drawFilesHoverOvers(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    if app.width // 2 + app.width // 20 <= mouseX <= app.width - app.width // 20 and app.screen.cy - 20 <= mouseY <= app.screen.cy + 20:
        app.screen.cx = mouseX
        app.mouseHasMoved = True
    app.stepsPerSecond = (3.125 * (app.screen.cx % (app.width // 2 + app.width // 20))) // 1 if app.screen.cx % (app.width // 2 + app.width // 20) != 0 else 1
    app.screen.stepsPerSecond = app.stepsPerSecond

runApp()