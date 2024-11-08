from cmu_graphics import *
import os
import time
import copy
from cpu import Cpu
from gameScreen import GameScreen
from cpuScreen import CpuScreen
from filesScreen import FilesScreen
from initScreen import InitScreen

def onAppStart(app):
    app.background='black'
    app.setMaxShapeCount(10000)
    setStates(app)
    app.files = os.listdir('/Users') + ['..']
    createDisplayedFiles(app)
    app.currPath = '/Users'
    app.filesColor = ['white' for _ in range(len(app.displayedFiles))]
    setTimers(app)
    app.currentDir = ['/Users']
    app.query = ''
    app.cpu = Cpu()
    app.screen = InitScreen(app)

def setStates(app):
    app.initMode = True
    app.showFiles = False
    app.showCPU = False
    app.initScreen = True
    app.fileWasSelected = False
    app.modeSelected = False
    app.mouseHasMoved = False

def setTimers(app):
    app.lastTimerUpdate = time.time()
    app.lastInstructionTime = time.time()
    app.timerInterval = 1/60
    app.instructionInterval = 1/500

def findFolderDir(folder, path):
    if folder in path:
        return path
    else:
        return handleFolderDir(folder, path)

def handleFolderDir(folder, path):
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

def redrawAll(app):
    app.screen.render(app)

def onStep(app):
    if not app.initScreen:
        currentTime = time.time()
        if currentTime - app.lastTimerUpdate >= app.timerInterval:
            handleTimers(app, currentTime)
        if currentTime - app.lastInstructionTime >= app.instructionInterval:
            readOpcode(app, currentTime)

def handleTimers(app, currentTime):
    if app.cpu.dt > 0:
        app.cpu.dt -= 1
    if app.cpu.st > 0:
        app.cpu.st -= 1
    app.lastTimerUpdate = currentTime

def readOpcode(app, currentTime):
    opcode = app.cpu.memory[app.cpu.pc] << 8 | app.cpu.memory[app.cpu.pc + 1]
    app.cpu.executeOpcode(opcode)
    app.lastInstructionTime = currentTime

def onKeyPress(app, key):
    if app.showFiles:
        if key == 'left':
            goBackInDir(app)
        elif key == 'backspace' and app.query != '':
            deleteQuery(app)
        elif key.isalpha() or key == 'space':
            updateQuery(app, key)

    if not app.initScreen:
        handleGameKeyPress(app, key)

def goBackInDir(app):
    try:
        app.currentDir.pop()
        app.currPath = '/'.join(app.currentDir)
        app.files = os.listdir(findFolderDir(app.currentDir[-1], app.currPath)) + ['..']
        createDisplayedFiles(app)
        app.filesColor = ['white' for _ in range(len(app.displayedFiles))]
    except Exception as e:
        pass

def createDisplayedFiles(app):
    app.displayedFiles = []
    for file in app.files:
        if file[0] != '.':
            app.displayedFiles.append(file)

def deleteQuery(app):
    app.query = app.query[:-1]
    for file in app.files:
        searchedFile = file.lower()
        if app.query in searchedFile:
            app.displayedFiles.append(file)
            app.filesColor.append('white')

def updateQuery(app, key):
    key = key.lower()
    app.query += key if len(key) == 1 else ' '
    print(app.query)
    app.displayedFiles = []
    app.filesColor = []
    for file in app.files:
        searchedFile = file.lower()
        if app.query in searchedFile and file[0] != '.':
            app.displayedFiles.append(file)
            app.filesColor.append('white')

def handleGameKeyPress(app, key):
    if key in app.cpu.keyboard:
        keyIndex = app.cpu.keyboard[key]
        app.cpu.keyStates[keyIndex] = True

def onKeyRelease(app, key):
    if not app.initScreen and key in app.cpu.keyboard:
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
    inMouseXRange = app.width // 2 + app.width // 12 < mouseX <  app.width // 2 + app.width // 12 + app.width // 3
    inMouseYRange = app.height // 5 < mouseY < app.height // 5 + app.height // 10
    if not app.fileWasSelected and inMouseXRange and inMouseYRange:
        return True

def onMousePress(app, mouseX, mouseY):
    if app.initScreen:
        clickOnMode(app, mouseX, mouseY)
        if clickOnSelectFile(app, mouseX, mouseY) and not app.showFiles:
            app.showFiles = True
        elif app.showFiles:
            handleClickOnFiles(app, mouseX, mouseY)
    handleScreenMode(app)

def handleClickOnFiles(app, mouseX, mouseY):
    app.query = ''
    if app.currentDir == []:
        app.currentDir = ['/Users']
    app.currentDir.append(app.screen.fileSelected(app, mouseX, mouseY))
    if app.currentDir[-1] == None:
        app.currentDir.pop()
    app.currPath = '/'.join(app.currentDir)
    if app.currentDir[-1][-4:] == '.ch8':
        readFile(app)
    elif app.currentDir != []:
        app.files = os.listdir(findFolderDir(app.currentDir[-1], app.currPath))
        createDisplayedFiles(app)
        app.filesColor = ['white' for _ in range(len(app.displayedFiles))]

def readFile(app):
    filePath = '/'.join(app.currentDir)
    f = open(filePath, 'rb')
    program = list(f.read())
    app.cpu.writeProgramIntoMemory(program)
    app.fileWasSelected = True
    app.showFiles = False

def handleScreenMode(app):
    if app.initScreen: 
        if app.showFiles:
            app.screen = FilesScreen(app)
        elif app.fileWasSelected and not app.modeSelected:
                app.screen = InitScreen(app)
        elif app.fileWasSelected and app.modeSelected:
            app.initScreen = False
    if app.modeSelected and app.fileWasSelected:
        if app.mode == 'CPU':
            app.screen = CpuScreen(app)
        elif app.mode == 'game':
            app.screen = GameScreen(app)

def onMouseMove(app, mouseX, mouseY):
    if app.initScreen:
        if not app.modeSelected and not app.showFiles:
            app.screen.drawModesHoverOvers(mouseX, mouseY)
        if not app.showFiles:
            app.screen.drawFileHoverOverColor(app, mouseX, mouseY)
        elif app.showFiles:
            app.screen.drawFilesHoverOver(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    if app.width // 2 + app.width // 20 <= mouseX <= app.width - app.width // 20 and app.screen.cy - 20 <= mouseY <= app.screen.cy + 20:
        app.screen.cx = mouseX
        app.mouseHasMoved = True
    app.stepsPerSecond = int((3.125 * (app.screen.cx % (app.width // 2 + app.width // 20))) // 1) if int((3.125 * (app.screen.cx % (app.width // 2 + app.width // 20))) // 1) != 0 else 1
    app.screen.stepsPerSecond = app.stepsPerSecond

runApp()