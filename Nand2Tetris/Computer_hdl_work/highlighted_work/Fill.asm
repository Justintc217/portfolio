// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


    // initialize screen address variable
    @SCREEN //begin screen
    D=A
    @screen_index
    M=D //load screen address into R0

(LOOP)
    @KBD // keyboard :4
    D=M
    @WHITEN //jump to whiten
    D;JEQ

(BLACKEN)
    @screen_index
    A=M
    M=-1 //blacken :10
    @ENDSCREEN // jump to test if end of screen section
    0;JMP

(WHITEN)
    @screen_index // :13
    A=M
    M=0 //whiten
    
(ENDSCREEN)
    @24000 // :16 end of screen. Actually 24575
    D=A
    @screen_index
    D=M-D // R0 - end of screen address
    @screen_index //reset screen address to beginning
    D;JEQ //is R0 == end of screen

    //increment screen address
    @screen_index
    M=M+1
    @LOOP // jump to beginning of loop
    0;JMP