
import os
import time

from google.genai import errors
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.gemini_tools import mastercode_tool
from agent.dispatcher import execute_tool


# --------------------------------------------------
# GEMINI CONFIGURATION
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

client = genai.Client(api_key=api_key)

MODEL_ID = "gemini-3.5-flash-lite"


# --------------------------------------------------
# CREATE GEMINI CHAT
# --------------------------------------------------

def create_chat():

    return client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            tools=[mastercode_tool]
        )
    )


# --------------------------------------------------
# API ERROR HANDLING AND RETRY
# --------------------------------------------------

def send_with_retry(chat, message, max_attempts=3):

    for attempt in range(1, max_attempts + 1):

        try:
            print(f"Sending request to Gemini (Attempt {attempt})...")

            response = chat.send_message(message)

            return response

        except errors.APIError as error:

            retryable_codes = [429, 500, 502, 503, 504]

            if error.code not in retryable_codes:
                raise

            if attempt == max_attempts:
                raise

            wait_time = 2 ** attempt

            print(f"Gemini API error: {error.code}")
            print(f"Retrying in {wait_time} seconds...")

            time.sleep(wait_time)


# --------------------------------------------------
# CLI AGENT
# --------------------------------------------------

def run_agent(user_prompt):

    # Create a new conversation
    chat = create_chat()

    response = send_with_retry(chat, user_prompt)

    max_iterations = 5
    iteration = 0

    while iteration < max_iterations:

        iteration += 1

        print(f"\n--- Agent Iteration {iteration} ---")

        if response.function_calls:

            function_response_parts = []

            for function_call in response.function_calls:

                function_name = function_call.name
                arguments = function_call.args

                print("Requested tool:", function_name)
                print("Arguments:", arguments)

                # Require approval for sensitive actions
                if function_name in [
                    "write_file",
                    "edit_file",
                    "run_python_file"
                ]:

                    print("\nMasterCode wants to perform this action:")
                    print("Tool:", function_name)
                    print("Arguments:", arguments)

                    approval = input(
                        "Do you approve this action? (yes/no): "
                    )

                    if approval.strip().lower() in ["yes", "y"]:

                        tool_result = execute_tool(
                            function_name,
                            arguments
                        )

                    else:

                        tool_result = {
                            "error": "Action rejected by the user."
                        }

                else:

                    tool_result = execute_tool(
                        function_name,
                        arguments
                    )

                print("Tool result:", tool_result)

                # Prepare function response for Gemini
                function_response_part = types.Part.from_function_response(
                    name=function_name,
                    response=tool_result
                )

                function_response_parts.append(
                    function_response_part
                )

            # Send all tool results together
            response = send_with_retry(
                chat,
                function_response_parts
            )

        else:

            print("\n--- Final Answer ---")
            print(response.text)

            return response.text

    print("\nMaximum tool iterations reached.")

    return None


# --------------------------------------------------
# STREAMLIT AGENT
# --------------------------------------------------

def run_agent_stream(user_prompt, chat=None):

    # Reuse an existing conversation when provided.
    # Otherwise, create a new conversation.
    if chat is None:
        chat = create_chat()

    response = send_with_retry(chat, user_prompt)

    max_iterations = 5

    for iteration in range(1, max_iterations + 1):

        if response.function_calls:

            function_response_parts = []

            for function_call in response.function_calls:

                function_name = function_call.name
                arguments = function_call.args

                # Notify Streamlit about the requested tool
                yield {
                    "type": "tool_requested",
                    "tool_name": function_name,
                    "arguments": arguments
                }

                # Approval required for sensitive actions
                if function_name in [
                    "write_file",
                    "edit_file",
                    "run_python_file"
                ]:
                    approval = yield {
                        "type": "approval_required",
                        "tool_name": function_name,
                        "arguments": arguments
                    }

                    if approval:

                        tool_result = execute_tool(
                            function_name,
                            arguments
                        )

                    else:

                        tool_result = {
                            "error": "Action rejected by the user."
                        }

                else:

                    # Read/list tools execute without approval
                    tool_result = execute_tool(
                        function_name,
                        arguments
                    )

                # Send tool result to Streamlit
                yield {
                    "type": "tool_result",
                    "tool_name": function_name,
                    "result": tool_result
                }

                # Prepare function response for Gemini
                function_response_part = types.Part.from_function_response(
                    name=function_name,
                    response=tool_result
                )

                function_response_parts.append(
                    function_response_part
                )

            # Send all tool responses to Gemini together
            response = send_with_retry(
                chat,
                function_response_parts
            )

        else:

            # Gemini has completed the task
            yield {
                "type": "final",
                "text": response.text
            }

            return

    # Maximum iteration limit
    yield {
        "type": "limit",
        "text": "Maximum tool iterations reached."
    }
