from screen import *

class InitScreen(Screen):
    def render(self, app):
        InitScreen.drawModes(self)
        InitScreen.drawSelectFile(self)
        InitScreen.drawStepsPerSecond(self, app)
    
    def drawModes(self):
        drawLabel('Select Mode', self.width // 4, self.height // 4, size=self.width//15, fill='white')
        drawRect(0, self.height // 3, self.width//4, self.height // 4, fill=self.gameColor, border='white')
        drawLabel('Play Chip8 Game', self.width//8, self.height // 3 + self.height // 8, fill=self.gameTextColor)
        drawRect(self.width//4, self.height // 3, self.width//4, self.height // 4, fill=self.cpuColor, border='white')
        drawLabel('CPU simulator', self.width // 4 + self.width // 8, self.height // 3 + self.height // 8, fill=self.cpuTextColor)

    def drawSelectFile(self):
        drawRect(self.width // 2 + self.width // 12, self.height // 5, self.width // 3, self.height // 10, fill=self.selectFileColor, border='white')
        drawLabel('Select File', 3 * self.width // 4, self.height // 4, size=self.width//15, fill=self.fileTextColor)

    def drawStepsPerSecond(self, app):
        r = self.width // 60
        n = str(app.stepsPerSecond) if self.mouseHasMoved else str(self.stepsPerSecond)
        drawLine(self.width // 2 + self.width // 20, self.height // 2, self.width - self.width // 20, self.height // 2, fill='white')
        drawCircle(self.cx, self.cy, r, fill='white')
        drawLabel(f'{n} steps per second', self.width // 2 + self.width // 4, self.height // 2 - self.height // 8, fill='white')

    def drawModesHoverOvers(self, mouseX, mouseY):
        if self.height // 3 <= mouseY <= ((self.height // 3) + (self.height // 4)):
                if 0 < mouseX < self.width // 4:
                    InitScreen.hoverOverGame(self)
                elif self.width // 4 < mouseX < self.width // 2:
                    InitScreen.hoverOverCpu(self)
                else:
                    InitScreen.notHoveringOver(self)
        else:
            InitScreen.notHoveringOver(self)
    
    def drawFileHoverOverColor(self, app, mouseX, mouseY):
        if not app.fileWasSelected:
            # TODO: Add comments / give names
            a = self.width // 2 + self.width // 12 < mouseX <  self.width // 2 + self.width // 12 + self.width // 3
            b = self.height // 5 < mouseY < self.height // 5 + self.height // 10
            if a and b:
                self.selectFileColor = 'white'
                self.fileTextColor = 'black'
            else:
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