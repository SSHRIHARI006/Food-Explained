import easyocr
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(image):
    image_np = np.array(image)
    results = reader.readtext(image_np, detail=0)
    return "\n".join(results)
