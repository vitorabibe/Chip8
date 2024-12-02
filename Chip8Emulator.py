from cmu_graphics import *
import os
import time
import threading
from cpu import Cpu
from gameScreen import GameScreen
from cpuScreen import CpuScreen
from filesScreen import FilesScreen
from initScreen import InitScreen
from readMeScreen import ReadMeScreen
from keyboardMapper import KeyboardMapper

def gameLoop(app):
    while True:
        if not app.initScreen:
            currentTime = time.time()
            if currentTime - app.lastInstructionTime >= app.instructionInterval:
                opcode = app.cpu.memory[app.cpu.pc] << 8 | app.cpu.memory[app.cpu.pc + 1]
                app.cpu.executeOpcode(opcode)
                app.lastInstructionTime = currentTime
            time.sleep(0.0001)

def onAppStart(app):
    app.background = 'black'
    app.setMaxShapeCount(10000)
    setStates(app)
    app.files = os.listdir('/Users') + ['..']
    createDisplayedFiles(app)
    app.currPath = '/Users'
    app.filesColor = ['white' for _ in range(len(app.displayedFiles))]
    app.keyColor = ['black' for _ in range(16)]
    app.lastTimerUpdate = time.time()
    app.lastInstructionTime = time.time()
    app.timerInterval = 1/60
    app.instructionInterval = 1/500
    app.currentDir = ['/Users']
    app.query = ''
    app.cpu = Cpu()
    app.screen = InitScreen(app)
    app.showReadMe = False
    app.showKeyboardMapper = False
    app.stepsPerSecond = 1
    gameThread = threading.Thread(target=gameLoop, args=(app,), daemon=True)
    gameThread.start()

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

def handleTimers(app, currentTime):
    if app.cpu.delayTimer > 0:
        app.cpu.delayTimer -= 1
    if app.cpu.soundTimer > 0:
        app.cpu.soundTimer -= 1
    app.lastTimerUpdate = currentTime

def onKeyPress(app, key):
    if app.showFiles:
        if key == 'left':
            goBackInDir(app)
        elif key == 'backspace' and app.query != '':
            deleteQuery(app)
        elif key.isalpha() or key == 'space':
            updateQuery(app, key)
    if app.showKeyboardMapper:
        app.screen.changedKey(app, key)
    if not app.initScreen:
        handleGameKeyPress(app, key)

def goBackInDir(app):
    try:
        app.currentDir.pop()
        app.currPath = '/'.join(app.currentDir)
        app.files = os.listdir(findFolderDir(app.currentDir[-1], app.currPath)) + ['..']
        createDisplayedFiles(app)
        app.filesColor = ['white' for _ in range(len(app.displayedFiles))]
    except:
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
    inMouseXRange = app.width // 2 + app.width // 12 < mouseX < app.width // 2 + app.width // 12 + app.width // 3
    inMouseYRange = app.height // 3 + app.height // 8 < mouseY < app.height // 3 + app.height // 4
    return not app.fileWasSelected and inMouseXRange and inMouseYRange

def clickOnReadMe(app, mouseX, mouseY):
    return (app.height // 2 + app.height // 4 <= mouseY <= app.height and 
            0 <= mouseX <= app.width // 2)

def clickOnKeyboardMapper(app, mouseX, mouseY):
    return (app.height // 2 + app.height // 4 <= mouseY <= app.height and 
            app.width // 2 <= mouseX <= app.width)

def onMousePress(app, mouseX, mouseY):
    if app.initScreen:
        clickOnMode(app, mouseX, mouseY)
        if clickOnReadMe(app, mouseX, mouseY):
            app.showReadMe = True
        elif clickOnSelectFile(app, mouseX, mouseY) and not app.showFiles:
            app.showFiles = True
        elif clickOnKeyboardMapper(app, mouseX, mouseY):
            app.showKeyboardMapper = True
        elif app.showFiles:
            handleClickOnFiles(app, mouseX, mouseY)
        elif app.showKeyboardMapper:
            app.screen.keyChanger(app, mouseX, mouseY)
    handleScreenMode(app)

def handleClickOnFiles(app, mouseX, mouseY):
    app.query = ''
    if not app.currentDir:
        app.currentDir = ['/Users']
    selectedFile = app.screen.fileSelected(app, mouseX, mouseY)
    if selectedFile is not None:
        app.currentDir.append(selectedFile)
        app.currPath = '/'.join(app.currentDir)
        if selectedFile.endswith('.ch8'):
            readFile(app)
        else:
            app.files = os.listdir(findFolderDir(app.currentDir[-1], app.currPath))
            createDisplayedFiles(app)
            app.filesColor = ['white' for _ in range(len(app.displayedFiles))]

def readFile(app):
    filePath = '/'.join(app.currentDir)
    with open(filePath, 'rb') as f:
        program = list(f.read())
    app.cpu.writeProgramIntoMemory(program)
    app.fileWasSelected = True
    app.showFiles = False

def handleScreenMode(app):
    if app.initScreen:
        if app.showFiles:
            app.screen = FilesScreen(app)
        elif app.showKeyboardMapper:
            app.screen = KeyboardMapper(app)
        elif app.showReadMe:
            app.screen = ReadMeScreen(app)
        elif app.fileWasSelected and not app.modeSelected:
            app.screen = InitScreen(app)
        elif app.fileWasSelected and app.modeSelected:
            app.initScreen = False
            if app.mode == 'CPU':
                app.screen = CpuScreen(app)
            elif app.mode == 'game':
                app.screen = GameScreen(app)

def onMouseMove(app, mouseX, mouseY):
    if app.initScreen and hasattr(app.screen, 'drawModesHoverOvers'):
        if not any([app.showReadMe, app.modeSelected, app.showFiles, app.showKeyboardMapper]):
            if hasattr(app.screen, 'drawFileHoverOverColor'):
                app.screen.drawFileHoverOverColor(app, mouseX, mouseY)
            if hasattr(app.screen, 'drawModesHoverOvers'):
                app.screen.drawModesHoverOvers(mouseX, mouseY)
            if hasattr(app.screen, 'drawReadMeHoverOverColor'):
                app.screen.drawReadMeHoverOverColor(mouseX, mouseY)
            if hasattr(app.screen, 'drawKeyboardMapperHoverOverColor'):
                app.screen.drawKeyboardMapperHoverOverColor(mouseX, mouseY)
        elif app.showFiles and hasattr(app.screen, 'drawFilesHoverOver'):
            app.screen.drawFilesHoverOver(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    if hasattr(app.screen, 'cy'):
        if (app.width // 2 + app.width // 20 <= mouseX <= app.width - app.width // 20 and 
            app.screen.cy - 20 <= mouseY <= app.screen.cy + 20):
            app.screen.cx = mouseX
            app.mouseHasMoved = True
            calculateStepsPerSecond(app)

def calculateStepsPerSecond(app):
    baseX = app.width // 2 + app.width // 20
    relativeX = app.screen.cx - baseX
    maxX = app.width - app.width // 20 - baseX
    app.stepsPerSecond = max(1, int((500 * relativeX) / maxX))
    if hasattr(app.screen, 'stepsPerSecond'):
        app.screen.stepsPerSecond = app.stepsPerSecond

runApp()