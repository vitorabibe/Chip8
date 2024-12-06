from screen import *

class GameScreen(Screen):
    # renders the game screen only if the pixel is a 1 to maximize efficiency.
    def render(self, app):
        if app.mode == 'game':
            xInit = 0
            yInit = 0
            width, height = app.width, app.height
        else:
            xInit = app.width // 6 + 20
            yInit = app.height // 10 + 20
            width, height = app.width - xInit, app.height - yInit
        pixelX = (width) // 64
        pixelY = (height) // 32
        for row in range(len(app.cpu.screen)):
            for pixel in range(len(app.cpu.screen[row])):
                if app.cpu.screen[row][pixel]:
                    drawRect(xInit + (pixel * pixelX), yInit + row * pixelY, pixelX, pixelY, align='center', fill='white')

