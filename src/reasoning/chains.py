from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from src.config.settings import ANTHROPIC_API_KEY, MODEL_NAME, MAX_TOKENS
from src.config.prompts_config import (
    SYSTEM_PROMPT,
    EXPLANATION_TEMPLATE,
    COMPARISON_TEMPLATE,
    FOLLOWUP_TEMPLATE
)
from src.context.schemas import ProductContext


llm = ChatAnthropic(
    anthropic_api_key=ANTHROPIC_API_KEY,
    model_name=MODEL_NAME,
    max_tokens=MAX_TOKENS,
    temperature=0.7
)


def reason(context: ProductContext) -> str:
    query_type = context.query_type
    
    prefs = context.user_preferences
    preferences_text = ""
    if prefs and (prefs.dietary_goals or prefs.restrictions):
        goals = f"Goals: {', '.join(prefs.dietary_goals)}" if prefs.dietary_goals else ""
        restrictions = f"Restrictions: {', '.join(prefs.restrictions)}" if prefs.restrictions else ""
        preferences_text = f"{goals}\n{restrictions}".strip() or "None specified"
    else:
        preferences_text = "None specified"
    
    if query_type == "comparison":
        prompt = PromptTemplate(
            input_variables=["source", "confidence", "raw_text", "user_query", "user_preferences"],
            template=COMPARISON_TEMPLATE
        )
        messages = prompt.format(
            source=context.source,
            confidence=context.confidence,
            raw_text=context.raw_text,
            user_query=context.user_query,
            user_preferences=preferences_text
        )
        response = llm.invoke(messages)
        return response.content
    
    elif query_type == "followup":
        prompt = PromptTemplate(
            input_variables=["source", "confidence", "raw_text", "user_query", "conversation_history", "user_preferences"],
            template=FOLLOWUP_TEMPLATE
        )
        history_text = "\n".join([
            f"{msg.role}: {msg.content}" 
            for msg in context.conversation_history
        ])
        messages = prompt.format(
            source=context.source,
            confidence=context.confidence,
            raw_text=context.raw_text,
            user_query=context.user_query,
            conversation_history=history_text,
            user_preferences=preferences_text
        )
        response = llm.invoke(messages)
        return response.content
    
    else:
        prompt = PromptTemplate(
            input_variables=["source", "confidence", "raw_text", "user_query", "user_preferences"],
            template=EXPLANATION_TEMPLATE
        )
        messages = prompt.format(
            source=context.source,
            confidence=context.confidence,
            raw_text=context.raw_text,
            user_query=context.user_query if context.user_query else "None",
            user_preferences=preferences_text
        )
        response = llm.invoke(messages)
        return response.content
