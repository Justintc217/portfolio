import sys
from pathlib import Path
from assembler import assembler

try:
    relative_path = Path(sys.argv[1])
except IndexError:
    relative_path = Path(input("type file path from 06. eg \"add/Add.asm\" :"))

PROJECT_PATH = Path("D:/nand2tetris/projects/06")
PROGRAM_PATH = PROJECT_PATH / relative_path
HACK_PATH = PROGRAM_PATH.parent / (PROGRAM_PATH.stem + ".hack")

if __name__ == "__main__":
    with open(PROGRAM_PATH) as asm_file:
        hack_assembly = [
            line.rstrip("\n").replace(" ", "").split("//")[0] for line in asm_file.readlines()
        ]

    hack_binary = assembler(hack_assembly)

    with open(HACK_PATH, "w") as hack_file:
        hack_file.writelines(hack_binary)
        hack_file.close()
