from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Some accounts support listing models (if available)
try:
    models = client.models.list()
    print("Available models:", models)
except Exception as e:
    print("Error:", e)