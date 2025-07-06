import os

def write_file(working_directory, file_path, content):

        # Join and normalize
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    #print(full_path)

    working_directory = os.path.abspath(working_directory)
    #print(working_directory)

    # Check: is full_path inside working_directory?
    if os.path.commonpath([working_directory, full_path]) != working_directory:
        print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        return
    
    if not os.path.exists(full_path):
        try:
            os.makedirs(file_path)
        except:
            print(f'Error: Unable to make dir "{file_path}"')
            return

    with open(full_path, "w") as f:
        try:
            f.write(content)
            print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        except:
            print(f'Error: Unable to write requested content to "{file_path}"')

#write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
#write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
#write_file("calculator", "/tmp/temp.txt", "this should not be allowed")