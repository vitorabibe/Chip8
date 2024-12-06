Chip112 is a Chip8 compiler with many added features. Chip8 is an old computer that ran 8-bit games such as pong,
space invaders, etc. By being a compiler, Chip112 has no code written in it to run a specific
program or game. Differently, it reads the Chip8 game’s hex code and outputs whatever the
code tells it to output.

To start a game, select the mode you want to run (either CPU Simulator, which displays the CPU's registers, instructions and opcode and runs at 4Hz, or Play Game, which runs just the game at 500Hz). The modes are in the two hexagons and are labeled accordingly. After selecting a mode, select the file you want to run by clicking in "Select File", thus opening the file picker. The file picker starts in your /Users folder. You can use your keys to search for a file with a hidden query, you can use the backspace key to delete the last letter off the query, and the left arrow key to go back to the previous directory.

If you select CPU Simulator, it is recommended to just run the Chip8 Tests, since it will be hard to play the game at 4Hz. 

There are only a few games included, but you can easily search online for other .ch8 files and run them using the compiler. It is recommended to search for README files of these .ch8 files to know which keys control what. 

The Chip8 keyboard is a 4x4 keyboard consisting of the following matrix of keys:

1 2 3 4
Q W E R
A S D F
Z X C V

Here are the keys that control the games included:

Pong (1 and 2 player versions):
1 and Q control left paddle (upwards and downards respectively), 4 and R control right paddle (upwards and downards respectively)

Space Invaders:
Q moves left, E moves left, W shoots and starts the game once the Space Invaders Init Screen is being displayed