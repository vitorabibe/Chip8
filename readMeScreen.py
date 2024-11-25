from screen import *

class ReadMeScreen(Screen):
    def render(self, app):
        readMe = '''This is a Chip8 emulator that can run Chip8 games and simulate a CPU.
            To run a Chip8 game with faster rendering, select "Play Chip8 Game"
            To simulate a CPU, select "CPU simulator".
            To run a Chip8 game, use the following keys:
            1 2 3 4,
            Q W E R,
            A S D F,
            Z X C V,
            After selecting your gamemode, click on "Select File" to choose a file to run.
            To select a file, click on the file name.
            To search for a file, just type out its name on the file picker. To delete a character, press backspace .'''
        drawLabel(readMe, 200, 200, size = 20, fill='white')
