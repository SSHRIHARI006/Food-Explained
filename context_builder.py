def build_context(
    product_data=None,
    ocr_text="",
    user_query=""
):
    if product_data:
        source = "barcode"
        confidence = "high"
        raw_text = product_data.get("ingredients_text", "")
    elif ocr_text:
        source = "ocr"
        confidence = "medium"
        raw_text = ocr_text
    else:
        source = "text"
        confidence = "low"
        raw_text = ""

    return {
        "source": source,
        "product_data": product_data,
        "raw_text": raw_text,
        "user_query": user_query,
        "confidence": confidence
    }
