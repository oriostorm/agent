import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):

        # Join and normalize
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    # print(full_path)

    working_directory = os.path.abspath(working_directory)
    # print(working_directory)

    # Check: is full_path inside working_directory?
    if os.path.commonpath([working_directory, full_path]) != working_directory:
        print(f'Error: Cannot access "{file_path}" as it is outside the permitted working directory')
        return
    
    if os.path.isfile(full_path):
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        print(file_content_string)
        if len(file_content_string) == MAX_CHARS:
            print(f"[...File {file_path} truncated at 10000 characters]")

