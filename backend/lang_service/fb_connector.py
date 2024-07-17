import os
from dotenv import load_dotenv
import requests

load_dotenv()
# Tu token de acceso de Facebook
access_token = os.environ.get('FB_ACCESS_TOKEN')
# Tu ID de página de Facebook
page_id = os.environ.get('FB_PAGE_ID')

# URL de la API de Facebook para subir la foto
upload_url = f'https://graph.facebook.com/v20.0/{page_id}/photos'


def send_post(text, image_path=None):
    # Datos de la imagen para la solicitud de subida
    image_data = {
        'access_token': access_token,
        'message': text
    }

    # Subir la imagen
    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        response = requests.post(upload_url, data=image_data, files=files)
        if response.status_code != 200:
            print(f"Error al subir la imagen: {response.status_code}")
            print(response.text)
            exit()

    # Extraer el ID de la foto de la respuesta
    response_data = response.json()
    photo_id = response_data['id']

    # URL de la API de Facebook para crear una publicación
    post_url = f'https://graph.facebook.com/v12.0/{page_id}/feed'

    # Datos del post
    post_data = {
        'access_token': access_token,
        'message': text,
        'object_attachment': photo_id
    }

    # Realizar la solicitud para publicar el post
    response = requests.post(post_url, data=post_data)

    # Verificar el resultado
    if response.status_code == 200:
        print("Post con imagen publicado exitosamente.")
    else:
        print(f"Error al publicar el post: {response.status_code}")
        print(response.text)
