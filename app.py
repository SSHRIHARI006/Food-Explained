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
    render_preference_panel
)

st.set_page_config(page_title="Food, Explained", layout="centered")

# Initialize memory
memory = ConversationMemory()

# Initialize session state for product context
if "product_data" not in st.session_state:
    st.session_state.product_data = None
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "product_preview" not in st.session_state:
    st.session_state.product_preview = None
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

st.title("Food, Explained")
st.caption("An AI assistant to help you understand food")

render_preference_panel(memory)

# Product input section (only show if not yet analyzed or user wants to change)
with st.container():
    if not st.session_state.analyzed:
        st.subheader("Add Product")
        
        uploaded_image = st.file_uploader(
            "Upload the back of a food product",
            type=["jpg", "jpeg", "png"]
        )

        barcode_input = st.text_input(
            "Optional: enter barcode number"
        )

        initial_query = st.text_input(
            "Optional: ask a question about the product"
        )

        analyze = st.button("Analyze Product", type="primary")

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
        # Show product card if available
        if st.session_state.product_preview:
            render_product_card(st.session_state.product_preview)
        
        # Option to analyze a new product
        if st.button("Analyze New Product"):
            st.session_state.analyzed = False
            st.session_state.product_data = None
            st.session_state.extracted_text = ""
            st.session_state.product_preview = None
            memory.clear()
            st.rerun()

# Chat interface (only show after initial analysis)
if st.session_state.analyzed:
    st.divider()
    st.subheader("Conversation")
    
    # Display conversation history
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
    
    # Chat input for follow-up questions
    followup_query = st.chat_input("Ask a follow-up question about this product...")
    
    if followup_query:
        # Add user message to display
        with st.chat_message("user"):
            st.write(followup_query)
        
        # Build context with conversation history
        context = build_context(
            product_data=st.session_state.product_data,
            ocr_text=st.session_state.extracted_text,
            user_query=followup_query,
            memory=memory
        )
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = reason(context)
                st.markdown(answer)
        
        # Save to memory
        memory.add_message("user", followup_query)
        memory.add_message("assistant", answer)
        
        st.rerun()
