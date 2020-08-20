from assembly_mapping.utility_functions import format_assembly_string

def handle_call(functionName, nArgs, ref):
    call_assembly = (
        push_return_address(functionName, ref) +
        push_pointer("LCL") +
        push_pointer("ARG") +
        push_pointer("THIS") +
        push_pointer("THAT") +
        reset_ARG(nArgs) +
        set_LCL_to_SP() +
        goto_function(functionName, ref)
    )
    formatted_assembly = "\n\t".join(call_assembly.splitlines())
    return formatted_assembly

@format_assembly_string
def reset_ARG(nArgs):
    assembly_string = """\
            // reset base of ARG
            @{nArgs}
            D=A
            @5
            D=D+A
            @SP
            D=M-D
            @ARG
            M=D
            """
    labels = {"nArgs": nArgs}
    return assembly_string, labels

@format_assembly_string
def push_pointer(pointer):
    assembly_string = """\
        // push {pointer}
        @{pointer}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """
    labels = {"pointer": pointer}
    return assembly_string, labels

@format_assembly_string
def push_return_address(functionName, ref):
    assembly_string = '''\
        // call {functionName}
        @{functionName}$set_ret.{ref}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        '''
    labels = {"functionName": functionName, "ref": ref}
    return assembly_string, labels

@format_assembly_string
def set_LCL_to_SP():
    assembly_string = '''\
        // LCL=SP
        @SP
        D=M
        @LCL
        M=D
        '''
    labels = dict()
    return assembly_string, labels

@format_assembly_string
def goto_function(functionName, ref):
    assembly_string = '''\
        // goto {functionName}
        @{functionName}
        0;JMP
        ({functionName}$set_ret.{ref})
        '''
    labels = {"functionName": functionName, "ref": ref}
    return assembly_string, labels