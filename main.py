import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse


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

    model = "gemini-2.0-flash-001"
 #   call_content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=prompt_list
    )
    print(response.text)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

main()