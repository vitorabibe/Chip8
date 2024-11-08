from screen import *

class GameScreen(Screen):
    def render(self, app):
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

