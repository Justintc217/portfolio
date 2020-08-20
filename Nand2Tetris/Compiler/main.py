import sys
from pathlib import Path
from tokenizer import *
from jack_to_xml_parser import *

try:
    PROJECT_PATH = Path(sys.argv[1])
except IndexError:
    PROJECT_PATH = Path(input("type file path: "))

filename = PROJECT_PATH.parent / (PROJECT_PATH.stem + "_new.xml")

if __name__ == "__main__":
    with open(PROJECT_PATH) as jack_file:
        content = jack_file.read()
        instructions = extract_instructions_only(content)
        token_sample = tokenizer(instructions)

    compile_to_xml(token_sample, filename)
