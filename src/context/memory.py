import streamlit as st
from typing import List, Dict, Optional
from src.context.schemas import ConversationMessage, UserPreferences
from src.config.settings import MAX_CONVERSATION_HISTORY


class ConversationMemory:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "user_preferences" not in st.session_state:
            st.session_state.user_preferences = UserPreferences()
    
    def add_message(self, role: str, content: str):
        message = ConversationMessage(role=role, content=content)
        st.session_state.messages.append(message.model_dump())
        
        if len(st.session_state.messages) > MAX_CONVERSATION_HISTORY * 2:
            st.session_state.messages = st.session_state.messages[-MAX_CONVERSATION_HISTORY * 2:]
    
    def get_recent_history(self, n: int = MAX_CONVERSATION_HISTORY) -> List[Dict]:
        return st.session_state.messages[-n * 2:] if st.session_state.messages else []
    
    def set_user_preference(self, key: str, value):
        prefs = st.session_state.user_preferences
        if hasattr(prefs, key):
            setattr(prefs, key, value)
            st.session_state.user_preferences = prefs
    
    def get_user_preferences(self) -> UserPreferences:
        return st.session_state.user_preferences
    
    def get_context_summary(self) -> str:
        history = self.get_recent_history()
        if not history:
            return ""
        
        lines = []
        for msg in history:
            role = msg["role"].capitalize()
            content = msg["content"][:100]
            lines.append(f"{role}: {content}")
        
        return "\n".join(lines)
    
    def clear(self):
        st.session_state.messages = []
        st.session_state.user_preferences = UserPreferences()
    
    def has_history(self) -> bool:
        return len(st.session_state.messages) > 0
