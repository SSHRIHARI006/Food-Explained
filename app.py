import streamlit as st
from PIL import Image
from ocr import extract_text_from_image
from barcode import fetch_product_from_barcode
from context_builder import build_context
from product_preview import extract_product_preview
from reasoner import reason

st.set_page_config(page_title="Food, Explained", layout="centered")

st.title("Food, Explained")
st.caption("An AI assistant to help you understand food")

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
            user_query=user_query
        )

        preview = extract_product_preview(context)

        if preview:
            st.subheader(preview["title"])

            if preview.get("name"):
                st.write(f"Name: {preview['name']}")

            if preview.get("brand"):
                st.write(f"Brand: {preview['brand']}")

            if preview.get("ingredients"):
                with st.expander("Ingredients (from label)"):
                    st.write(preview["ingredients"])

            if preview["confidence"] == "high":
                st.caption("Confidence: High (barcode verified)")
            elif preview["confidence"] == "medium":
                st.caption("Confidence: Medium (label text detected)")
            else:
                st.caption("Confidence: Low (could not reliably extract details)")


        answer = reason(context)

        st.subheader("Response")
        st.write(answer)
