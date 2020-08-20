// eq0
@SP
A=M-1
D=M
@if
D;JEQ
D=0
@finally
0;JMP
(if)
D=1
(finally)
@SP
A=M-1
M=D