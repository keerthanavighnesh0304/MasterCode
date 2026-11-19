import os
from dotenv import load_dotenv
from google import genai
from agent.gemini_tools import read_file_tool

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MODEL_ID = "gemini-3.5-flash-lite"

response = client.models.generate_content(
    model=MODEL_ID,
    contents="Read the contents of sample.py in your workspace.",
    config={
        "tools": [read_file_tool]
    }
)

print("\n--- Gemini Response ---")

if response.function_calls:
    for function_call in response.function_calls:
        print("Function name:", function_call.name)
        print("Arguments:", function_call.args)
else:
    print("Text response:", response.text)

client.close()