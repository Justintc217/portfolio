from functools import reduce

class Assembler():
    def __init__(self, comp, dest, jump, symbols, asm_file):
        self.comp = comp
        self.dest = dest
        self.jump = jump
        self.symbols = symbols
        self.asm_file = asm_file
    
    # prepare data
    def extract_assembly_from_file(self):
        def clean_line(line):
            return line.rstrip("\n").replace(" ", "").split("//")[0]
        cleaned_assembly = [clean_line(line) for line in self.asm_file.readlines()]
        filtered_assembly = list(filter(None, cleaned_assembly))
        return filtered_assembly
    
    def load_reference_to_symbols_table(self, assembly):
        # side effect
        index = 0
        for line in assembly:
            if line.startswith("("):
                ref = line.lstrip("(").rstrip(")")
                self.symbols[ref] = str(index)
            else:
                index += 1
    
    def remove_references(self, assembly):
        assembly_without_references = list(filter(
            lambda x: not x.startswith("("),
            assembly
            ))
        return assembly_without_references
    
    # assembly -> binary
    def assemble(self, assembly_without_references):
        binary_output = reduce(
            (lambda x, y: "%s%s" %(x,y)),
            map(
                self.decider,
                assembly_without_references
                )
            )
        return binary_output

    def decider(self, line):
        if line.startswith("@"):
            return self.A_handler(line) + "\n"
        return self.C_handler(line) + "\n"

    # A instruction handling
    def A_handler(self, line):
        address = line.lstrip("@")
        try:
            address = int(address)
        except ValueError:
            address = self.symbolic_address_to_address(address)
        binary = '{:016b}'.format(address)
        return binary
    
    def symbolic_address_to_address(self, symbolic_address):
        # A_handler helper function 
        try:
            address = int(self.symbols[symbolic_address])
        except KeyError:
            self.add_symbol_address(symbolic_address)
            address = int(self.symbols[symbolic_address])
        return address
    
    def load_symbol_address_to_symbols_table(self, symbolic_address):
        # side effect of the A_handler helper
        for open_address in range(16, 16384):
            if open_address not in self.symbols.values():
                self.symbols[symbolic_address] = str(open_address)
                break
    
    # C instruction handling
    def C_handler(self, line):
        comp_key, dest_key, jump_key = self.partition(line)
        binary = "111" + self.comp[comp_key] + self.dest[dest_key] + self.jump[jump_key]
        return binary    
    
    def partition(self, line):
        # C_handler helper function
        if "=" in line:
            dest_key, comp_and_jump = line.split("=")
        else:
            comp_and_jump = line
            dest_key = "null"
        if ";" in line:
            comp_key, jump_key = comp_and_jump.split(";")
        else:
            comp_key = comp_and_jump
            jump_key = "null"
        return comp_key, dest_key, jump_key
