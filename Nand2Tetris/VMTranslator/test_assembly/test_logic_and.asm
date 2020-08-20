//and
@SP
M=M-1 // SP --
A=M
D=M // *SP aka y  
@if0
D;JEQ
@SP
A=M-1 // A = (SP -1)
D=M
@if0
D;JEQ
@SP // neither x nor y are 0
A = M-1
M=1
@end
0;JMP
(if0)
@SP
A=M-1
M=0
(end)
0


