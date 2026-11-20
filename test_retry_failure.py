from unittest.mock import Mock, patch
from google.genai import errors
from agent.agent import send_with_retry

# Simulate Gemini returning HTTP 503
api_error = errors.APIError(
    code=503,
    response_json={"error": {"message": "Service unavailable"}}
)

mock_chat = Mock()
mock_chat.send_message.side_effect = api_error

with patch("agent.agent.time.sleep") as mock_sleep:

    try:
        send_with_retry(mock_chat, "Hello", max_attempts=3)

    except errors.APIError as error:
        print("Final API error:", error.code)

    print("API calls:", mock_chat.send_message.call_count)
    print("Retry waits:", mock_sleep.call_count)