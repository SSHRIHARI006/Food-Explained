import streamlit as st


def apply_custom_styles():
    st.markdown("""
        <style>
        .stApp {
            background: #0f172a;
        }
        
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            border: 1px solid #334155;
        }
        
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #334155;
            padding: 0.75rem;
            background-color: #1e293b;
            color: #e2e8f0;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #6366f1;
        }
        
        .stChatMessage {
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            background-color: #1e293b;
            border: 1px solid #334155;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 2rem;
            background-color: #1e293b;
            color: #94a3b8;
            border: 1px solid #334155;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #334155;
            color: #e2e8f0;
        }
        
        div[data-testid="stExpander"] {
            border-radius: 8px;
            border: 1px solid #334155;
            background: #1e293b;
        }
        
        label {
            color: #cbd5e1 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def render_confidence_badge(confidence: str):
    colors = {
        "high": "#10b981",
        "medium": "#3b82f6",
        "low": "#f59e0b"
    }
    
    text = {
        "high": "Verified via Barcode",
        "medium": "Detected from Label",
        "low": "Limited Data"
    }
    
    color = colors.get(confidence, colors["low"])
    badge_text = text.get(confidence, "Unknown")
    
    st.markdown(f"""
        <div style='display: inline-block; background: #1e293b; 
                    padding: 0.5rem 1rem; border-radius: 6px; 
                    border-left: 3px solid {color}; border: 1px solid #334155;'>
            <span style='color: #e2e8f0; font-weight: 500; font-size: 0.9rem;'>
                {badge_text}
            </span>
        </div>
    """, unsafe_allow_html=True)


def render_product_card(preview: dict):
    st.markdown("""
        <div style='background: #1e293b; padding: 1.5rem; border-radius: 8px; 
                    border: 1px solid #334155; margin-bottom: 1.5rem;'>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <h2 style='color: #e2e8f0; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 600;'>
            {preview['title']}
        </h2>
    """, unsafe_allow_html=True)
    
    if preview.get("name") or preview.get("brand"):
        cols = st.columns(2)
        with cols[0]:
            if preview.get("name"):
                st.markdown(f"""
                    <div style='margin-bottom: 0.75rem;'>
                        <span style='color: #94a3b8; font-size: 0.85rem;'>Product</span><br>
                        <span style='color: #e2e8f0; font-weight: 500;'>{preview['name']}</span>
                    </div>
                """, unsafe_allow_html=True)
        with cols[1]:
            if preview.get("brand"):
                st.markdown(f"""
                    <div style='margin-bottom: 0.75rem;'>
                        <span style='color: #94a3b8; font-size: 0.85rem;'>Brand</span><br>
                        <span style='color: #e2e8f0; font-weight: 500;'>{preview['brand']}</span>
                    </div>
                """, unsafe_allow_html=True)
    
    if preview.get("ingredients"):
        with st.expander("View Ingredients", expanded=False):
            st.markdown(f"""
                <div style='background: #0f172a; padding: 1rem; border-radius: 6px; 
                            font-family: monospace; font-size: 0.85rem; color: #cbd5e1;
                            border: 1px solid #334155;'>
                    {preview['ingredients']}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
    render_confidence_badge(preview["confidence"])
    
    st.markdown("</div>", unsafe_allow_html=True)


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
        st.markdown("""
            <div style='padding: 1rem 0;'>
                <h2 style='color: #e2e8f0; margin-bottom: 0.5rem; font-size: 1.3rem;'>Settings</h2>
                <p style='color: #94a3b8; font-size: 0.9rem;'>Personalize your experience</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("<h3 style='color: #e2e8f0; font-size: 1rem; margin-bottom: 0.5rem;'>Dietary Goals</h3>", unsafe_allow_html=True)
        
        dietary_goals = st.text_input(
            "Goals",
            placeholder="high protein, low sugar",
            label_visibility="collapsed"
        )
        
        st.markdown("<h3 style='color: #e2e8f0; font-size: 1rem; margin: 1rem 0 0.5rem 0;'>Restrictions</h3>", unsafe_allow_html=True)
        
        restrictions = st.text_input(
            "Restrictions",
            placeholder="vegetarian, gluten-free",
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", use_container_width=True):
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
                st.success("Saved")
        
        with col2:
            if st.button("Clear", use_container_width=True):
                memory.clear()
                st.rerun()
        
        st.markdown("---")
        
        prefs = memory.get_user_preferences()
        if prefs.dietary_goals or prefs.restrictions:
            st.markdown("""
                <div style='background: #1e293b; padding: 1rem; border-radius: 6px; 
                            border-left: 3px solid #6366f1; border: 1px solid #334155;'>
                    <h4 style='color: #e2e8f0; margin: 0 0 0.5rem 0; font-size: 0.9rem;'>
                        Active Preferences
                    </h4>
            """, unsafe_allow_html=True)
            
            if prefs.dietary_goals:
                st.markdown(f"<span style='color: #cbd5e1;'><strong>Goals:</strong> {', '.join(prefs.dietary_goals)}</span>", unsafe_allow_html=True)
            if prefs.restrictions:
                st.markdown(f"<span style='color: #cbd5e1;'><strong>Restrictions:</strong> {', '.join(prefs.restrictions)}</span>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
