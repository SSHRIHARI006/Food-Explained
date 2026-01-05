import streamlit as st
from PIL import Image
from src.core.ocr import extract_text_from_image
from src.core.barcode import fetch_product_from_barcode
from src.core.product_preview import extract_product_preview
from src.context.builder import build_context
from src.context.memory import ConversationMemory
from src.reasoning.chains import reason
from src.ui.components import (
    render_product_card,
    render_preference_panel,
    apply_custom_styles
)

st.set_page_config(
    page_title="Food, Explained",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "AI-powered food product analysis"
    }
)

apply_custom_styles()

memory = ConversationMemory()

if "product_data" not in st.session_state:
    st.session_state.product_data = None
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "product_preview" not in st.session_state:
    st.session_state.product_preview = None
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

render_preference_panel(memory)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.5rem;'>
                Food, Explained
            </h1>
            <p style='font-size: 1rem; color: #94a3b8; margin-top: 0;'>
                AI-powered food product analysis
            </p>
        </div>
    """, unsafe_allow_html=True)

if not st.session_state.analyzed:
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        with st.container():
            st.markdown("""
                <div style='background: #1e293b; padding: 1.5rem; border-radius: 8px; 
                            margin-bottom: 2rem; border: 1px solid #334155;'>
                    <h2 style='color: #e2e8f0; margin: 0; font-size: 1.3rem;'>Get Started</h2>
                    <p style='color: #94a3b8; margin-top: 0.5rem;'>
                        Upload an image or enter a barcode to analyze any food product
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Upload Image", "Enter Barcode"])
            
            with tab1:
                uploaded_image = st.file_uploader(
                    "Choose a product image",
                    type=["jpg", "jpeg", "png"],
                    label_visibility="collapsed"
                )
                if uploaded_image:
                    st.image(Image.open(uploaded_image), use_container_width=True, caption="Product Image")
            
            with tab2:
                barcode_input = st.text_input(
                    "Enter barcode number",
                    placeholder="e.g., 737628064502",
                    label_visibility="collapsed"
                )
            
            initial_query = st.text_input(
                "Ask a specific question (optional)",
                placeholder="e.g., Is this suitable for diabetics?"
            )
            
            st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
            analyze = st.button("Analyze Product", type="primary", use_container_width=True)

        if analyze:
            if not uploaded_image and not barcode_input:
                st.warning("Please provide an image or barcode")
            else:
                product_data = None
                extracted_text = ""

                if uploaded_image:
                    image = Image.open(uploaded_image)
                    st.image(image, use_container_width=True, caption="Uploaded Image")

                if barcode_input.strip():
                    with st.spinner("Fetching product data..."):
                        product_data = fetch_product_from_barcode(barcode_input.strip())

                if not product_data and uploaded_image:
                    with st.spinner("Extracting text from image..."):
                        extracted_text = extract_text_from_image(image)

                # Store in session state
                st.session_state.product_data = product_data
                st.session_state.extracted_text = extracted_text
                st.session_state.analyzed = True

                # Build context and get initial response
                context = build_context(
                    product_data=product_data,
                    ocr_text=extracted_text,
                    user_query=initial_query if initial_query else "Analyze this product",
                    memory=memory
                )

                preview = extract_product_preview(context.model_dump())
                st.session_state.product_preview = preview

                with st.spinner("Analyzing..."):
                    answer = reason(context)

                memory.add_message("user", initial_query if initial_query else "Analyze this product")
                memory.add_message("assistant", answer)

                st.rerun()
else:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.session_state.product_preview:
            render_product_card(st.session_state.product_preview)
        
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
        if st.button("Analyze New Product", use_container_width=True):
            st.session_state.analyzed = False
            st.session_state.product_data = None
            st.session_state.extracted_text = ""
            st.session_state.product_preview = None
            memory.clear()
            st.rerun()

if st.session_state.analyzed:
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
            <div style='margin-bottom: 1.5rem;'>
                <h2 style='color: #e2e8f0; margin-bottom: 0.5rem; font-size: 1.5rem;'>Conversation</h2>
                <p style='color: #94a3b8;'>Ask follow-up questions about this product</p>
            </div>
        """, unsafe_allow_html=True)
    
        chat_container = st.container()
        with chat_container:
            history = memory.get_recent_history()
            if history:
                for msg in history:
                    role = msg["role"]
                    content = msg["content"]
                    
                    if role == "user":
                        with st.chat_message("user"):
                            st.write(content)
                    else:
                        with st.chat_message("assistant"):
                            st.markdown(content)
        
        followup_query = st.chat_input("Ask a follow-up question...")
    
        if followup_query:
            with st.chat_message("user"):
                st.write(followup_query)
            
            context = build_context(
                product_data=st.session_state.product_data,
                ocr_text=st.session_state.extracted_text,
                user_query=followup_query,
                memory=memory
            )
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = reason(context)
                st.markdown(answer)
        
        # Save to memory
        memory.add_message("user", followup_query)
        memory.add_message("assistant", answer)
        
        st.rerun()
