
import os
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image
import io

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the generative AI model
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Gemini API key not found. Please set it in the .env file.")



def generate_image(fabric_image, model_image, prompt, fabric_image_2=None):
    """
    Generates an image using the Gemini 1.5 Flash model.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        fabric_image_pil = PIL.Image.open(fabric_image)
        model_image_pil = PIL.Image.open(model_image)
        
        content = [prompt, fabric_image_pil, model_image_pil]
        
        if fabric_image_2:
            fabric_image_2_pil = PIL.Image.open(fabric_image_2)
            content.append(fabric_image_2_pil)

        response = model.generate_content(content)

        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    return io.BytesIO(image_data)

        if hasattr(response, 'text') and response.text:
            print(f"No image data in response. Response: {response.text}")
        else:
            print("No image data in response and no text either.")
        return None

    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        return None
