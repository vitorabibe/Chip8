from screen import *

class FilesScreen(Screen):
    def drawFilesHoverOver(self, app, mouseX, mouseY):
        if app.displayedFiles != []:
            numOfFiles = len(app.displayedFiles)
            cols, rows, cellWidth, cellHeight = FilesScreen.getFileLayoutData(numOfFiles, app)
            for row in range(rows):
                for col in range(cols):
                    fileIndex, rLeft, rTop = FilesScreen.getBounds(row, col, cols, numOfFiles, cellWidth, cellHeight)
                    if (rLeft <= mouseX <= rLeft + cellWidth) and (rTop <= mouseY <= rTop + cellHeight):
                        app.filesColor[fileIndex] = 'black'
                    else:
                        app.filesColor[fileIndex] = 'white'

    def render(self, app):
        if app.displayedFiles != []:
            numOfFiles = len(app.displayedFiles)
            cols, rows, cellWidth, cellHeight = FilesScreen.getFileLayoutData(numOfFiles, app)
            for row in range(rows):
                for col in range(cols):
                    fileIndex, rLeft, rTop = FilesScreen.getBounds(row, col, cols, numOfFiles, cellWidth, cellHeight)
                    drawRect(rLeft, rTop, cellWidth, cellHeight, fill=app.filesColor[fileIndex], border='black', borderWidth=1)
                    drawLabel(app.displayedFiles[fileIndex], (rLeft + cellWidth // 2), (rTop + cellHeight // 2), fill='red', size=app.width//60)

    def fileSelected(self, app, mouseX, mouseY):
        if app.displayedFiles != []:
            numOfFiles = len(app.displayedFiles)
            cols, rows, cellWidth, cellHeight = FilesScreen.getFileLayoutData(numOfFiles, app)
            for row in range(rows):
                for col in range(cols):
                    fileIndex, rLeft, rTop = FilesScreen.getBounds(row, col, cols, numOfFiles, cellWidth, cellHeight)
                    if (rLeft <= mouseX <= rLeft + cellWidth) and (rTop <= mouseY <= rTop + cellHeight):
                        return app.displayedFiles[fileIndex]
        return None

    def getFileLayoutData(numOfFiles, app):
        maxFilesPerCol = 80
        rows = 80 if numOfFiles > 80 else numOfFiles
        cols = (numOfFiles // maxFilesPerCol) + 1
        cellWidth = app.width // cols
        cellHeight = app.height // rows
        return cols, rows, cellWidth, cellHeight

    def getBounds(row, col, cols, numOfFiles, cellWidth, cellHeight):
        fileIndex = row * cols + col
        if fileIndex < numOfFiles:
            rLeft = col * cellWidth
            rTop = row * cellHeight
        return fileIndex, rLeft, rTop