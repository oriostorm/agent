import os
from dotenv import load_dotenv
from google import genai
import sys


def main():

    num_args = len(sys.argv)

    if num_args == 1 or num_args > 2:
        print("Usage: python3 main.py <prompt for Gemini to answer>")
        sys.exit(1)

    gemini_request_and_response(sys.argv[1])


def gemini_request_and_response(prompt):

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    #print(api_key)

    model = "gemini-2.0-flash-001"
 #   call_content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=prompt
    )
    print(response.text)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

main()