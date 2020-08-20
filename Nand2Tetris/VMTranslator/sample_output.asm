//initialize
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
	
// push constant 10
        @10
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
// pop local 0
        @LCL
        D=M
        @0
        D=D+A
        @addr_local
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_local
        A=M
        M=D
// push constant 21
        @21
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
// push constant 22
        @22
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
// pop argument 2
        @ARG
        D=M
        @2
        D=D+A
        @addr_argument
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_argument
        A=M
        M=D
// pop argument 1
        @ARG
        D=M
        @1
        D=D+A
        @addr_argument
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_argument
        A=M
        M=D
// push constant 36
        @36
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
// pop this 6
        @THIS
        D=M
        @6
        D=D+A
        @addr_this
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_this
        A=M
        M=D
// push constant 42
        @42
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
// push constant 45
        @45
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
// pop that 5
        @THAT
        D=M
        @5
        D=D+A
        @addr_that
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_that
        A=M
        M=D
// pop that 2
        @THAT
        D=M
        @2
        D=D+A
        @addr_that
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_that
        A=M
        M=D
// push constant 510
        @510
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
// pop temp 6
        @5
        D=A
        @6
        D=D+A
        @addr_temp
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_temp
        A=M
        M=D
// push local 0
        @LCL
        D=M
        @0
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
// push that 5
        @THAT
        D=M
        @5
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
// add
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D+M
// push argument 1
        @ARG
        D=M
        @1
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
// sub
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=M-D
// push this 6
        @THIS
        D=M
        @6
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
// push this 6
        @THIS
        D=M
        @6
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
// add
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D+M
// sub
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=M-D
// push temp 6
        @5
        D=A
        @6
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
// add
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D+M