from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "Explain whey protein vs yogurt in simple terms."}
    ]
)

print(response.content[0].text)
