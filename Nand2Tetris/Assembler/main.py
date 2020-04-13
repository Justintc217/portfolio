import sys
from pathlib import Path
from Assembler import Assembler
from c_instruction_map import comp, dest, jump, symbols

try:
    relative_path = Path(sys.argv[1])
except IndexError:
    relative_path = Path(input("type file path from 06. eg \"add/Add.asm\" :"))

PROJECT_PATH = Path("D:/nand2tetris/projects/06")
PROGRAM_PATH = PROJECT_PATH / relative_path
HACK_PATH = PROGRAM_PATH.parent / (PROGRAM_PATH.stem + ".hack")

if __name__ == "__main__":
    with open(PROGRAM_PATH) as asm_file:
        assembler_instance = Assembler(comp, dest, jump, symbols, asm_file)
        assembly = assembler_instance.extract_assembly_from_file()

    assembler_instance.load_reference_to_symbols_table(assembly)

    assembly_without_references = assembler_instance.remove_references(assembly)

    hack_binary = assembler_instance.assemble(assembly_without_references)

    with open(HACK_PATH, "w") as hack_file:
        hack_file.writelines(hack_binary)