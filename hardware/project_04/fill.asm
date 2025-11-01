// this program is fill implementation in the Hack assembly language
// fill program is about I/O, if a key on the keyboard is pressed, the screen becomes entirely black, when no key is pressed
// the screen is entirely white.


// pixelColor = 0 // white by default
@pixelColor
M=0

(LOOP)
// if keyboard output is zero, then pixelColor is white, else black
@KBD
D=M
@WHITE
D;JEQ
(BLACK)
@pixelColor
M=-1
// go to PAINT
@PAINT
0;JMP
(WHITE)
@pixelColor
M=0

(PAINT)
// numOfRegisters = 8192
@8192
D=A
@numOfRegisters
M=D

// i = 0
@i
M=0

// addr = base address of the screen map space
@SCREEN
D=A
@addr
M=D

(PAINT_LOOP)
// if i == numOfRegisters, go to LOOP
@i
D=M
@numOfRegisters
D=D-M
@LOOP
D;JEQ

// write pixelColor at the current register pointed to by addr
@pixelColor
D=M
@addr
A=M
M=D

// i = i + 1
@i
M=M+1
// addr = addr + 1
@addr
M=M+1

@PAINT_LOOP
0;JMP
