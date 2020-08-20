// sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

// eq0
@SP
A=M-1
D=M
@if
D;JLT
D=0
@finally
0;JMP
(if)
D=-1
(finally)
@SP
A=M-1
M=D