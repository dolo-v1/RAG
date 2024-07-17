import os

# Function to read text files
def load_text_files(directory):
    text_data = {}
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_data[file] = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text_data[file] = f.read()
    return text_data
