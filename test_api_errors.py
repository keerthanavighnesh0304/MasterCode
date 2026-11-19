from google.genai import errors

print("Available Gemini API error classes:")

print("APIError:", errors.APIError)
print("ServerError:", errors.ServerError)
print("ClientError:", errors.ClientError)