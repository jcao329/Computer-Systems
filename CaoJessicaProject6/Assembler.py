import re

# Define the Hack Computer instruction sets
COMP_TABLE = { '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100', 'A': '0110000',
    '!D': '0001101', '!A': '0110001', '-D': '0001111', '-A': '0110011', 'D+1': '0011111',
    'A+1': '0110111', 'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101', 'M': '1110000', '!M': '1110001',
    '-M': '1110011', 'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011',
    'M-D': '1000111', 'D&M': '1000000', 'D|M': '1010101'
}
DEST_TABLE = { '': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}

JUMP_TABLE = { '': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 
'JMP': '111'}

# Initialize symbol table with predefined symbols
SYMBOL_TABLE = { 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'SCREEN': 16384, 'KBD': 24576,
    **{f'R{i}': i for i in range(16)}}

def parse_assembly(filename):
    """
    Cleans the file to ignore comments and whitespace. Taken same logic  from Project 0, but does not write a new file. 
    Comments can begin with // or with /* and end with */. Unlike project0, this will not write a new file, it instead
    returns a list where each value is the cleaned line. 

    Input: filename: string 
    output: list[string]
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    instructions = []
    insidecomment = False

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if "/*" in line:
            insidecomment = True
            line = line.split('/*')[0].strip()
        
        if insidecomment:
            if "*/" in line:
                insidecomment = False
                line = line.split('*/')[-1].strip()
            else:
                continue
        if "//" in line:
            line = line.split('//')[0].strip()

        if line and not insidecomment:  # Ignore empty lines
            instructions.append(line)

    return instructions

def first_pass(instructions):
    """
    Initial read through of the cleaned file and will add labels to our dictionary of symbols with value of the line
    number in the file (address) of the label. It will return a new list without the labels. 

    input: instructions: list[strings] 
    output: list[strings]
    """
    line_number = 0
    for instruction in instructions:
        if instruction.startswith('(') and instruction.endswith(')'):
            label = instruction[1:-1]
            SYMBOL_TABLE[label] = line_number  # Map label to current line number
        else:
            line_number += 1 
    return [instr for instr in instructions if not (instr.startswith('(') and instr.endswith(')'))]

def translate_a_instruction(instruction):
    """
    Function to translate a instructions. Type a instructions will be of form "@value" where value is a number. 
    This function will convert this line into 15 bit binary number with a leading 0.

    input: instruction: string 
    output: string -> binary command in machine language
    """
    address = instruction[1:]
    if address.isdigit():
        address = int(address)
    else:
        # Allocate new address if symbol is not already in the symbol table
        if address not in SYMBOL_TABLE:
            SYMBOL_TABLE[address] = len(SYMBOL_TABLE)
        address = SYMBOL_TABLE[address]
    return f'0{address:015b}'  # A-instruction is 0 followed by 15-bit address

def translate_c_instruction(instruction):
    """
    Function to translate c instructions. Type c instructions will be of form "dest=comp;jump". We will use the symbol 
    table dictionary to convert. 

    input: instruction: string
    output: string -> binary command in machine language
    """
    if '=' in instruction:
        dest, rest = instruction.split('=')
    else:
        dest, rest = '', instruction

    if ';' in rest:
        comp, jump = rest.split(';')
    else:
        comp, jump = rest, ''

    return f'111{COMP_TABLE[comp]}{DEST_TABLE[dest]}{JUMP_TABLE[jump]}'

def assemble_to_hack(instructions, output_filename):
    """
    Second pass of the instructions after cleaning and parsing to convert each line into its binary instruction in 
    machine language. Writes each line to a file with name output_filename. 

    input: instructions: list[strings], output_filename: string
    output: None
    """
    # Second pass: Translate instructions to binary
    binary_instructions = []
    for instruction in instructions:
        if instruction.startswith('@'):
            binary_instructions.append(translate_a_instruction(instruction))
        else:
            binary_instructions.append(translate_c_instruction(instruction))

    # Write to .hack file
    with open(output_filename, 'w') as f:
        for binary_instruction in binary_instructions:
            f.write(binary_instruction + '\n')

# Main function to assemble .asm to .hack
def assemble(filename):
    """
    Assembles a file from asm to machine language. Writes the result to a .hack file. 

    input: filename: string
    output: None
    """
    instructions = parse_assembly(filename)
    instructions = first_pass(instructions)  # Resolve labels in the first pass
    output_filename = filename.replace('.asm', '.hack')
    assemble_to_hack(instructions, output_filename)
    print(f'Assembly complete. Output written to {output_filename}')

