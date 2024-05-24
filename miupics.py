%pip install rembg
import rembg
import json
import time
import base64
import requests
from rembg import remove
class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '09C4B8B6427542CBF80BDD74D493DEEA', '27B92ACCAF8ED0F87644593223E11A06')
    model_id = api.get_model()
    prompt = input("")
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)
    image_base64 = images[0]
    # Декодируем строку base64 в бинарные данные
    image_data = base64.b64decode(image_base64)
    # Открываем файл для записи бинарных данных изображения
    with open("image.jpg", "wb") as file:
        file.write(image_data)
from PIL import Image
input_path = 'image.jpg'
output_path = 'output_1.png'
input = Image.open(input_path)
output = remove(input)
output.save(output_path)
