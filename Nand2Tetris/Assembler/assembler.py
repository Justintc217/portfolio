from functools import reduce
from c_instruction_map import comp, dest, jump, symbols

def assembler(hack_assembly): # returns map
    assembly_with_ref = list(filter(None, hack_assembly))
    reference_finder(assembly_with_ref)
    assembly = filter(
        lambda x: not x.startswith("("),
        assembly_with_ref
        )
    return reduce(
        (lambda x, y: x + y),
        map(
            decider,
            assembly
            )
    )

def reference_finder(assembly_with_ref):
    index = 0
    for line in assembly_with_ref:
        if line.startswith("("):
            ref = line.lstrip("(").rstrip(")")
            symbols[ref] = index
        else:
            index += 1

def decider(line):
    if line.startswith("@"):
        return A_handler(line) + "\n"
    return C_handler(line) + "\n"

# A handling
def symbol_to_value(symbolic_address):
    try:
        symbolic_address = symbols[symbolic_address]
    except KeyError:
        for open_address in range(16, 16384):
            if open_address not in symbols.values():
                symbols[symbolic_address] = open_address
                symbolic_address = open_address
                break
    return symbolic_address

def A_handler(line):
    address = line.lstrip("@")
    try:
        address = int(address)
    except ValueError:
        address = int(symbol_to_value(address))
    binary = '{:016b}'.format(address)
    return binary

# C handling
def partition(line):
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

def C_handler(line):
    comp_key, dest_key, jump_key = partition(line)
    binary = "111" + comp[comp_key] + dest[dest_key] + jump[jump_key]
    return binary
