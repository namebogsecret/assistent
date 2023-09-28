import os
import requests
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
class OpenAIImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_image(self, prompt, n=1, size="1024x1024", response_format="url"):
        """
        Creates an image given a prompt using the OpenAI API.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": response_format
        }
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
        return response.json()

    def save_image_from_url(self, image_url, save_path):
        """
        Downloads an image from the given URL and saves it to the specified path.
        """
        response = requests.get(image_url)
        with open(save_path, 'wb') as file:
            file.write(response.content)



if __name__ == "__main__":
    # Example usage
    api_key = os.getenv("OPENAI_API_KEY")
    prompt = "A cute baby sea otter"
    generator = OpenAIImageGenerator(api_key)
    response = generator.create_image(prompt, n=2, size="1024x1024")

    # Process the response
    if 'data' in response and isinstance(response['data'], list):
        for idx, image_data in enumerate(response['data']):
            if 'url' in image_data:
                image_url = image_data['url']
                save_path = f"image_{idx}.jpg"  # Specify the desired save path and file name
                generator.save_image_from_url(image_url, save_path)
                print("Generated image saved:", save_path)
            elif 'b64' in image_data:
                # Process the base64-encoded image data as needed
                print("Generated image (base64):", image_data['b64'])
    else:
        print("Unexpected response format:", response)
