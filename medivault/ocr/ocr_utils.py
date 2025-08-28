import os
import base64
import mimetypes
from mistralai import Mistral

api_key = os.environ.get("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

def run_ocr(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    data_uri = f"data:{mime_type};base64,{encoded}"

    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": data_uri},
        include_image_base64=False
    )

    return "\n\n".join(page.markdown or page.text or "" for page in response.pages)