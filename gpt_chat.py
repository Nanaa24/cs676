import os
import openai

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

print("Interactive GPT Chat (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Exiting chat...")
        break

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",   # You can also try "gpt-4" if your key has access
        messages=[{"role": "user", "content": user_input}],
        max_tokens=200
    )

    reply = response.choices[0].message.content
    print("GPT:", reply)
