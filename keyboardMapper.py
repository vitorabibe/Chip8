from screen import *
from cpu import Cpu

class KeyboardMapper(Screen):
    def render(self, app):
        KeyboardMapper.drawKeyRects(self)
        KeyboardMapper.drawKeyLabels(self)

    def drawKeyRects(self):
        for i in range(16):
            drawRect((i % 4) * self.width // 4, (i // 4) * self.height // 4, self.width // 4, self.height // 4, fill=app.keyColor[i], border='white')

    def drawKeyLabels(self):
        drawLabel('1', self.width // 8, self.height // 8, size=self.width//15, fill='red')
        drawLabel('2', self.width // 8 + self.width // 4, self.height // 8, size=self.width//15, fill='red')
        drawLabel('3', self.width // 8 + self.width // 2, self.height // 8, size=self.width//15, fill='red')
        drawLabel('4', self.width // 8 + 3 * self.width // 4, self.height // 8, size=self.width//15, fill='red')
        drawLabel('Q', self.width // 8, self.height // 4 + self.height // 8, size=self.width//15, fill='red')
        drawLabel('W', self.width // 8 + self.width // 4, self.height // 8 + self.height // 4, size=self.width//15, fill='red')
        drawLabel('E', self.width // 8 + self.width // 2, self.height // 8 + self.height // 4, size=self.width//15, fill='red')
        drawLabel('R', self.width // 8 + 3 * self.width // 4, self.height // 8 + self.height // 4, size=self.width//15, fill='red')
        drawLabel('A', self.width // 8, self.height // 8 + self.height // 2, size=self.width//15, fill='red')
        drawLabel('S', self.width // 8 + self.width // 4, self.height // 8 + self.height // 2, size=self.width//15, fill='red')
        drawLabel('D', self.width // 8 + self.width // 2, self.height // 8 + self.height // 2, size=self.width//15, fill='red')
        drawLabel('F', self.width // 8 + 3 * self.width // 4, self.height // 8 + self.height // 2, size=self.width//15, fill='red')
        drawLabel('Z', self.width // 8, self.height // 8 + 3 * self.height // 4, size=self.width//15, fill='red')
        drawLabel('X', self.width // 8 + self.width // 4, self.height // 8 + 3 * self.height // 4, size=self.width//15, fill='red')
        drawLabel('C', self.width // 8 + self.width // 2, self.height // 8 + 3 * self.height // 4, size=self.width//15, fill='red')
        drawLabel('V', self.width // 8 + 3 * self.width // 4, self.height // 8 + 3 * self.height // 4, size=self.width//15, fill='red')
    
    def drawKeysHoverOver(self, app, mouseX, mouseY):
        cols, rows, cellWidth, cellHeight = 4, 4, self.width // 4, self.height // 4
        for row in range(rows):
            for col in range(cols):
                keyIndex, rLeft, rTop = KeyboardMapper.getBounds(row, col, cols, cellWidth, cellHeight)
                if (rLeft <= mouseX <= rLeft + cellWidth) and (rTop <= mouseY <= rTop + cellHeight):
                    app.keyColor[keyIndex] = 'white'
                else:
                    app.keyColor[keyIndex] = 'black'

    def getBounds(row, col, cols, cellWidth, cellHeight):
        keyIndex = row * cols + col
        rLeft = col * cellWidth
        rTop = row * cellHeight
        return keyIndex, rLeft, rTop
    
    def keyChanger(self, app, mouseX, mouseY):
        selectedKey = KeyboardMapper.findSelectedKey(self, mouseX, mouseY)
        if selectedKey != None and self.keyPressed != None:
            Cpu.changeKeyboard(self, selectedKey, self.keyPressed)

    def findSelectedKey(self, mouseX, mouseY):
        cols, rows, cellWidth, cellHeight = 4, 4, self.width // 4, self.height // 4
        for row in range(rows):
            for col in range(cols):
                keyIndex, rLeft, rTop = KeyboardMapper.getBounds(row, col, cols, cellWidth, cellHeight)
                if (rLeft <= mouseX <= rLeft + cellWidth) and (rTop <= mouseY <= rTop + cellHeight):
                    return self.keyboard[keyIndex]
        return None
    
    def changedKey(self, app, key):
        self.keyPressed = key
        