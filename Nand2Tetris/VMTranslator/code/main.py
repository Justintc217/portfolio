import sys
from pathlib import Path
from VMTranslator import VMTranslator
from bootstrap import bootstrap

try:
    relative_path = Path(sys.argv[1])
except IndexError:
    relative_path = Path(input(
        "type file path from 07. eg \"07/MemoryAccess/BasicTest/BasicTest.vm\" :"
    ))

PROJECT_PATH = Path("D:/nand2tetris/projects")
PROGRAM_PATH = PROJECT_PATH / relative_path
if PROGRAM_PATH.is_file():
    ASM_PATH = PROGRAM_PATH.parent / (PROGRAM_PATH.stem + "_.asm")
else:
    ASM_PATH = PROGRAM_PATH / (PROGRAM_PATH.stem + ".asm")

if __name__ == "__main__":
    if PROGRAM_PATH.is_file():
        vm_files = list(PROGRAM_PATH)
    else:
        vm_files = PROGRAM_PATH.glob("*.vm")

    asm_contents = bootstrap
    for file in vm_files:
        print(type(file))
        translator_instance = VMTranslator(file)
        instructions = translator_instance.extract_instructions_only()
        asm_contents = asm_contents + "\n" + translator_instance.translator(instructions)

    translator_instance.write_contents(ASM_PATH, asm_contents)
