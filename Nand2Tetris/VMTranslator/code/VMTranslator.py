from functools import reduce
from itertools import chain
from assembly_mapping.vm_to_assembly_map import (
    vm_assembly_static_logic_dict,
    vm_assembly_comparisons,
    vm_assembly_pushpop_dict,
    segment_pointer_symbolic_address_dict,
    program_control_dict
)

from assembly_mapping.call_assembly import handle_call
from assembly_mapping.function_assembly import handle_function
from assembly_mapping.return_assembly import handle_return


class VMTranslator():
    def __init__(self, file_path):
        self.vm_file_contents = self.get_contents_from_file(file_path)
        self.filename = "{parent}.{child}".format(parent=file_path.parent.stem, child=file_path.stem)
        self.ref = self.reference_code_generator()
        self.functionNames = list()
        self.functionRefs = list()

    @staticmethod
    def get_contents_from_file(file_path):
        with open(file_path) as vm_file:
            vm_file_contents = vm_file.readlines()
        return vm_file_contents

    @staticmethod
    def write_contents(file_path, contents):
        with open(file_path, "w") as asm_file:
            asm_file.writelines(contents)

    @staticmethod
    def reference_code_generator():
        i = 0
        while True:
            yield i
            i += 1

    def extract_instructions_only(self):
        def clean_line(line):
            line = line.rstrip("\n")
            code, *_ = line.split("//")
            code = code.strip()
            return code
        clean_code = map(clean_line, self.vm_file_contents)
        instructions = list(filter(None, clean_code))
        return instructions

    def translator(self, instructions):
        asm_contents = reduce(
            (lambda x, y: "%s\n%s" % (x, y)),
            map(self.parser, instructions)
        )
        return asm_contents

    def parser(self, instruction_line):
        command, *attributes = instruction_line.split(" ")
        if not attributes and command != "return":
            # arithmetic path
            return self.arithmetic_handler(command)
        elif command in program_control_dict.keys():
            # program control path
            return self.program_control_handler(command, *attributes)
        elif command == "call":
            functionName, nArgs = attributes
            self.functionRefs.append(next(self.ref))
            return handle_call(functionName, nArgs, ref=self.functionRefs[-1])
        elif command == "function":
            functionName, nVar = attributes
            self.functionNames.append(functionName)
            return handle_function(functionName, nVar)
        elif command == "return":
            functionName = self.functionNames[-1]
            if not self.functionRefs:
                ref = next(self.ref)
            else:
                ref = self.functionRefs.pop()
            return handle_return(functionName, ref=ref)
        else:
            # push pop path
            return self.pushpop_handler(command, *attributes)

    def arithmetic_handler(self, command):
        if command in vm_assembly_static_logic_dict.keys():
            return vm_assembly_static_logic_dict[command]
        return vm_assembly_comparisons.format(
            ref=next(self.ref),
            instruction=command.upper(),
            comment=command
        )

    def program_control_handler(self, command, label):
        _, filename = self.filename.split(".")
        label = "{filename}${label}".format(filename = filename, label = label)
        return program_control_dict[command].format(label=label)

    def pushpop_handler(self, command, segment, value):
        if segment in segment_pointer_symbolic_address_dict.keys():
            assembly = vm_assembly_pushpop_dict["%s segment_pointer" % command]
            symbolic_segment_pointer_name = (
                segment_pointer_symbolic_address_dict[segment]
            )
        else:
            assembly = vm_assembly_pushpop_dict["%s %s" % (command, segment)]
            symbolic_segment_pointer_name = ""
        return assembly.format(
            ref=next(self.ref),
            filename=self.filename,
            value=value,
            segment_pointer_name=segment,
            symbolic_segment_pointer_name=symbolic_segment_pointer_name
        )
