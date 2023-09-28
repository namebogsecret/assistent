import requests
import json
from time import sleep
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
class LeonardoService:
    def __init__(self, api_key, base_url="https://cloud.leonardo.ai/api/rest/v1/generations"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

    def generate(self, prompt="little cat", negative_prompt = "", iterations=60, size=512, model_id = "cd2b2a15-9760-4174-a5ff-4d2925057376", style = None, version = "v2"):
        url = self.base_url
        payload = {
            "prompt": prompt,
            "modelId": model_id,
            "width": size,
            "height": size,
            "negative_prompt": negative_prompt,
            "sd_version": version, #"v1_5"
            "num_images": 1,
            "num_inference_steps": int(iterations),
            "guidance_scale": 7,
            "presetStyle": style,
            "tiling": False,
            "public": False,
            "promptMagic": True
        }

        response = requests.post(url, json=payload, headers=self.headers).text
        # Проверяем, является ли ответ валидным JSON
        try:
            response_dict = json.loads(response)
        except json.JSONDecodeError:
            print('Response is not valid JSON.')
            return None

        # Проверяем, является ли ответ словарем
        if not isinstance(response_dict, dict):
            print('Response is not a dictionary.')
            return None

        # Проверяем, содержит ли словарь ключ 'sdGenerationJob'
        if 'sdGenerationJob' not in response_dict:
            print('Response does not contain "sdGenerationJob".')
            return None

        # Проверяем, является ли значение 'sdGenerationJob' словарем
        if not isinstance(response_dict['sdGenerationJob'], dict):
            print('Value of "sdGenerationJob" is not a dictionary.')
            return None

        # Проверяем, содержит ли словарь 'sdGenerationJob' ключ 'generationId'
        if 'generationId' not in response_dict['sdGenerationJob']:
            print('Dictionary "sdGenerationJob" does not contain "generationId".')
            return None

        # Проверяем, является ли 'generationId' строкой
        generation_id = response_dict['sdGenerationJob']['generationId']
        if not isinstance(generation_id, str):
            print('Generation ID is not a string.')
            return None

        # Если все проверки пройдены, выводим 'generationId'
        print(f'Generation ID is: {generation_id}')
        save_path = self.fetch_image(generation_id)
        return save_path


    def fetch_image(self, image_id):
        url = f"{self.base_url}/{image_id}"

        status = ""
        max_retries = 30
        retries = 0
        response = None

        while status != "COMPLETE" and retries < max_retries:
            response = requests.get(url, headers=self.headers)
            response_dict = json.loads(response.text)
            status = response_dict.get('generations_by_pk', {}).get('status', "")
            retries += 1
            sleep(2)  # sleep for 2 seconds

        if response is None:
            return None
        response = response.text

        
        try:
            response_dict = json.loads(response)
        except json.JSONDecodeError:
            print('Response is not valid JSON.')
            return None

        # Проверка наличия ключа 'generations_by_pk' и 'generated_images'
        if 'generations_by_pk' not in response_dict or 'generated_images' not in response_dict['generations_by_pk']:
            print('Response does not contain "generations_by_pk" or "generated_images".')
            return None

        # Проверка наличия элементов в списке 'generated_images'
        if len(response_dict['generations_by_pk']['generated_images']) == 0:
            print('List "generated_images" is empty.')
            return None

        # Проверка первого элемента списка 'generated_images'
        first_image = response_dict['generations_by_pk']['generated_images'][0]
        if 'url' not in first_image or 'nsfw' not in first_image:
            print('First image does not contain "url" or "nsfw".')
            return None
        
        # Если все проверки пройдены, выводим url
        print(f'URL is: {first_image["url"]}')
        image_url = first_image['url']
        save_path = f"image_{image_id}.jpg"  # Specify the desired save path and file name
        response = requests.get(image_url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("Generated image saved:", save_path)
        
        # Проверка значения 'nsfw'
        if first_image['nsfw'] is not False:
            print('Value of "nsfw" is not False.')
            return None


        return save_path

def im_3(img, leonardo_service,prompt="elephant on a horse", model_id="6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", style="LEONARDO", version = "v2"):
    im = leonardo_service.generate(prompt=prompt, model_id=model_id, style=style, version=version)
    if im is not    None:
        img.append(im)


if __name__ == "__main__":
    your_api_key = "2abf2dfa-8734-490b-aa0f-619502bf4b1e"
    leonardo_service = LeonardoService(api_key=your_api_key)
    input = input("Enter prompt: ")
    """img = leonardo_service.generate(prompt=input)
    # Открываем изображение
    if img is None:
        exit()
    from PIL import Image
    img = Image.open(img)# Отображаем изображение
    img.show()"""
    img = []
    im_3(img, leonardo_service,input, model_id="6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", style="LEONARDO",version="v1_5")
    im_3(img, leonardo_service,input, model_id="6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",version="v1_5") #
    im_3(img, leonardo_service,input, model_id="cd2b2a15-9760-4174-a5ff-4d2925057376", style="LEONARDO",version="v1_5")
    im_3(img, leonardo_service,input, model_id="cd2b2a15-9760-4174-a5ff-4d2925057376",version="v1_5")
    im_3(img, leonardo_service,input, model_id="291be633-cb24-434f-898f-e662799936ad", style="LEONARDO",version="v1_5")
    im_3(img, leonardo_service,input, model_id="291be633-cb24-434f-898f-e662799936ad",version="v1_5")
    im_3(img, leonardo_service,input, model_id="6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", style="LEONARDO") 
    im_3(img, leonardo_service,input, model_id="6bef9f1b-29cb-40c7-b9df-32b51c1f67d3")
    im_3(img, leonardo_service,input, model_id="cd2b2a15-9760-4174-a5ff-4d2925057376", style="LEONARDO")
    im_3(img, leonardo_service,input, model_id="cd2b2a15-9760-4174-a5ff-4d2925057376")
    im_3(img, leonardo_service,input, model_id="291be633-cb24-434f-898f-e662799936ad", style="LEONARDO")#
    im_3(img, leonardo_service,input, model_id="291be633-cb24-434f-898f-e662799936ad")
    from PIL import Image
    for im in img:
        if im is None:
            continue
        
        img = Image.open(im)
        # Отображаем изображение
        img.show()
    