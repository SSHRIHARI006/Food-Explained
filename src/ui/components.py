import streamlit as st


def render_confidence_badge(confidence: str):
    if confidence == "high":
        st.success("Confidence: High (barcode verified)", icon="✓")
    elif confidence == "medium":
        st.info("Confidence: Medium (label text detected)", icon="ℹ")
    else:
        st.warning("Confidence: Low (insufficient data)", icon="⚠")


def render_product_card(preview: dict):
    st.subheader(preview["title"])
    
    if preview.get("name"):
        st.markdown(f"**Product:** {preview['name']}")
    
    if preview.get("brand"):
        st.markdown(f"**Brand:** {preview['brand']}")
    
    if preview.get("ingredients"):
        with st.expander("Ingredients"):
            st.text(preview["ingredients"])
    
    render_confidence_badge(preview["confidence"])


def render_conversation_history(memory):
    if not memory.has_history():
        return
    
    with st.expander("Conversation History"):
        history = memory.get_recent_history()
        for msg in history:
            role = msg["role"]
            content = msg["content"]
            
            if role == "user":
                st.markdown(f"**You:** {content}")
            else:
                st.markdown(f"**Assistant:** {content[:200]}...")


def render_preference_panel(memory):
    with st.sidebar:
        st.header("Preferences")
        
        dietary_goals = st.text_input(
            "Dietary goals (comma separated)",
            placeholder="high protein, low sugar"
        )
        
        restrictions = st.text_input(
            "Restrictions (comma separated)",
            placeholder="vegetarian, gluten-free"
        )
        
        if st.button("Save Preferences"):
            if dietary_goals:
                memory.set_user_preference(
                    "dietary_goals", 
                    [g.strip() for g in dietary_goals.split(",")]
                )
            if restrictions:
                memory.set_user_preference(
                    "restrictions",
                    [r.strip() for r in restrictions.split(",")]
                )
            st.success("Preferences saved")
        
        if st.button("Clear Conversation"):
            memory.clear()
            st.rerun()
