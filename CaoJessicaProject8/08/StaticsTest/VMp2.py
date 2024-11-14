import sys
import os

COMMAND_TYPE = ["sub","add", "neg",  "eq", "gt", "lt", "and", "or", "not", "label", "goto", "if-goto", "function", 
                "call", "return"]

# Helper to generate unique labels for conditional commands (eq, gt, lt)
label_counter = 0


def unique_label(base="LABEL"):
    """
    Generates new labels for gt, eq, lt. 
    Input: nothing
    returns: string of the form LABEL_K where K is an integer that is the Kth label 
    """
    global label_counter
    label = f"{base}_{label_counter}"
    label_counter += 1
    return label

def translate_vm_to_asm(vm_files, asm_filename):
    """
    docstring here
    """
    asm_instructions = []
    
    # Add bootstrap code
    asm_instructions.extend(generate_bootstrap_code())
    
    # Translate each VM file and append its assembly code
    for vm_filename in vm_files:
        basename = os.path.splitext(os.path.basename(vm_filename))[0]
        asm_instructions.extend(translate_file(vm_filename, basename))

    # Write the output to the .asm file
    with open(asm_filename, 'w') as file:
        file.write('\n'.join(asm_instructions) + '\n')


def translate_file(vm_filename, basename):
    """
    Translates a single .vm file into assembly instructions.

    Inputs:
        vm_filename - the name of the .vm file
        basename - the base name of the file (used for static variables)
    Returns:
        list[string] - assembly code lines
    """
    asm_instructions = []

    with open(vm_filename, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('//'):
            continue

        command = line.split()
        asm_instructions.extend(translate_command(command, basename))

    return asm_instructions

def translate_command(command, basename):
    """
    Determines if the command is a push, pull, or arithmetic command and returns hack assembly code as a list 
    where each element is a line.

    input: list[string] - command
           string - basename
    returns list[string]
    """
    cmd_type = command[0]
    if cmd_type == 'push':
        return translate_push(command[1], command[2], basename)
    elif cmd_type == 'pop':
        return translate_pop(command[1], command[2], basename)
    elif cmd_type in COMMAND_TYPE[:9]:  # Arithmetic commands
        return translate_arithmetic(cmd_type)
    elif cmd_type == 'label':
        return translate_label(command[1])
    elif cmd_type == 'goto':
        return translate_goto(command[1])
    elif cmd_type == 'if-goto':
        return translate_if_goto(command[1])
    elif cmd_type == 'function':
        return translate_function(command[1], int(command[2]))
    elif cmd_type == 'call':
        return translate_call(command[1], int(command[2]))
    elif cmd_type == 'return':
        return translate_return()
    else:
        return []

def generate_bootstrap_code():
    """
    Generates the bootstrap code to initialize the stack pointer and call Sys.init.

    returns list[string] - the assembly instructions for the bootstrap code
    """
    instructions = [
        "@256",          # Set SP = 256
        "D=A",
        "@SP",
        "M=D"
    ]
    # Call Sys.init with 0 arguments
    instructions.extend(translate_call("Sys.init", 0))
    return instructions

def translate_function(func_name, n_vars):
    instructions = [f"({func_name})"]
    for _ in range(n_vars):
        instructions.extend([
            "@SP", "AM=M+1", "A=A-1", "M=0"  # Push 0 for each local variable
        ])
    return instructions

def translate_call(func_name, n_args):
    """
    Translates a call command, setting up a new stack frame for the called function.

    input: string - func_name, int - n_args
    returns list[string] - assembly code
    """
    return_label = unique_label("RETURN")
    instructions = [
        f"@{return_label}", "D=A", "@SP", "AM=M+1", "A=A-1", "M=D",  # Push return address
        "@LCL", "D=M", "@SP", "AM=M+1", "A=A-1", "M=D",              # Push LCL
        "@ARG", "D=M", "@SP", "AM=M+1", "A=A-1", "M=D",              # Push ARG
        "@THIS", "D=M", "@SP", "AM=M+1", "A=A-1", "M=D",             # Push THIS
        "@THAT", "D=M", "@SP", "AM=M+1", "A=A-1", "M=D",             # Push THAT
        f"@SP", "D=M", f"@{n_args + 5}", "D=D-A", "@ARG", "M=D",     # ARG = SP - n_args - 5
        "@SP", "D=M", "@LCL", "M=D",                                 # LCL = SP
        f"@{func_name}", "0;JMP",                                    # Jump to function
        f"({return_label})"                                          # Declare return label
    ]
    return instructions

def translate_return():
    """
    Translates a return command, restoring the caller's state and jumping to the return address.

    returns list[string] - assembly code
    """
    instructions = [
        "@LCL", "D=M", "@R13", "M=D",               # FRAME = LCL
        "@5", "A=D-A", "D=M", "@R14", "M=D",        # RET = *(FRAME-5)
        "@SP", "AM=M-1", "D=M", "@ARG", "A=M", "M=D",  # *ARG = pop()
        "@ARG", "D=M+1", "@SP", "M=D",              # SP = ARG + 1
        "@R13", "AM=M-1", "D=M", "@THAT", "M=D",    # THAT = *(FRAME-1)
        "@R13", "AM=M-1", "D=M", "@THIS", "M=D",    # THIS = *(FRAME-2)
        "@R13", "AM=M-1", "D=M", "@ARG", "M=D",     # ARG = *(FRAME-3)
        "@R13", "AM=M-1", "D=M", "@LCL", "M=D",     # LCL = *(FRAME-4)
        "@R14", "A=M", "0;JMP"                      # goto RET
    ]
    return instructions

def translate_label(label):
    """
    docstring
    """
    return [f"({label})"]

def translate_goto(label):
    """
    docstring
    """
    return [f"@{label}", "0;JMP"]

def translate_if_goto(label):
    """
    docstring
    """
    return [ 
        "@SP",
        "AM=M-1",
        "D=M",
        f"@{label}",
        "D;JNE"
    ]

def translate_push(segment, index, basename):
    """
    Translate push vm lines. Segment indicates type of the push command. 
    input: string - segment 
           index - int
           string - basename (for static)
    returns list[string] of the corresponding hack assembly code
    """
    SEGMENTS = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
    'temp': 5,
    'pointer': 3,
    'static': f"{basename}.{index}"
    }
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
                f"@{base_address + index}",
                "D=M",
                "@SP",
                "AM=M+1",
                "A=A-1",
                "M=D"
                ]
        elif segment == 'static':
            instructions = [
            f"@{basename}.{index}",
            "D=M",
            "@SP",
            "AM=M+1",
            "A=A-1",
            "M=D"
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

def translate_pop(segment, index, basename):
    """
    Translate pop vm lines. Segment deteremines type of pop command. 

    input: string - segment 
           index - int
           string - basename (for static)
    returns list[string] of the corresponding hack assembly code
    """
    SEGMENTS = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
    'temp': 5,
    'pointer': 3,
    'static': f"{basename}.{index}"
    }
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
        elif segment == 'static':
            instructions = [
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{base_address}",
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
    """
    Translates arithmetic commands.

    input: string - command
    returns list[string] of the corresponding hack assembly code
    """
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
    vm_files = sys.argv[1:]
    asm_filename = "Output.asm"
    translate_vm_to_asm(vm_files, asm_filename)
    print(f"Translation complete. Output written to {asm_filename}")
