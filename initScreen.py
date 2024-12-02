from screen import *
from math import cos, sin, radians

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
        self.width = app.width
        self.height = app.height

    def render(self, app):
        self.drawPixelArtTitle()
        self.drawModes()
        self.drawSelectFile()
        self.drawReadMeScreen()
        self.drawKeyboardMapper()
    
    def drawPixelArtTitle(self):
        pixelSize = self.width // 80
        startX = self.width // 4
        startY = self.height // 12
        
        patterns = {
            'C': [[0,1,1,1],[1,1,0,0],[1,0,0,0],[1,1,0,0],[0,1,1,1]],
            'H': [[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1]],
            'I': [[1,1,1,1],[0,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1]],
            'P': [[1,1,1,1],[1,0,0,1],[1,1,1,1],[1,0,0,0],[1,0,0,0]],
            '1': [[0,1,1,0],[1,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1]],
            '2': [[1,1,1,1],[0,0,0,1],[0,1,1,1],[1,0,0,0],[1,1,1,1]]
        }
        
        x = startX
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

    def drawModes(self):
        startY = self.height // 3
        modeWidth = self.width // 4
        spacing = modeWidth // 2 + modeWidth // 3
        radius = modeWidth // 2
        centerX = self.width // 4
        
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
                 fill=self.gameTextColor, size=self.width//45, bold=True)
        drawLabel('CPU simulator', centerX, centerY2,
                 fill=self.cpuTextColor, size=self.width//45, bold=True)

    def drawSelectFile(self):
        startY = self.height // 4 + self.height // 8
        folderX = self.width * 3 // 4 - self.width // 12
        folderWidth = self.width // 6
        folderHeight = self.height // 8
        
        drawPolygon(folderX, startY + folderHeight//4,
                    folderX + folderWidth, startY + folderHeight//4,
                    folderX + folderWidth, startY + folderHeight,
                    folderX, startY + folderHeight,
                    fill=self.selectFileColor, border='white')
        
        drawPolygon(folderX + folderWidth//6, startY,
                    folderX + folderWidth//2, startY,
                    folderX + folderWidth//2, startY + folderHeight//4,
                    folderX + folderWidth//6, startY + folderHeight//4,
                    fill=self.selectFileColor, border='white')
        
        drawLabel('Select File', folderX + folderWidth//2,
                 startY + folderHeight//1.5, size=self.width//50,
                 fill=self.fileTextColor)

    def drawModesHoverOvers(self, mouseX, mouseY):
        startY = self.height // 3
        modeWidth = self.width // 4
        spacing = modeWidth // 2 + modeWidth // 3
        radius = modeWidth // 2
        centerX = self.width // 4
        
        centerY1 = startY
        if ((mouseX - centerX)**2 + (mouseY - centerY1)**2 <= radius**2):
            self.hoverOverGame()
            return
        
        centerY2 = startY + spacing
        if ((mouseX - centerX)**2 + (mouseY - centerY2)**2 <= radius**2):
            self.hoverOverCpu()
            return
        
        self.notHoveringOver()

    def drawKeyboardMapper(self):
        drawRect(self.width // 2,
                self.height // 2 + self.height // 4,
                self.width // 2, self.height // 4,
                fill=self.keyboardMapperColor,
                border='white')
        drawLabel('Keyboard Mapper',
                 self.width // 2 + self.width // 4,
                 self.height - self.height // 8,
                 size=self.width // 17,
                 fill=self.keyboardMapperTextColor)

    def drawReadMeScreen(self):
        drawRect(0, self.height // 2 + self.height // 4,
                self.width // 2, self.height // 4,
                fill=self.readMeColor, border='white')
        drawLabel('Read Me', self.width // 4,
                 self.height - self.height // 8,
                 size=self.width // 17,
                 fill=self.readMeTextColor)

    def drawKeyboardMapperHoverOverColor(self, mouseX, mouseY):
        if self.height // 2 + self.height // 4 <= mouseY <= self.height:
            if self.width // 2 <= mouseX <= self.width:
                self.keyboardMapperColor = 'white'
                self.keyboardMapperTextColor = 'black'
            else:
                self.keyboardMapperColor = 'black'
                self.keyboardMapperTextColor = 'white'
        else:
            self.keyboardMapperColor = 'black'
            self.keyboardMapperTextColor = 'white'

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