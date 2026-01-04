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
    
    if query_type == "comparison":
        prompt = PromptTemplate(
            input_variables=["source", "confidence", "raw_text", "user_query"],
            template=COMPARISON_TEMPLATE
        )
        messages = prompt.format(
            source=context.source,
            confidence=context.confidence,
            raw_text=context.raw_text,
            user_query=context.user_query
        )
        response = llm.invoke(messages)
        return response.content
    
    elif query_type == "followup":
        prompt = PromptTemplate(
            input_variables=["source", "confidence", "raw_text", "user_query", "conversation_history"],
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
            conversation_history=history_text
        )
        response = llm.invoke(messages)
        return response.content
    
    else:
        prompt = PromptTemplate(
            input_variables=["source", "confidence", "raw_text", "user_query"],
            template=EXPLANATION_TEMPLATE
        )
        messages = prompt.format(
            source=context.source,
            confidence=context.confidence,
            raw_text=context.raw_text,
            user_query=context.user_query if context.user_query else "None"
        )
        response = llm.invoke(messages)
        return response.content
