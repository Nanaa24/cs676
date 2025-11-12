# chatgpt_box.py
from openai import OpenAI
import os

# Make sure your API key is set here or via environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Interactive GPT Chat (type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[{"role": "user", "content": user_input}]
    )

    # Correct way to access AI's response in v2
    print("AI:", response.choices[0].message.content)
    