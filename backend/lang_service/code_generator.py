from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json

load_dotenv()
# setup llm
llm = ChatOpenAI(model="gpt-4o", temperature=0)


def code_suggestion(prompt, code):
    messages = [
        {"role": "system", "content": "Eres un desarrollador experto"},
        {"role": "user", "content": [
            {"type": "text", "text": f"""
                Ejecuta esta instrucción: {prompt} 

                Al código fuente: {code}

                Retorna solo el código fuente, sin explicaciones ni detalle alguno en formato json en una variable llamada: result.
            """}
        ]}
    ]

    ai_message = llm.invoke(messages)
    response = ai_message.content
    print('response', response)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    print('response2', response)

    return json.loads(response)

def code_explanation(code):
    messages = [
        {"role": "system", "content": "Eres un desarrollador experto"},
        {"role": "user", "content": [
            {"type": "text", "text": f"""
                Genera una explicación del comportamiento 

                Al código fuente: {code}

                Retorna solo la explicación en formato de texto con saltos de linea escapados dentro de un json en una variable llamada: result.
            """}
        ]}
    ]

    ai_message = llm.invoke(messages)
    response = ai_message.content
    print('response', response)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    print('response2', response)

    return json.loads(response)

def code_files_image_based(prompt, base64Frame):
    messages = [
        {"role": "system",
         "content": "Eres un desarrollador experto"},
        {"role": "user", "content": [
                {"type": "text", "text": f"""
                    Genera el código para esta instrucción: {prompt} 
                    
                    Analizando la siguiente imagen
    
                    Retorna todos los archivos necesarios para ejecutar la instrucción, sin explicación ni detalles dentro de un json en una variable llamada: result con un array con la siguiente estructura:
                    
                    filePath: contendrá la ruta y el nombre del archivo
                    fileContent: contendrá el contenido del archivo
                    
                """},
                {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{base64Frame}', "detail": "low"}}
            ],
        }
    ]

    ai_message = llm.invoke(messages)
    response = ai_message.content
    print('response', response)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    print('response2', response)

    return json.loads(response)


def code_files(prompt, code):
    messages = [
        {"role": "system",
         "content": "Eres un desarrollador experto"},
        {"role": "user", "content": [
            {"type": "text", "text": f"""
                    Ejecuta esta instrucción: {prompt} 

                    Al código fuente: {code}

                    Retorna todos los archivos necesarios para ejecutar la instrucción, sin explicación ni detalles dentro de un json en una variable llamada: result con un array con la siguiente estructura:

                    filePath: contendrá el nombre del archivo
                    fileContent: contendrá el contenido del archivo

                """}
        ],
         }
    ]

    ai_message = llm.invoke(messages)
    response = ai_message.content
    print('response', response)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    print('response2', response)

    return json.loads(response)