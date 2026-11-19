
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.gemini_tools import list_files_tool

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Use the same model ID that worked in your main.py
MODEL_ID = "gemini-3.5-flash-lite"

# Ask Gemini to use the available tool
response = client.models.generate_content(
    model=MODEL_ID,
    contents="List all the files available in your workspace.",
    config=types.GenerateContentConfig(
        tools=[list_files_tool]
    )
)

# Inspect Gemini's response
print("\n--- Gemini Response ---")

if response.function_calls:
    for function_call in response.function_calls:
        print("Function name:", function_call.name)
        print("Arguments:", function_call.args)
else:
    print("Text response:", response.text)

client.close()
