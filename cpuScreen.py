from screen import *
from gameScreen import *

class CpuScreen(Screen):
    def render(self, app):
        opcode = app.cpu.memory[app.cpu.pc] << 8 | app.cpu.memory[app.cpu.pc + 1]
        drawRect(0, 0, app.width, app.height, fill=None, border='white')
        CpuScreen.drawPC(self, app)
        CpuScreen.drawOpcode(self, opcode)
        CpuScreen.drawInstruction(self, app)
        CpuScreen.drawI(self, app)
        CpuScreen.drawRegisters(self, app)
        GameScreen.render(self, app)

    def drawPC(self, app):
        pcX = 0
        pcY = 0
        pcLen = app.width // 6
        pcHeight = app.height // 20
        drawRect(pcX, pcY, pcLen, pcHeight, fill=None, border='white')
        if 'PC' in app.cpu.command:
            color = 'red'
        else:
            color = 'white'
        drawLabel(f'PC: {app.cpu.pc}', pcX + (pcLen) // 2, pcY + (pcHeight // 2), size = pcLen // 5, fill=color)

    def drawOpcode(self, opcode):
        opcodeX = app.width // 6
        opcodeY = 0
        opcodeLen = app.width - app.width // 6
        opcodeHeight = app.height // 20
        opcode = f'{opcode:016b}'
        drawRect(opcodeX, opcodeY, opcodeLen, opcodeHeight, fill=None, border='white')
        drawLabel(f'Opcode: {opcode}', opcodeX + (opcodeLen) // 2, opcodeY + (opcodeHeight // 2), size = opcodeLen // 20, fill='white')

    def drawInstruction(self, app):
        instructionX = 0
        instructionY = app.height // 20
        instructionLen = app.width
        instructionHeight = app.height // 20
        drawRect(instructionX, instructionY, instructionLen, instructionHeight, fill=None, border='white')
        drawLabel(f'Instruction: {app.cpu.instruction}, {app.cpu.command}', instructionX + (instructionLen) // 2, instructionY + (instructionHeight // 2), size = instructionLen // 30, fill='white')

    def drawI(self, app):
        x = 0
        y = app.height // 10
        len = app.width // 6
        height = app.height // 20
        drawRect(x, y, len, height, fill=None, border='white')
        if 'I' in app.cpu.command:
            color = 'red'
        else:
            color = 'white'
        drawLabel(f'I: {app.cpu.I}', x + (len) // 2, y + (height // 2), size = len // 5, fill=color)

    def drawRegisters(self, app):
        xInit = 0
        yInit = 3 * (app.height // 20)
        len = app.width // 6
        height = app.height // 20
        drawRect(xInit, yInit, len, height, fill=None, border='white')
        drawLabel('Registers:', xInit + len // 2, yInit + height // 2, size = len // 7, fill='white')
        for i in range(16):
            y = yInit + (height * i) + height
            if f'v[{i}]' in app.cpu.command:
                color = 'red'
            else:
                color = 'white'
            if not i == 15:
                drawRect(xInit, y, len, height, fill=None, border='white')
                drawLabel(f'v[{i}] = {app.cpu.registers[i]}', xInit + len // 2, y + height // 2, size = len // 7, fill=color)
            else:
                drawRect(xInit, y, len, height, fill=None, border='white')
                drawLabel(f'Flag: {app.cpu.registers[i]}', xInit + len // 2, y + height // 2, size = len // 7, fill=color)    