from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Try a simple request with claude-instant-1
response = client.messages.create(
    model="claude-instant-1",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100
)

print(response["completion"])