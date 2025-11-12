import anthropic
import os

# Initialize client with your API key
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Make a request to Claude
response = client.messages.create(
    model="claude-instant-1",  # Use a model your account can access
    messages=[{"role": "user", "content": "Hello Claude!"}],
    max_tokens=100
)

# Print Claude's response
print("Claude says:", response["completion"])