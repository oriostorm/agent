import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

WORKING_DIR = "./calculator"

AGENT_ITERATIONS = 5

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():

    num_args = len(sys.argv)

    if num_args == 1:
        print("Usage: python3 main.py <prompt for Gemini to answer>")
        sys.exit(1)
    
    args = parse_args()
    user_prompt = args.prompt
    

    messages = [ types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),]

    gemini_request_and_response(messages, user_prompt, args.verbose)


def parse_args():
    parser = argparse.ArgumentParser(description="an agentic CLI tool")
    parser.add_argument("prompt", type=str, help="The input to pass to agent to process")
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output with token values')
    return parser.parse_args()


def gemini_request_and_response(prompt_list, user_prompt, verbose_flag):

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    #print(api_key)

 #   call_content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
    
#loop starts
    for i in range(AGENT_ITERATIONS):

        try:
            print(f"iteration {i}: {prompt_list}")

            response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt_list,
            config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
            ))

            for candidate in response.candidates:
                prompt_list.append(candidate.content)

            if response.function_calls:
                for function_call in response.function_calls:
                    function_name = function_call.name
                    function_args = function_call.args
                    print(function_args)
                    print(f"Calling function: {function_name}({function_args})")
                    function_call = types.FunctionCall(name=function_name, args=function_args)
                    function_call_result = call_function(function_call, verbose_flag)
                    prompt_list.append(function_call_result)

                    if not function_call_result.parts[0].function_response.response:
                        raise ValueError("Big problem with function call!!!")
                    
                    
                    if verbose_flag:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    else:
                        print("successful but I didn't want to be verbose")

            if response.text:
                print(response.text)
            else:
                print("I am still running")

        except Exception as e:
            print(f"An Error occurred with my agent: {e}")

#loop ends

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: 
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name == "get_file_content" :
        print("get_file_content")
        function_result = get_file_content(WORKING_DIR, **function_call_part.args)
    elif function_call_part.name == "get_files_info" :
        print("get_files_info")
        function_result = get_files_info(WORKING_DIR, **function_call_part.args)
    elif function_call_part.name == "run_python_file" :
        function_result = run_python_file(WORKING_DIR, **function_call_part.args)
        print("run_python_file")
    elif function_call_part.name == "write_file" :
        print("write_file") 
        function_result = write_file(WORKING_DIR, **function_call_part.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
        )
    ],
    )

main()

# func_args = {
#     "file_path": "lorem.txt",
#     "content": "I want this to be in lorem ipsum"
# }

# function_call = types.FunctionCall(name= "write_file", args= func_args)

# print(call_function(function_call, True))