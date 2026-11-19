import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.gemini_tools import mastercode_tool
from agent.dispatcher import execute_tool


# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

client = genai.Client(api_key=api_key)

MODEL_ID = "gemini-3.5-flash-lite"

# Original user request
user_prompt = "List all the files in my workspace."


# STEP 1: Send request to Gemini
response = client.models.generate_content(
    model=MODEL_ID,
    contents=user_prompt,
    config=types.GenerateContentConfig(
        tools=[mastercode_tool]
    )
)

print("\n--- Gemini's Initial Response ---")

if response.function_calls:

    # STEP 2: Get Gemini's function request
    for function_call in response.function_calls:

        function_name = function_call.name
        arguments = function_call.args

        print("Requested tool:", function_name)
        print("Arguments:", arguments)

        # STEP 3: Execute through our dispatcher
        tool_result = execute_tool(function_name, arguments)

        print("\n--- Actual Tool Result ---")
        print(tool_result)

        # STEP 4: Prepare the function response
        function_response_part = types.Part.from_function_response(
            name=function_name,
            response=tool_result
        )

        function_response_content = types.Content(
            role="user",
            parts=[function_response_part]
        )

        # Preserve Gemini's original function-call message
        model_function_call_content = response.candidates[0].content

        # Send the complete conversation back to Gemini
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_prompt)]
                ),
                model_function_call_content,
                function_response_content
            ],
            config=types.GenerateContentConfig(
                tools=[mastercode_tool]
            )
            )

        

        
        print("\n--- Gemini's Final Answer ---")
        print(response.text)

else:
    print(response.text)

client.close()