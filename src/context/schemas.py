from typing import Optional, Dict, List, Literal
from pydantic import BaseModel, Field


class ProductData(BaseModel):
    product_name: Optional[str] = None
    ingredients_text: Optional[str] = None
    nutrition: Optional[Dict] = None
    brands: Optional[str] = None


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class UserPreferences(BaseModel):
    dietary_goals: List[str] = Field(default_factory=list)
    restrictions: List[str] = Field(default_factory=list)


class ProductContext(BaseModel):
    source: Literal["barcode", "ocr", "text"]
    confidence: Literal["high", "medium", "low"]
    product_data: Optional[ProductData] = None
    raw_text: str = ""
    user_query: str = ""
    query_type: Literal["explanation", "comparison", "followup"] = "explanation"
    conversation_history: List[ConversationMessage] = Field(default_factory=list)
    user_preferences: UserPreferences = Field(default_factory=UserPreferences)
