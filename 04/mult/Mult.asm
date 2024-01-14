// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// Assumes that R0 >= 0, R1 >= 0, and R0 * R1 < 32768.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// for(int i = R1, i>0, i--) {
//    R2 = R2 + R0
// }

// initialize sum
@R2
M = 0

// Calculate only if both R0, R1 are non-zero
@R0
D=M
@R1
D=M|D
@END
D;JEQ

// calculate multiplication
(CALC)
// End function if we've finished multiplication process
@R1
D=M
@END
D;JEQ

// Update counter of how many times to add
@R1
M = M - 1

// Add numbers
@R0
D = M
@R2
M = M + D
@CALC
0;JMP

(END)
@END
0;JMP