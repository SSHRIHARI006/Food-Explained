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
    render_conversation_history,
    render_preference_panel
)

st.set_page_config(page_title="Food, Explained", layout="centered")

memory = ConversationMemory()

st.title("Food, Explained")
st.caption("An AI assistant to help you understand food")

render_preference_panel(memory)

uploaded_image = st.file_uploader(
    "Upload the back of a food product",
    type=["jpg", "jpeg", "png"]
)

barcode_input = st.text_input(
    "Optional: enter barcode number"
)

user_query = st.text_input(
    "Optional: ask a question"
)

analyze = st.button("Analyze")

if analyze:
    if not uploaded_image and not barcode_input and not user_query:
        st.warning("Provide an image, barcode, or question")
    else:
        product_data = None
        extracted_text = ""

        if uploaded_image:
            image = Image.open(uploaded_image)
            st.subheader("Uploaded Image")
            st.image(image, use_container_width=True)

        if barcode_input.strip():
            product_data = fetch_product_from_barcode(barcode_input.strip())

        if not product_data and uploaded_image:
            extracted_text = extract_text_from_image(image)

        context = build_context(
            product_data=product_data,
            ocr_text=extracted_text,
            user_query=user_query,
            memory=memory
        )

        preview = extract_product_preview(context.model_dump())

        if preview:
            render_product_card(preview)

        answer = reason(context)

        memory.add_message("user", user_query if user_query else "Analyze this product")
        memory.add_message("assistant", answer)

        st.subheader("Response")
        st.write(answer)

        render_conversation_history(memory)
