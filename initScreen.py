#citation: used LLM to help me improve the UI of the Init Screen, mostly by making the hexagons for the modes and their hover over effects
#citation continuation: nevertheless, still had to correct / change much of the logic for that part of the code to also work

from math import cos, sin, radians
from screen import *

class InitScreen(Screen):
    def __init__(self, app):
        self.gameColor = 'black'
        self.gameTextColor = 'white'
        self.cpuColor = 'black'
        self.cpuTextColor = 'white'
        self.selectFileColor = 'black'
        self.fileTextColor = 'white'
        self.readMeColor = 'black'
        self.readMeTextColor = 'white'
        self.keyboardMapperColor = 'black'
        self.keyboardMapperTextColor = 'white'

    def render(self, app):
        self.drawPixelArtTitle(app)
        self.drawModes(app)
        self.drawSelectFile(app)
    
    #draws the pixel art title of the game by using a state 2d list to draw each pixel individually where 1 is white, 0 is black
    def drawPixelArtTitle(self, app):
        pixelSize = app.width // 80
        x = app.width // 4
        startY = app.height // 12
        
        patterns = {
            'C': [[0,1,1,1],[1,1,0,0],[1,0,0,0],[1,1,0,0],[0,1,1,1]],
            'H': [[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1]],
            'I': [[1,1,1,1],[0,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1]],
            'P': [[1,1,1,1],[1,0,0,1],[1,1,1,1],[1,0,0,0],[1,0,0,0]],
            '1': [[0,1,1,0],[1,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1]],
            '2': [[1,1,1,1],[0,0,0,1],[0,1,1,1],[1,0,0,0],[1,1,1,1]]
        }
        
        for char in "CHIP 112":
            if char == ' ':
                x += pixelSize * 5
                continue
            
            pattern = patterns[char]
            for row in range(len(pattern)):
                for col in range(len(pattern[0])):
                    if pattern[row][col]:
                        drawRect(x + col * pixelSize,
                               startY + row * pixelSize,
                               pixelSize, pixelSize,
                               fill='white')
            x += pixelSize * 5

    #draws the two modes of the game, the game and the CPU simulator, each being a hexagon
    def drawModes(self, app):
        startY = app.height // 2.5
        modeWidth = app.width // 4
        spacing = modeWidth // 2 + modeWidth // 2.5
        radius = modeWidth // 2
        centerX = app.width // 4
        
        points1 = []
        centerY1 = startY
        for i in range(6):
            angle = i * 360/6
            x = centerX + radius * cos(radians(angle))
            y = centerY1 + radius * sin(radians(angle))
            points1.append((x, y))
        drawPolygon(*[coord for point in points1 for coord in point],
                    fill=self.gameColor, border='white')
        
        points2 = []
        centerY2 = startY + spacing
        for i in range(6):
            angle = i * 360/6
            x = centerX + radius * cos(radians(angle))
            y = centerY2 + radius * sin(radians(angle))
            points2.append((x, y))
        drawPolygon(*[coord for point in points2 for coord in point],
                    fill=self.cpuColor, border='white')
        
        drawLabel('Play Chip8 Game', centerX, centerY1,
                 fill=self.gameTextColor, size=app.width//45, bold=True)
        drawLabel('CPU simulator', centerX, centerY2,
                 fill=self.cpuTextColor, size=app.width//45, bold=True)

    #draws the select file button which is a folder icon
    def drawSelectFile(self, app):
        startY = app.height // 3 + app.height // 8
        folderX = app.width * 3 // 4 - app.width // 12
        folderWidth = app.width // 6
        folderHeight = app.height // 8
        
        drawPolygon(folderX, startY + folderHeight//4,
                    folderX + folderWidth, startY + folderHeight//4,
                    folderX + folderWidth, startY + folderHeight,
                    folderX, startY + folderHeight,
                    fill=self.selectFileColor, border='white')
        
        drawPolygon(folderX, startY,
                    folderX + folderWidth//2 - folderWidth//6, startY,
                    folderX + folderWidth//2, startY + folderHeight//4,
                    folderX, startY + folderHeight//4,
                    fill=self.selectFileColor, border='white')
        
        drawLabel('Select File', folderX + folderWidth//2,
                 startY + folderHeight//1.5, size=app.width//50,
                 fill=self.fileTextColor)

    # handles calculations to determine if the mouse is hovering over a mode
    def drawModesHoverOvers(self, mouseX, mouseY):
        startY = app.height // 2.5
        modeWidth = app.width // 4
        spacing = modeWidth // 2 + modeWidth // 2.5
        radius = modeWidth // 2
        centerX = app.width // 4
        
        centerY1 = startY
        if ((mouseX - centerX)**2 + (mouseY - centerY1)**2 <= radius**2):
            self.hoverOverGame()
            return
        
        centerY2 = startY + spacing
        if ((mouseX - centerX)**2 + (mouseY - centerY2)**2 <= radius**2):
            self.hoverOverCpu()
            return
        
        self.notHoveringOver()
    
    # handles calculations to determine if the mouse is hovering over the select file button
    def drawFileHoverOverColor(self, mouseX, mouseY):
        startY = app.height // 3 + app.height // 8
        folderX = app.width * 3 // 4 - app.width // 12
        folderWidth = app.width // 6
        folderHeight = app.height // 8

        inMouseXRange = folderX <= mouseX <= folderX + folderWidth
        inMouseYRange = startY <= mouseY <= startY + folderHeight

        if inMouseXRange and inMouseYRange:
            self.drawFileHoverOver()
        else:
            self.notHoveringOverFile()

    # the next five functions change the color of the text and the button when the mouse is hovering over
    def drawFileHoverOver(self):
        self.selectFileColor = 'white'
        self.fileTextColor = 'black'

    def notHoveringOverFile(self):
        self.selectFileColor = 'black'
        self.fileTextColor = 'white'

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

    # handles the logic for when the user clicks on a mode
    def handleModeClicks(self, app, mouseX, mouseY):
        startY = app.height // 2.5
        modeWidth = app.width // 4
        spacing = modeWidth // 2 + modeWidth // 2.5
        radius = modeWidth // 2
        centerX = app.width // 4
        
        centerY1 = startY
        if ((mouseX - centerX)**2 + (mouseY - centerY1)**2 <= radius**2):
            app.mode = 'game'
            app.modeSelected = True
            return
        
        centerY2 = startY + spacing
        if ((mouseX - centerX)**2 + (mouseY - centerY2)**2 <= radius**2):
            app.mode = 'CPU'
            app.modeSelected = True
            return