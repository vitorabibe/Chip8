from cmu_graphics import *

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
        self.readMeColor = 'black'
        self.readMeTextColor = 'white'
        self.keyboardMapperColor = 'black'
        self.keyboardMapperTextColor = 'white'
        self.stepsPerSecond = 250
        self.mouseHasMoved = app.mouseHasMoved
        self.keyboard = ['1', '2', '3', '4', 'q', 'w', 'e', 'r', 'a', 's', 'd', 'f', 'z', 'x', 'c', 'v']
        self.keyPressed = None