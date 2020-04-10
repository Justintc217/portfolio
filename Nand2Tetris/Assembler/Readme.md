design an assembler that can translate from hack assembly to hack executable binary

Part 1: design only for A and C instructions. Not for symbols
    
    Architecture
        there will be 3 functions
            Decider - removes whitespace and comments, determines if A or C instruction or neither
            A_handler - translates value into binary with prepended 0
            C_handler - Parses statement. places values in 3 data dictionary values to map keys to values
                Opcodes
                jump
                Dest
        the main.py will open the asm file and run through it line by line
        
        