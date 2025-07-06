import os
import subprocess

FILE_TYPE = ".py"

def run_python_file(working_directory, file_path):
    #print("running")
    # Join and normalize
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    #print(full_path)

    working_directory = os.path.abspath(working_directory)
    #print(working_directory)

    # Check: is full_path inside working_directory?

    #print(full_path)
    if os.path.commonpath([working_directory, full_path]) != working_directory:
        print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        return

    if not os.path.exists(full_path):
        print(f'Error: File "{file_path}" not found.')
        #print(full_path)
        return

    root, extension = os.path.splitext(file_path)
    if extension.lower() != FILE_TYPE:
        print(f'Error: "{file_path}" is not a Python file.')
        return

    try:
        result = subprocess.run(["python3", file_path], text = True, capture_output=True, timeout=30, cwd=working_directory)
    except Exception as e:
        print(f"Error: executing Python file: {e}")
        return
    
    if result.stdout:
        print(f"STDOUT:", result.stdout)
    if result.stderr:
        print(f"STDERR:", result.stderr)
    if result.returncode != 0:
        print(f"Process returned with code", result.returncode)
    if not result.stdout and result.returncode == 0:
        print("No output produced")

# run_python_file("calculator", "sub_test.py")