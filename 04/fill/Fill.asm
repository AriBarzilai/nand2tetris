// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.

//R0 - screen refresh offset
//R1 - screen action (-1 or 0)

// initializes values in case it is garbage left by another program
@KBD
M = 0

(LOOP)
@R0 // resets R0
M = 0

// if key is pressed, set data to -1; else set data to 0. Afterwards, run what is in Execute
@KBD
D=M
@WHITE
D;JEQ

(BLACK)
@SCREEN
D=A
@R0
A=M+D
M=-1
@R0
M = M + 1

D=M
@8192
D=D-A
@BLACK //continue drawing until entire screen is drawn
D;JNE
@LOOP // after screen is fully drawn, check again for keyboard update
0;JMP

(WHITE)
@SCREEN
D=A
@R0
A=M+D
M=0
@R0
M = M + 1

D=M
@8192
D=D-A
@WHITE //continue drawing until entire screen is drawn
D;JNE
@LOOP // after screen is fully drawn, check again for keyboard update
0;JMP