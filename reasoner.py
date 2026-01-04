import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

SYSTEM_PROMPT = """
You are an AI assistant that helps people think clearly about food.

Rules:
- Do not invent product names or brands.
- Do not label foods as good, bad, healthy, or unhealthy.
- Avoid fear-based or alarmist language.
- Explain trade-offs, not absolutes.
- Be honest about uncertainty.

Response format:
- Always respond in clean Markdown.
- Use short section headers.
- Keep the tone calm, practical, and human.

You are not a doctor. Do not give medical advice.
"""


def reason(context):
    source = context.get("source", "unknown")
    confidence = context.get("confidence", "low")
    raw_text = context.get("raw_text", "")
    user_query = context.get("user_query", "")

    prompt = f"""
Context source: {source}
Confidence level: {confidence}

Product information:
{raw_text}

User question:
{user_query if user_query else "None"}

Task:
Respond using the following Markdown structure:

## Short answer
A direct response to the user's question or the most relevant takeaway.

## How it works
Explain what this food or drink does in the body, based on available information.

## Trade-offs
Explain differences, limitations, or things to be aware of, without fear.

## Practical way to use it
Give a realistic, everyday way to think about or consume this food.

If information is incomplete, say so calmly.
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text
