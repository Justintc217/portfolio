from assembly_mapping.utility_functions import format_assembly_string

def handle_function(functionName, nVar):
    function_assembly = (
        label_function_start(functionName) +
        push_zero() * int(nVar)
    )
    formatted_assembly = "\n\t".join(function_assembly.splitlines())
    return formatted_assembly

@format_assembly_string
def push_zero():
    assembly_string ='''\
        // push 0
        @SP
        A=M
        M=0
        @SP
        M=M+1
        '''
    labels = dict()
    return assembly_string, labels

@format_assembly_string
def label_function_start(functionName):
    assembly_string = '''\
        // initialize {functionName}
        ({functionName})
        '''
    labels = {"functionName": functionName}
    return assembly_string, labels