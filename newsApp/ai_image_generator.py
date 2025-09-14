from django.conf import settings
import requests
import base64
from django.core.files.base import ContentFile

# -------------------- AI Image Generation --------------------
def AI_image_generation(news_obj):
    """
    Generates an AI image for a news article using Hugging Face API
    and saves it to the News object if it doesn't already have a file.
    Prints informative messages if image generation fails.
    """
    hf_key = settings.HUGGINGFACE_API_KEY
   

    HF_API_URL = "https://api-inference.huggingface.co/models/gsdf/Counterfeit-V2.5"
    headers = {"Authorization": f"Bearer {hf_key}"}

    heading_text = news_obj.heading
    body_text = news_obj.description or ""

    try:
        prompt = f"Realistic high-quality news photo for article: {heading_text}. {body_text[:200]}"
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=60
        )

        if response.status_code != 200:
            print(f"❌ Hugging Face API request failed for '{heading_text}' with status {response.status_code}: {response.text}")
            return

        data = response.json()

        # Check if image data exists
        image_base64 = None
        if isinstance(data, list) and len(data) > 0 and "generated_image" in data[0]:
            image_base64 = data[0]["generated_image"]
        elif isinstance(data, dict) and "image" in data:
            image_base64 = data["image"]

        if not image_base64:
            print(f"⚠️ Hugging Face API did not return an image for '{heading_text}'")
            return

        # Save image
        image_bytes = base64.b64decode(image_base64)
        filename = f"{heading_text[:50].replace(' ', '_')}.png"
        news_obj.file.save(filename, ContentFile(image_bytes), save=True)
        print(f"✅ AI image generated and saved for '{heading_text}'")

    except Exception as e:
        print(f"💥 AI image generation failed for '{heading_text}': {e}")
