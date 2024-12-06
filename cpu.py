import random

class Cpu:
    def __init__(self):
        self.registers = [0 for i in range(16)]
        self.I = 0
        initalMemoryPosition = 512
        self.pc = initalMemoryPosition
        self.stack = []
        self.sPointer = 0
        self.keyboard = {'1': 1, '2': 2, '3': 3, '4': 0xC,  'q': 4, 'w': 5, 'e': 6, 'r': 0xD,  'a': 7, 's': 8, 'd': 9, 'f': 0xE,  'z': 0xA, 'x': 0, 'c': 0xB, 'v': 0xF}
        self.keyStates = [False] * 16
        self.screen = [[0 for _ in range(64)] for _ in range(32)]
        self.instruction = 0
        self.command = ''
        self.memory = [0 for _ in range(4096)]
        self.delayTimer = 0
        self.soundTimer = 0
    
    def changeKeyboard(self, key, newKey):
        print(key)
        print(newKey)
        if newKey not in self.keyboard:
            self.keyboard[newKey] = self.keyboard.pop(key)
            print(self.keyboard)
    
    def writeProgramIntoMemory(self, program):
        self.memory[512:] = program
    
    # executes the opcode sent to the function by masking the instruction and different possibilities of the opcode
    # opcode is in comment for each case, what the case does is in the command variable
    def executeOpcode(self, opcode):
        instruction = opcode >> 12
        x = (opcode >> 8) & 0x0F
        y = (opcode >> 4) & 0x0F
        n = opcode & 0x000F
        kk = opcode & 0x00FF
        nnn = opcode & 0x0FFF
        match instruction:
            case 0: 
                if opcode == 0x00E0:
                    # 0x0000
                    self.instruction = 0.0
                    self.command = 'clears screen'
                    self.screen = [[0 for _ in range(64)] for _ in range(32)]
                    self.pc += 2
                elif opcode == 0x00EE:
                    # 0x00EE 
                    self.instruction = 0.14
                    self.command = 'returns from subroutine'
                    self.pc = self.stack.pop()
                else:
                    self.pc += 2
            case 1:
                # 0x1nnn
                self.instruction = 1
                self.command = f'set PC to {nnn}'
                self.pc = nnn
            case 2:
                # 0x2nnn
                self.instruction = 2
                self.command = f'append PC to stack, set PC to {nnn}'
                self.stack.append(self.pc + 2)
                self.pc = nnn
            case 3:
                # 0x3xkk
                self.instruction = 3
                self.command = f'skips next instruction if v[{x}] == {kk}'
                if self.registers[x] == kk:
                    self.pc += 4
                else:
                    self.pc += 2
            case 4:
                # 0x4xkk
                self.instruction = 4
                self.command = f'skips next instruction if v[{x}] != {kk}'
                if self.registers[x] != kk:
                    self.pc += 4
                else:
                    self.pc += 2
            case 5:
                # 0x5xy0
                self.instruction = 5
                self.command = f'skips next instruction if v[{x}] == v[{y}]'
                if self.registers[x] == self.registers[y]:
                    self.pc += 4
                else:
                    self.pc += 2
            case 6:
                # 0x6xkk
                self.instruction = 6
                self.command = f'set v[{x}] = {kk}'
                self.registers[x] = kk
                self.pc += 2
            case 7:
                # 0x7xkk
                self.instruction = 7
                self.command = f'adds {kk} to v[{x}]'
                self.registers[x] += kk
                self.registers[x] = self.registers[x] % 256
                self.pc += 2
            case 8:
                match n:
                    case 0:
                        # 0x8xy0
                        self.instruction = 8.0
                        self.command = f'v[{x}] = v[{y}]'
                        self.registers[x] = self.registers[y]
                    case 1:
                        # 0x8xy1
                        self.instruction = 8.1
                        self.command = f'v[{x}] is ORed by v[{y}]'
                        self.registers[x] |= self.registers[y]
                    case 2:
                        # 0x8xy2
                        self.instruction = 8.2
                        self.command = f'v[{x}] is ANDed by v[{y}]'
                        self.registers[x] &= self.registers[y]     
                    case 3:
                        # 0x8xy3
                        self.instruction = 8.3
                        self.command = f'v[{x}] is XORed by v[{y}]'
                        self.registers[x] ^= self.registers[y]   
                    case 4:
                        # 0x8xy4
                        self.instruction = 8.4
                        self.command = f'v[{x}] += v[{y}]; Flag = carry'
                        result = self.registers[x] + self.registers[y]
                        self.registers[x] = result & 255
                        self.registers[15] = 1 if result > 255 else 0    
                    case 5:
                        # 0x8xy5
                        self.instruction = 8.5
                        self.command = f'v[{x}] -= v[{y}]; Flag = NOT borrow'
                        result = self.registers[x] - self.registers[y]
                        self.registers[x] = (self.registers[x] - self.registers[y]) & 255
                        self.registers[15] = 1 if result >= 0 else 0
                    case 6:
                        # 0x8xy6
                        self.instruction = 8.6
                        self.command = f'V[{x}] shifted right, Flag = LSB'
                        oldX = self.registers[x]
                        self.registers[x] //= 2
                        self.registers[15] = oldX & 1
                    case 7:
                        # 0x8xy7
                        self.instruction = 8.7
                        self.command = f'v[{x}] = v[{y}] - v[{x}]; Flag = NOT borrow'
                        oldX = self.registers[x]
                        self.registers[x] = (self.registers[y] - self.registers[x]) & 255
                        self.registers[15] = 1 if self.registers[y] >= oldX else 0
                    case 14:
                        # 0x8xyE
                        self.instruction = 8.14
                        self.command = f'VY shifted left, stored in VX, Flag = MSB'
                        oldX = self.registers[x]
                        self.registers[x] *= 2
                        self.registers[x] &= 255
                        self.registers[15] = oldX >> 7
                self.pc += 2
            case 9:
                # 0x9xy0
                self.instruction = 9
                self.command = f'skips next instruction if v[{x}] != v[{y}]'
                if self.registers[x] != self.registers[y]:
                    self.pc += 4
                else:
                    self.pc += 2
            case 10:
                # 0xAnnn
                self.instruction = 10
                self.command = f'sets I = {nnn}'
                self.I = nnn
                self.pc += 2
            case 11:
                # 0xBnnn
                self.instruction = 11
                self.command = f'sets PC to {nnn} + v[0]({self.registers[0]})'
                self.pc = nnn + self.registers[0]
            case 12:
                # 0xCxkk
                r = random.randint(0, 255)
                self.instruction = 12
                self.command = f'sets v[{x}] equal to {kk} & {r}'
                self.registers[x] = r & kk
                self.pc += 2
            case 13:
                # 0xDxyn
                self.instruction = 13
                self.command = f'Draws from memory location {self.I} at coordinate (v[{x}], v[{y}])'
                self.registers[15] = 0
                for height in range(n):
                    sprite = self.memory[self.I + height]
                    for bit in range(8):
                        screenX = (self.registers[x] + bit) % 64
                        screenY = (self.registers[y] + height) % 32
                        spritePixel = (sprite >> (7 - bit)) & 1
                        was0 = self.screen[screenY][screenX] == 0
                        self.screen[screenY][screenX] ^= spritePixel
                        if self.screen[screenY][screenX] == 0 and was0 == False:
                            self.registers[15] = 1
                self.pc += 2
            case 14:
                match kk:
                    case 158:
                        # 0xEx9E
                        self.instruction = 14.158
                        self.command = f'skips next instruction if key pressed = v[{x}] ({self.registers[x]})'
                        if self.keyStates[self.registers[x]]:
                            self.pc += 4
                        else:
                            self.pc += 2
                    case 161:
                        # 0xExA1
                        self.instruction = 14.161
                        self.command = f'skips next instruction if key not pressed = v[{x}] ({self.registers[x]})'
                        if not self.keyStates[self.registers[x]]:
                            self.pc += 4
                        else:
                            self.pc += 2
            case 15:
                match kk:
                    case 10:
                        # 0xFx0A
                        self.instruction = 15.10
                        self.command = f'wait for key press and store in v[{x}]'
                        pressedKeys = [i for i, pressed in enumerate(self.keyStates) if pressed]
                        if not pressedKeys:
                            return
                        else:
                            self.registers[x] = pressedKeys[0]
                            self.pc += 2
                    case 7:
                        # 0xFx07
                        self.instruction = 15.7
                        self.command = f'set v[{x}] = delay timer'
                        self.registers[x] = self.delayTimer
                        self.pc += 2
                    case 15:
                        # 0xFx0F
                        self.instruction = 15.15
                        self.command = f'set delay timer = v[{x}]'
                        self.delayTimer = self.registers[x]
                        self.pc += 2
                    case 18:
                        # 0xFx12
                        self.instruction = 15.18
                        self.command = f'set sound timer = v[{x}]'
                        self.soundTimer = self.registers[x]
                        self.pc += 2
                    case 21:
                        # 0xFx15
                        self.delayTimer = self.registers[x]
                        self.pc += 2
                    case 24:
                        # 0xFx18
                        self.soundTimer = self.registers[x]
                        self.pc += 2
                    case 30:
                        # 0xFx1E
                        self.instruction = 15.30
                        self.command = f'I += v[{x}]'
                        self.I = (self.I + self.registers[x]) & 0xFFF
                        self.pc += 2
                    case 51:
                        # 0xFx33
                        self.instruction = 15.51
                        self.command = f'I, I+1, I+2 = BCD of v{[x]}'
                        hundreds = self.registers[x] // 100 % 10
                        tens = self.registers[x] // 10 % 10
                        ones = self.registers[x] % 10
                        self.memory[self.I] = hundreds
                        self.memory[self.I + 1] = tens
                        self.memory[self.I + 2] = ones
                        self.pc += 2
                    case 41:
                        # 0xFx29
                        self.instruction = 15.41
                        self.command = f'I = v{[x]} sprite location'
                        self.I = self.registers[x] * 5
                        self.pc += 2
                    case 85:
                        # 0xFx55
                        self.instruction = 15.85
                        self.command = f'writes v[0], v[{x}] in memory I, I + {x}'
                        for i in range(x + 1):
                            self.memory[self.I + i] = self.registers[i] % 256
                        self.pc += 2
                    case 101:
                        # 0xFx65
                        self.instruction = 15.85
                        self.command = f'reads memory I, I + {x} in v[0], v[{x}]'
                        for i in range(x + 1):
                            self.registers[i] = self.memory[self.I + i]
                            self.registers[i] = self.registers[i] % 256
                        self.pc += 2
