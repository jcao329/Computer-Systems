def clean_file(input_file):
    # Generate the output file name by appending '.out' before the file extension
    if '.' in input_file:
        # Split the file at the last dot to handle the extension
        base_name = input_file.rsplit('.', 1)[0]
        ext = '.' + input_file.rsplit('.', 1)[1]
    else:
        # If there's no extension, just append .out
        base_name = input_file
        ext = ''

    output_file = base_name + '.out' + ext

    with open(input_file, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []
    inside_comment = False

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            # Skip empty lines
            continue

        # Check for multi-line comments (/* ... */)
        if '/*' in stripped_line:
            inside_comment = True
            stripped_line = stripped_line.split('/*')[0].strip()

        if inside_comment:
            # Skip lines inside a comment block
            if '*/' in stripped_line:
                inside_comment = False
                stripped_line = stripped_line.split('*/')[-1].strip()
            else:
                # Skip the line if we're inside a comment block
                continue

        # Check for single-line comments (//)
        if '//' in stripped_line:
            stripped_line = stripped_line.split('//')[0].strip()

        # Add the line to cleaned_lines if it's not empty and not inside a comment block
        if stripped_line and not inside_comment:
            cleaned_lines.append(stripped_line)

    # Write the cleaned lines to the output file
    with open(output_file, 'w') as file:
        file.write('\n'.join(cleaned_lines))
