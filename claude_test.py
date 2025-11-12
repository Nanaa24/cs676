from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-instant-1",
    messages=[{"role": "user", "content": "Hello Claude!"}],
    max_tokens=100
)

print(response["completion"])
