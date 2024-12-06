#citation: used LLM to help me find ways of implementing the new refresh rate logic
#citation: used Github Copilot to help me with comments

#focus on UI for file picker and starter interface and figure out the refresh rate logic (done)

from cmu_graphics import *
import os
import time
import threading
from cpu import Cpu
from gameScreen import GameScreen
from cpuScreen import CpuScreen
from filesScreen import FilesScreen
from initScreen import InitScreen

#refresh rate logic is ran in a different thread, so that the ch8 code is read at 500Hz while the screen is drawn at 60Hz
def gameLoop(app):
    while True:
        if not app.initScreen:
            if app.mode == 'CPU':
                opcode = app.cpu.memory[app.cpu.pc] << 8 | app.cpu.memory[app.cpu.pc + 1]
                app.cpu.executeOpcode(opcode)
                time.sleep(0.25)
            elif app.mode == 'game':
                opcode = app.cpu.memory[app.cpu.pc] << 8 | app.cpu.memory[app.cpu.pc + 1]
                app.cpu.executeOpcode(opcode)
                time.sleep(0.002)

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
    app.stepsPerSecond = 1
    gameThread = threading.Thread(target=gameLoop, args=(app,), daemon=True)
    gameThread.start()
    app.stepsPerSecond = 60

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

#(next three functions): finds all paths in the current selected directory using backtracking
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

#(next two functions): handle the CPU delay and sound timers, which was done with the help of LLM
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

#updates the query and handles key presses during games
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

#goes back in dir if the user presses the left key
def goBackInDir(app):
    try:
        app.currentDir.pop()
        app.currPath = '/'.join(app.currentDir)
        app.files = os.listdir(findFolderDir(app.currentDir[-1], app.currPath)) + ['..']
        createDisplayedFiles(app)
        app.filesColor = ['white' for _ in range(len(app.displayedFiles))]
        app.query = ''
    except:
        pass

#creates the displayed files list
def createDisplayedFiles(app):
    app.displayedFiles = []
    for file in app.files:
        if file[0] != '.':
            app.displayedFiles.append(file)

#deletes the query if the user presses backspace
def deleteQuery(app):
    app.query = app.query[:-1]
    for file in app.files:
        searchedFile = file.lower()
        if app.query in searchedFile:
            app.displayedFiles.append(file)
            app.filesColor.append('white')

#updates the query if the user presses a key
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

#handles key presses during games
def handleGameKeyPress(app, key):
    if key in app.cpu.keyboard:
        keyIndex = app.cpu.keyboard[key]
        app.cpu.keyStates[keyIndex] = True

#handles key releases during games
def onKeyRelease(app, key):
    if not app.initScreen and key in app.cpu.keyboard:
        keyIndex = app.cpu.keyboard[key]
        app.cpu.keyStates[keyIndex] = False

# next two functions handle mouse clicks during init screen
def clickOnMode(app, mouseX, mouseY):
    if not app.modeSelected and hasattr(app.screen, 'handleModeClicks'):
        app.screen.handleModeClicks(app, mouseX, mouseY)

def clickOnSelectFile(app, mouseX, mouseY):
    inMouseXRange = app.width // 2 + app.width // 12 < mouseX < app.width // 2 + app.width // 12 + app.width // 3
    inMouseYRange = app.height // 3 + app.height // 8 < mouseY < app.height // 3 + app.height // 4
    return not app.fileWasSelected and inMouseXRange and inMouseYRange

#calls the appropriate function when the user clicks on the screen
def onMousePress(app, mouseX, mouseY):
    if app.initScreen:
        clickOnMode(app, mouseX, mouseY)
        if clickOnSelectFile(app, mouseX, mouseY) and not app.showFiles:
            app.showFiles = True
        elif app.showFiles:
            handleClickOnFiles(app, mouseX, mouseY)
    handleScreenMode(app)

#handles the logic of clicking on files and updating the files shown
def handleClickOnFiles(app, mouseX, mouseY):
    try:
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
    except:
        pass

#reads the .ch8 file that the user selected
def readFile(app):
    filePath = '/'.join(app.currentDir)
    with open(filePath, 'rb') as f:
        program = list(f.read())
    app.cpu.writeProgramIntoMemory(program)
    app.fileWasSelected = True
    app.showFiles = False

#handles which screen class to make app.screen be based on current state
def handleScreenMode(app):
    if app.initScreen:
        if app.fileWasSelected and app.modeSelected:
            app.initScreen = False
            if app.mode == 'CPU':
                app.screen = CpuScreen(app)
            elif app.mode == 'game':
                app.screen = GameScreen(app)
        elif app.showFiles:
            app.screen = FilesScreen(app)
        elif app.fileWasSelected:
            app.screen = InitScreen(app)

#handles mouse movement during the init screen and file picker
def onMouseMove(app, mouseX, mouseY):
    if app.initScreen and hasattr(app.screen, 'drawModesHoverOvers'):
        if hasattr(app.screen, 'drawModesHoverOvers') and not app.modeSelected:
            app.screen.drawModesHoverOvers(mouseX, mouseY)
        if hasattr(app.screen, 'drawFileHoverOverColor'):
            app.screen.drawFileHoverOverColor(mouseX, mouseY)
    elif app.showFiles and hasattr(app.screen, 'drawFilesHoverOver'):
        app.screen.drawFilesHoverOver(app, mouseX, mouseY)

runApp()