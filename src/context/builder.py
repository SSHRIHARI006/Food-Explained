from typing import Optional, Dict
from src.context.schemas import ProductContext, ProductData, ConversationMessage, UserPreferences
from src.context.memory import ConversationMemory


def classify_query(user_query: str) -> str:
    query_lower = user_query.lower()
    
    comparison_keywords = ["compare", "vs", "versus", "difference between", "better than"]
    if any(keyword in query_lower for keyword in comparison_keywords):
        return "comparison"
    
    followup_keywords = ["what if", "how about", "what about", "also", "and if"]
    if any(keyword in query_lower for keyword in followup_keywords):
        return "followup"
    
    return "explanation"


def build_context(
    product_data: Optional[Dict] = None,
    ocr_text: str = "",
    user_query: str = "",
    memory: Optional[ConversationMemory] = None
) -> ProductContext:
    
    if product_data:
        source = "barcode"
        confidence = "high"
        raw_text = product_data.get("ingredients_text") or ""
        product_obj = ProductData(**product_data)
    elif ocr_text:
        source = "ocr"
        confidence = "medium"
        raw_text = ocr_text or ""
        product_obj = None
    else:
        source = "text"
        confidence = "low"
        raw_text = ""
        product_obj = None
    
    query_type = classify_query(user_query) if user_query else "explanation"
    
    conversation_history = []
    user_preferences = None
    
    if memory:
        history = memory.get_recent_history()
        conversation_history = [ConversationMessage(**msg) for msg in history]
        user_preferences = memory.get_user_preferences()
    
    return ProductContext(
        source=source,
        confidence=confidence,
        product_data=product_obj,
        raw_text=raw_text,
        user_query=user_query,
        query_type=query_type,
        conversation_history=conversation_history,
        user_preferences=user_preferences if user_preferences else UserPreferences()
    )
