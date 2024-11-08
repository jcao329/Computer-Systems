import sys

# Mapping VM segments to Hack assembly symbols
SEGMENTS = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
    'temp': 5,
    'pointer': 3,
}
COMMAND_TYPE = ["sub","add", "neg",  "eq", "gt", "lt", "and", "or", "not"]

# Helper to generate unique labels for conditional commands (eq, gt, lt)
label_counter = 0

def unique_label():
    global label_counter
    label = f"LABEL_{label_counter}"
    label_counter += 1
    return label

def translate_vm_to_asm(vm_filename, asm_filename):
    asm_instructions = []
    
    with open(vm_filename, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('//'):
            continue

        command = line.split()
        asm_instructions.extend(translate_command(command))

    with open(asm_filename, 'w') as file:
        file.write('\n'.join(asm_instructions) + '\n')

def translate_command(command):
    cmd_type = command[0]
    if cmd_type == 'push':
        return translate_push(command[1], command[2])
    elif cmd_type == 'pop':
        return translate_pop(command[1], command[2])
    elif cmd_type in COMMAND_TYPE:
        return translate_arithmetic(cmd_type)
    else:
        return []

def translate_push(segment, index):
    instructions = []
    index = int(index)

    if segment == 'constant':
        instructions = [
            f"@{index}",
            "D=A",
            "@SP",
            "AM=M+1",
            "A=A-1",
            "M=D"
        ]
    elif segment in SEGMENTS:
        base_address = SEGMENTS[segment]
        if segment == 'temp' or segment == 'pointer':
            # temp and pointer are directly addressable
            instructions = [
                f"@{index}",
                "D=M",
                "@SP",
                "AM=M+1",
                "A=A-1",
                "M=D",
            ]
        else:
            # local, argument, this, that are base pointers
            instructions = [
                f"@{base_address}",
                "D=M",
                f"@{index}",
                "A=D+A",
                "D=M",
                "@SP",
                "AM=M+1",
                "A=A-1",
                "M=D"
            ]
    return instructions

def translate_pop(segment, index):
    instructions = []
    index = int(index)

    if segment in SEGMENTS:
        base_address = SEGMENTS[segment]
        if segment == 'temp' or segment == 'pointer':
            target = base_address + index
            # temp and pointer are directly addressable
            instructions = [
                "@SP",
                "AM=M-1",
                "D=M",
                f"@{target}",
                "M=D"
            ]
        else:
            # local, argument, this, that are base pointers
            instructions = [
                f"@{base_address}",
                "D=M",
                f"@{index}",
                "D=D+A",
                "@R13",
                "M=D",      
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D"
            ]
    return instructions

def translate_arithmetic(command):
    instructions = []
    if command == 'add':
        instructions = [
            "@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M"
        ]
    elif command == 'sub':
        instructions = [
            "@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D"
        ]
    elif command == 'neg':
        instructions = [
            "@SP", "A=M-1", "M=-M"
        ]
    elif command == 'eq':
        label = unique_label()
        instructions = [
            "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1",
            f"@{label}", "D;JEQ", "@SP", "A=M-1", "M=0",
            f"({label})"
        ]
    elif command == 'gt':
        label = unique_label()
        instructions = [
            "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D","M=-1",
            f"@{label}", "D;JGT", "@SP", "A=M-1", "M=0",
            f"({label})"
        ]
    elif command == 'lt':
        label = unique_label()
        instructions = [
            "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1",
            f"@{label}", "D;JLT", "@SP", "A=M-1", "M=0",
            f"({label})"
        ]
    elif command == 'and':
        instructions = [
            "@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M"
        ]
    elif command == 'or':
        instructions = [
            "@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M"
        ]
    elif command == 'not':
        instructions = [
            "@SP", "A=M-1", "M=!M"
        ]
    return instructions

if __name__ == "__main__":
    vm_filename = sys.argv[1]  
    asm_filename = vm_filename.replace('.vm', '.asm') 
    translate_vm_to_asm(vm_filename, asm_filename)
    print(f"Translation complete. Output written to {asm_filename}")
