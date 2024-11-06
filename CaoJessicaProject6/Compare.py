def compare(file1, file2):
    try:
        with open(file1, 'r') as file1, open(file2, 'r') as file2:
            line_num = 1
            differences = False
            count = 0
            for line1, line2 in zip(file1, file2):
                if line1 != line2:
                    differences = True
                    print(f"Difference at line {line_num}:")
                    print(f"File 1: {line1.strip()}")
                    print(f"File 2: {line2.strip()}")
                    count += 1
                    if count==7:
                        return
                line_num += 1
            
            # Check if one file has extra lines
            extra_file1 = file1.readlines()
            extra_file2 = file2.readlines()
            
            if extra_file1:
                differences = True
                for extra_line in extra_file1:
                    print(f"Extra line in File 1 at line {line_num}: {extra_line.strip()}")
                    line_num += 1
            
            if extra_file2:
                differences = True
                for extra_line in extra_file2:
                    print(f"Extra line in File 2 at line {line_num}: {extra_line.strip()}")
                    line_num += 1
            
            if not differences:
                print("Files are identical.")
    except FileNotFoundError as e:
        print(f"Error: {e}")

compare('Max.hack', 'Max1.hack')