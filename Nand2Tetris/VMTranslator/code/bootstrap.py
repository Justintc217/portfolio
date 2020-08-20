bootstrap = '''//initialize
    @256
    D=A
    @SP
    M=D
// call Sys.init
	@Sys.init$set_ret.0
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
	// push LCL
	@LCL
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	// push ARG
	@ARG
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	// push THIS
	@THIS
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	// push THAT
	@THAT
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
	// reset base of ARG
	@0
	D=A
	@5
	D=D+A
	@SP
	D=M-D
	@ARG
	M=D
	// LCL=SP
	@SP
	D=M
	@LCL
	M=D
	// goto Sys.init
	@Sys.init
	0;JMP
	(Sys.init$set_ret.0)
	'''
