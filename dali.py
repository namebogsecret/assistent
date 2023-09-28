import os
import openai
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_image(prompt, n=1, size="1024x1024", response_format="url"):
    """
    Creates an image given a prompt using the OpenAI API.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=n,
            size=size,
            response_format=response_format
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
prompt = "A cute baby sea otter"
response = create_image(prompt, n=2, size="1024x1024")

# Process the response
if response is not None:
    print(response)
else:
    print("Image creation failed.")
