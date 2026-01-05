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

EXPLANATION_TEMPLATE = """
Context source: {source}
Confidence level: {confidence}

Product information:
{raw_text}

User question:
{user_query}

User preferences:
{user_preferences}

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

Consider the user's stated preferences when relevant, but do not override their judgment.
If information is incomplete, say so calmly.
"""

COMPARISON_TEMPLATE = """
Context source: {source}
Confidence level: {confidence}

Products being compared:
{raw_text}

User question:
{user_query}

User preferences:
{user_preferences}

Task:
Compare these products using the following structure:

## Key differences
What makes these products different from each other.

## What to consider
Context-dependent factors that matter for choosing between them.

## Practical takeaway
Simple guidance based on use case, frequency, or preference.

Avoid declaring winners. Focus on trade-offs.
Consider the user's stated preferences when relevant, but respect that both options may have valid use cases.
"""

FOLLOWUP_TEMPLATE = """
Context source: {source}
Confidence level: {confidence}

Product information:
{raw_text}

Previous conversation:
{conversation_history}

User preferences:
{user_preferences}

Current question:
{user_query}

Task:
Answer the follow-up question using previous context. Keep the response focused and practical.

Important:
- Reference previous conversation only when directly relevant
- Do not repeat information already provided unless clarifying
- Consider user preferences, but do not let them override current context if the question is exploratory
- If the question is unrelated to preferences or history, answer it directly

Memory should inform, not override.
"""
