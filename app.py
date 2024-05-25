import streamlit as st
import pandas as pd
import numpy as np
import rembg
import json
import time
import base64
import requests
from rembg import remove
from PIL import Image

st.title("Добро пожаловать в нейросеть MiuPics")
st.write("Первая нейросеть по генерированию изображений для веб-дизайна.")
st.write("Здесь вы сможете сгенерировать необходимое изображение, предварительно выбрав желаемый тип, а также стиль. Просто введите ваш запрос в окно ввода промпта и нажмите на кнопку 'Сгенерировать'. Для того, чтобы вырезать фон, нажмите на кнопку 'Вырезать фон'.")
st.write("Для того, чтобы вырезать фон, нажмите на кнопку 'Вырезать фон'.")

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

    def generate(self, prompt, model, images=1, width=1024, height=1024, style=3):
        styles = ["KANDINSKY", "UHD", "ANIME", "DEFAULT"]
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "style":styles[style],
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

selected_type= st.radio('Выберите тип изображения:', ["Стикер", "Иконка", "Фотография", "Вектор", "Макет сайта", "Шаблон"])
if selected_type == "Иконка":
    icon_type = st.selectbox('Тип иконки:', ['простые элементы', 'информационная', 'линейная', 'иллюстрация', "объемная"])
    selected_type = selected_type + icon_type
elif selected_type == "Стикер":
    stiker_type = st.selectbox('Тип стикера:', ['без фона','линейный','простые элементы','наклейка','графичный'])
    selected_type = selected_type + stiker_type

write_prompt = st.text_input(label='Введите промпт')
final_prompt = write_prompt + selected_type

selected_style = st.radio('Выберите стиль изображения:', ['Абстракционизм', 'Ультра HD', 'Аниме', 'Без стиля'])
if selected_style == 'Абстракционизм':
    img_style = 0
elif selected_style == 'Ультра HD':
    img_style = 1
elif selected_style == 'Аниме':
    img_style = 2
else:
    img_style = 3

if st.checkbox('Выбрать цвет'):
    color = st.text_input('Напишите основные цвета генерируемого изображения')
    final_prompt = final_prompt + ', основные цвета: ' + color
def result():
    if __name__ == '__main__':
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '09C4B8B6427542CBF80BDD74D493DEEA', '27B92ACCAF8ED0F87644593223E11A06')
        model_id = api.get_model()
        prompt = final_prompt
        if prompt is None:
            print('Введите промпт')
        else:
            uuid = api.generate(prompt, model_id, style=img_style)
            images = api.check_generation(uuid)
            image_base64 = images[0]
            # Декодируем строку base64 в бинарные данные
            image_data = base64.b64decode(image_base64)
            # Открываем файл для записи бинарных данных изображения
            with open("image.jpg", "wb") as file:
                return file.write(image_data)

def remove_bg():
    input_path = 'image.jpg'
    output_path = 'output_1.png'
    input = Image.open(input_path)
    output = remove(input)
    return output.save(output_path)


if st.button('Сгенерировать'):
    with st.spinner(text='Подождите, генерируем'):
        time.sleep(3)
        result()
        image = st.image('image.jpg')
        st.success('Готово!')
        with open('image.jpg', 'rb') as f:
            st.download_button('Скачать', f, file_name='image.jpg')
elif st.button('Показать сгенерированное изображение'):
    st.image('image.jpg')
if st.button('Вырезать фон'):
        with st.spinner(text='Подождите, генерируем'):
            time.sleep(3)
            remove_bg()
            st.success('Готово!')
            st.image('output_1.png')