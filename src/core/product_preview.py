def extract_product_preview(context):
    source = context.get("source")
    product_data = context.get("product_data")
    raw_text = context.get("raw_text", "")

    if source == "barcode" and product_data:
        return {
            "title": "Product (from barcode)",
            "name": product_data.get("product_name"),
            "brand": product_data.get("brands"),
            "ingredients": product_data.get("ingredients_text"),
            "confidence": "high"
        }

    if source == "ocr" and raw_text:
        ingredients = None
        for line in raw_text.split("\n"):
            if "ingredient" in line.lower():
                ingredients = line
                break

        if ingredients:
            return {
                "title": "Product details (from label)",
                "name": None,
                "brand": None,
                "ingredients": ingredients,
                "confidence": "medium"
            }

        return {
            "title": "Product details unclear",
            "name": None,
            "brand": None,
            "ingredients": None,
            "confidence": "low"
        }

    return None
