from assembly_mapping.utility_functions import format_assembly_string

def handle_return(functionName, ref):
    return_assembly = (
        endframe_pointer(functionName) +
        load_return_address(functionName, ref) +
        load_ARG() +
        increment_SP_from_ARG() +
        load_pointer("THAT", 1) +
        load_pointer("THIS", 2) +
        load_pointer("ARG", 3) +
        load_pointer("LCL", 4) +
        goto_return_address(functionName, ref)
    )
    formatted_assembly = "\n\t".join(return_assembly.splitlines())
    return formatted_assembly

@format_assembly_string
def endframe_pointer(functionName):
    assembly_string = '''\
        // return {functionName}
        // endFrame = LCL
        @LCL
        D=M
        @endFrame
        M=D        
        '''
    labels = {"functionName": functionName}
    return assembly_string, labels

@format_assembly_string
def load_return_address(functionName, ref):
    assembly_string = '''\
        // retAddr = *(endFrame - 5)
        @5
        D=A
        @endFrame
        A=M-D
        D=M
        @{functionName}$get_ret.{ref}
        M=D
        '''
    labels = {"functionName": functionName, "ref": ref}
    return assembly_string, labels

@format_assembly_string
def load_ARG():
    assembly_string = '''\
        // *ARG = pop()
        @SP
        M=M-1
        A=M
        D=M
        @ARG
        A=M
        M=D
        '''
    labels = dict()
    return assembly_string, labels

@format_assembly_string
def increment_SP_from_ARG():
    assembly_string = '''\
        // SP = ARG + 1
        @ARG
        D=M+1
        @SP
        M=D
        '''
    labels = dict()
    return assembly_string, labels

@format_assembly_string
def load_pointer(pointer, index):
    assembly_string = '''\
        // {pointer} = *(endFrame - {index})
        @{index}
        D=A
        @endFrame
        A=M-D
        D=M
        @{pointer}
        M=D
        '''
    labels = {"pointer": pointer, "index": index}
    return assembly_string, labels

@format_assembly_string
def goto_return_address(functionName, ref):
    assembly_string = '''\
        // goto {functionName}$ret.{ref}
        @{functionName}$get_ret.{ref}
        A=M
        0;JMP
        '''
    labels = {"functionName": functionName, "ref": ref}
    return assembly_string, labels