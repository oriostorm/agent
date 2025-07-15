import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):

    if not directory:
        directory = "."
    # Join and normalize
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    #print(full_path)

    working_directory = os.path.abspath(working_directory)
    #print(working_directory)

    # Check: is full_path inside working_directory?
    if os.path.commonpath([working_directory, full_path]) != working_directory:
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return

    if not os.path.isdir(full_path):
        f'Error: "{directory}" is not a directory'
    else:
        dir_list = os.listdir(full_path)

        for item in dir_list:
            file_size = os.path.getsize(os.path.join(full_path,item))
            is_dir = os.path.isdir(os.path.join(full_path,item))
            print(f"- {item}: file_size={file_size} bytes and is_dir={is_dir}")
