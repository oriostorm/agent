import os
from google.genai import types

MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="displays contents of requested file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the specifc file to read contents from, relative to working directory. If not provided, nothing will be displayed",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):

    #creat blank list
    full_func_string = []
        # Join and normalize
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    # print(full_path)

    working_directory = os.path.abspath(working_directory)
    # print(working_directory)

    # Check: is full_path inside working_directory?
    if os.path.commonpath([working_directory, full_path]) != working_directory:
        print_value = f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
        print(print_value)
        return print_value
    
    if os.path.isfile(full_path):
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return file_content_string
        print(file_content_string)
        if len(file_content_string) == MAX_CHARS:
            print_value = f"[...File {file_path} truncated at 10000 characters]"
            print(print_value)
            return print_value

