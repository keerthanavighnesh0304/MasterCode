
from unittest.mock import Mock, patch
from google.genai import errors
from agent.agent import run_agent_stream

# Simulate Gemini returning HTTP 503
api_error = errors.APIError(
    code=503,
    response_json={
        "error": {
            "message": "Service unavailable"
        }
    }
)

# Create a mock chat that always fails
mock_chat = Mock()
mock_chat.send_message.side_effect = api_error

# Prevent actual waiting during retries
with patch("agent.agent.time.sleep"):

    generator = run_agent_stream(
        "Hello MasterCode",
        mock_chat
    )

    try:
        next(generator)

    except errors.APIError as error:
        print("API error propagated:", error.code)

    except Exception as error:
        print("Unexpected error:", type(error).__name__, error)

print("API calls:", mock_chat.send_message.call_count)
