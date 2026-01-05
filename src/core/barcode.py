import requests
import numpy as np

try:
    from pyzbar.pyzbar import decode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False


def detect_barcode(image):
    if not PYZBAR_AVAILABLE:
        return None
    
    image_np = np.array(image)
    decoded = decode(image_np)

    if not decoded:
        return None

    return decoded[0].data.decode("utf-8")


def fetch_product_from_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "product_name": product.get("product_name"),
        "ingredients_text": product.get("ingredients_text"),
        "nutrition": product.get("nutriments"),
        "brands": product.get("brands")
    }
