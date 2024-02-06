import os
import re

def extract_lines_with_slash_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()

    lines_with_slash = []
    for line in content:
        if '/' in line and "export" not in line and "require" not in line and "//" not in line and "import" not in line and "return" not in line and "</" not in line and "/>" not in line and "} from " not in line and "Math.floo" not in line and "/*" not in line:
            lines_with_slash.append(line)

    return lines_with_slash

def extract_all_lines_with_slash(base_directory):
    all_lines = []
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.js') or file.endswith('.jsx') or file.endswith('.tsx'):
                file_path = os.path.join(root, file)
                all_lines.extend(extract_lines_with_slash_from_file(file_path))
    return all_lines

base_directory = "/Users/office/Documents/timelyAI/chrone-react-native/src"
lines = extract_all_lines_with_slash(base_directory)
print("Extracted lines with '/':")
output_file_path = "extracted_lines.txt"
with open(output_file_path, 'w') as f:
    for line in lines:
        f.write(line + '\n')
