from genai_content_generator import generate_content, generate_image, generate_image_sdxl
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

            En el campo respuesta_texto_corto genera un texto de menos de 280 caracteres incluyendo espacios.
            En el campo respuesta_extensa genera un texto menos de 1000 caracteres.
            En el campo respuesta_mail genera un texto de minimo 350 palabras en formato html para correo electronico con las siguientes secciones:
                un saludo, 
                una introducción del tema marcando en negritas los puntos importantes longitud de texto: minimo 50 palabras, 
                bullets explicando puntos importantes longitud de texto: minimo 200 palabras, 
                explicación mas detallada longitud de texto: minimo 100 palabras,
                una despedida.
            En el campo imagen_prompt genera un prompt en idioma inglés de menos de 512 caracteres incluyendo espacios para crear una imagen relacionada al tema y contexto, pero que no contenga:
                any text,
                any diagrams,
                any illegal or fraudulent activity,
                any violation the rights of others,
                any threaten, incite, promote, or actively encourage violence, terrorism, or other serious harm,
                any content or activity that promotes child sexual exploitation or abuse,
                any violation the security, integrity, or availability of any user, network, computer or communications system, software application, or network or computing device,
                any related to distribute, publish, send, or facilitate the sending of unsolicited mass email or other messages, promotions, advertising, or solicitations (or “spam”).
            
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
        #image_result = generate_image(imagen_prompt)
        image_result = generate_image_sdxl(imagen_prompt)
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