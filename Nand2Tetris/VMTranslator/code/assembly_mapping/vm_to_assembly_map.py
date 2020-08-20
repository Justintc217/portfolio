from textwrap import dedent

vm_assembly_static_logic_dict = {
    "sub": dedent(
        '''// sub
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=M-D'''
    ),
    
    "add": dedent(
        '''// add
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D+M'''
    ),
    
    "neg": dedent(
        '''// neg      
        @SP
        A=M-1
        M=-M'''
    ),
    
    "and": dedent(
        '''// and
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D&M'''
    ),
    
    "or": dedent(
        '''// or
        @SP
        M=M-1
        A=M
        D=M
        A=A-1
        M=D|M'''
    ),
    
    "not": dedent(
        '''// not
        @SP
        A=M-1
        M=!M'''
    ),
    
}

vm_assembly_comparisons = dedent(
    "// {comment}\n        " +
    vm_assembly_static_logic_dict["sub"] + 
        '''
        // comparison by {comment}
        @SP
        A=M-1
        D=M
        @if_{ref}
        D;J{instruction}
        D=0
        @finally_{ref}
        0;JMP
        (if_{ref})
        D=-1
        (finally_{ref})
        @SP
        A=M-1
        M=D'''
)

vm_assembly_pushpop_dict = {
    "push segment_pointer": dedent(
        '''// push {segment_pointer_name} {value}
        @{symbolic_segment_pointer_name}
        D=M
        @{value}
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1'''    
    ),
        
    "pop segment_pointer": dedent(
        '''// pop {segment_pointer_name} {value}
        @{symbolic_segment_pointer_name}
        D=M
        @{value}
        D=D+A
        @addr_{segment_pointer_name}
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_{segment_pointer_name}
        A=M
        M=D'''    
    ),
    
    "push temp": dedent(
        '''// push temp {value}
        @5
        D=A
        @{value}
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1'''    
    ),
        
    "pop temp": dedent(
        '''// pop temp {value}
        @5
        D=A
        @{value}
        D=D+A
        @addr_temp
        M=D
        @SP 
        M=M-1
        A=M
        D=M
        @addr_temp
        A=M
        M=D'''    
    ),
        
    "push constant": dedent(
        '''// push constant {value}
        @{value}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1'''
    ),
    
    "pop constant": dedent(
        '''// push constant {value}
        @SP
        M=M-1'''
    ),
        
    "push pointer": dedent(
        '''// push pointer {value}
        @{value}
        D=A
        @THIS
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1'''
    ),
        
    "pop pointer": dedent(
        '''// pop pointer {value}
        @THIS
        D=A
        @{value}
        D=D+A
        @this_or_that
        M=D
        @SP
        M=M-1
        A=M
        D=M
        @this_or_that
        A=M
        M=D'''
    ),
    
    "push static": dedent(
        '''// push static {value}
        @{filename}.{value}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1'''
    ),
    
    "pop static": dedent(
        '''// pop static {value}
        @SP
        M=M-1
        A=M
        D=M 
        @{filename}.{value}
        M=D'''
    ),
}

segment_pointer_symbolic_address_dict = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}

program_control_dict = {
    "label": "({label})",
    
    "goto": dedent(
        '''// goto {label}
        @{label}
        0;JMP'''
    ),
    
    "if-goto": dedent(
        '''// if-goto {label}
        @SP
        M=M-1   
        A=M
        D=M
        @{label}
        D;JNE'''
    )
}
    