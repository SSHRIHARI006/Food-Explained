import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = "claude-3-haiku-20240307"
MAX_TOKENS = 500
MAX_CONVERSATION_HISTORY = 5
