import os
import subprocess
from google.genai import types

FILE_TYPE = ".py"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to execute, relative to the working directory",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    #print("running")
    # Join and normalize
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    #print(full_path)

    working_directory = os.path.abspath(working_directory)
    #print(working_directory)

    # Check: is full_path inside working_directory?

    #print(full_path)
    function_output = ""

    if os.path.commonpath([working_directory, full_path]) != working_directory:
        function_output = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        return function_output

    if not os.path.exists(full_path):
        function_output = f'Error: File "{file_path}" not found.'
        #print(full_path)
        return function_output

    root, extension = os.path.splitext(file_path)
    if extension.lower() != FILE_TYPE:
        function_output = f'Error: "{file_path}" is not a Python file.'
        return function_output

    try:
        result = subprocess.run(["python3", file_path], text = True, capture_output=True, timeout=30, cwd=working_directory)
    except Exception as e:
        function_output = f"Error: executing Python file: {e}"
        return function_output
    
    if result.stdout:
        function_output = f"STDOUT:", result.stdout
    if result.stderr:
        function_output = f"STDERR:", result.stderr
    if result.returncode != 0:
        function_output = f"Process returned with code", result.returncode
    if not result.stdout and result.returncode == 0:
        function_output = "No output produced"

    return function_output

# run_python_file("calculator", "sub_test.py")