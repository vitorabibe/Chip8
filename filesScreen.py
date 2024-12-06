#citation: used the help from LLM for the vast majority of this code, with the growthFactor logic being implemented by me
#(previously the files just had a set width and height)

from screen import *

class FilesScreen(Screen):
    def __init__(self, app):
        self.gridSpacing = 20
        self.defaultTextSize = 12
        self.growthFactor = 5
        
    def getAdjustedTextSize(self, filename):
        # Base case: 12 characters or less gets default size
        if len(filename) <= 12:
            return self.defaultTextSize

        # Progressive scaling for longer names
        # The longer the name, the more aggressive the size reduction
        length = len(filename)
        if length <= 15:
            return self.defaultTextSize * (12 / length)
        elif length <= 20:
            return self.defaultTextSize * (11 / length)
        elif length <= 25:
            return self.defaultTextSize * (10 / length)
        else:
            return self.defaultTextSize * (9 / length)
        
    def render(self, app):
        drawRect(0, 0, app.width, 40, fill='white', border='black')
        pathText = '/'.join(app.currentDir)
        drawLabel(pathText, 10, 20, align='left', size=14, fill='black')
        self.growthFactor = 5 * ((len(app.displayedFiles) // 12) + 1)
        if app.displayedFiles:
            cols = app.width // (app.width / self.growthFactor + self.gridSpacing)
            for i, file in enumerate(app.displayedFiles):
                row = i // cols
                col = i % cols
                x = col * (app.width / self.growthFactor + self.gridSpacing) + self.gridSpacing
                y = row * (app.height / self.growthFactor  + self.gridSpacing) + 60
                self.drawFileIcon(x, y, app.width / self.growthFactor, app.filesColor[i], file)

    def drawFileIcon(self, x, y, size, colorState, filename):
        folderHeight = size * 0.8
        folderWidth = size
        fillColor = 'white' if colorState == 'black' else 'black'
        
        # Draw main folder body
        drawPolygon(x, y + folderHeight//4,
                   x + folderWidth, y + folderHeight//4,
                   x + folderWidth, y + folderHeight,
                   x, y + folderHeight,
                   fill=fillColor, border='white')
        
        # Draw folder tab
        drawPolygon(x, y,
                   x + folderWidth//2 - folderWidth//6, y,
                   x + folderWidth//2, y + folderHeight//4,
                   x, y + folderHeight//4,
                   fill=fillColor, border='white')
        
        # Draw filename with progressively adjusted size
        adjustedSize = self.getAdjustedTextSize(filename)
        drawLabel(filename, x + folderWidth//2,
                 y + folderHeight - folderHeight//4,
                 size=adjustedSize, fill='red')

    # File selection logic
    def fileSelected(self, app, mouseX, mouseY):
        if not app.displayedFiles:
            return None
        cols = app.width // (app.width / self.growthFactor + self.gridSpacing)
        for i, file in enumerate(app.displayedFiles):
            row = i // cols
            col = i % cols
            x = col * (app.width / self.growthFactor + self.gridSpacing) + self.gridSpacing
            y = row * (app.height / self.growthFactor + self.gridSpacing) + 60
            if (x <= mouseX <= x + app.width / self.growthFactor and 
                y <= mouseY <= y + app.height / self.growthFactor):
                return file
        return None

    # File hover over logic
    def drawFilesHoverOver(self, app, mouseX, mouseY):
        if not app.displayedFiles:
            return
        cols = app.width // (app.height / self.growthFactor + self.gridSpacing)
        for i, file in enumerate(app.displayedFiles):
            row = i // cols
            col = i % cols
            x = col * (app.width / self.growthFactor + self.gridSpacing) + self.gridSpacing
            y = row * (app.height / self.growthFactor + self.gridSpacing) + 60
            if (x <= mouseX <= x + app.width / self.growthFactor and 
                y <= mouseY <= y + app.height / self.growthFactor):
                app.filesColor[i] = 'black'
            else:
                app.filesColor[i] = 'white'