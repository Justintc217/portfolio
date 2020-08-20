// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// set R2 to zero
// begin loop
// decrement R0. if less then 0 end program otherwise continue
// add R1 to R2
// return to loop beginning


@2
M=0
@0 //beginning of loop
M=M-1
D=M
@14 //end program
D;JLT
@1
D=M
@2
M=D+M
@2
0;JMP=
