from genai_content_generator import generate_content, generate_image
from x_connector import send_tweet
from fb_connector import send_post
from documents import get_content_from_document


def post_content(tweet_text, image_name=None, type='twitter'):
    image_path = f"images/{image_name}.png"
    if type == 'twitter':
        send_tweet(tweet_text, image_path)
    if type == 'facebook':
        send_post(tweet_text, image_path)


def get_preview_content(query, include_image=False, include_context=False):
    context = ''

    if include_context:
        context = get_content_from_document(query)
        print('Context: ', context)

    prompt = f"""
        
            Buscar datos importantes para elaborar contenido sobre el siguiente tema, no te salgas del contexto que estoy agregando
            Tema: {query}
            Contexto: {context}

            En el campo respuesta_texto_corto genera un texto de menos de 280 caracteres incluyendo espacios
            En el campo respuesta_extensa genera un texto menos de 1000 caracteres
            En el campo respuesta_mail genera un texto en formato html para correo electronico, con un saludo, marcando en negritas los puntos importantes, bullets y explicación y una despedida
            En el campo imagen_prompt genera un prompt en idioma inglés de menos de 512 caracteres incluyendo espacios para crear una imagen, valida que no provoque conflictos con el AWS Responsible AI Policy
            
            Retorna la respuesta en un json válido que no tenga limite de caracteres y que este completo con la siguiente estructura

            "respuesta_texto_corto":
            "respuesta_extensa":
            "respuesta_mail":
            "imagen_prompt":
            
            Asegurate de quitar los caracteres ```json y ``` de la respuesta
            """

    image_result = None
    tweet_content = ''
    post_content = ''
    respuesta_mail = ''

    content = generate_content(prompt)

    tweet_content = content['respuesta_texto_corto']
    post_content = content['respuesta_extensa']
    respuesta_mail = content['respuesta_mail']
    imagen_prompt = content['imagen_prompt']

    print('include_image', include_image)
    if include_image:
        image_result = generate_image(imagen_prompt)
        return {
            'tweet_content': tweet_content,
            'post_content': post_content,
            'email_content': respuesta_mail,
            'image_base64': image_result['image_base64'],
            'image_name': image_result['image_name']
        }
    else:
        return {
            'tweet_content': tweet_content,
            'post_content': post_content,
            'email_content': respuesta_mail,
        }

def upload_document(tweet_text, image_name=None, type='twitter'):
    if type == 'twitter':
        image_path = f"images/{image_name}.png"
        send_tweet(tweet_text, image_path)