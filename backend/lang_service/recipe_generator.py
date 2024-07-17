from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json
from db_answer import recipe_product_question

load_dotenv()
# setup llm
llm = ChatOpenAI(model="gpt-4o", temperature=0)


def recipe_generator(query):
    recipe = generate_recipe(query)
    urls = get_urls_market(recipe['prompt_ingredients'])

    return {
        'recipe_name': recipe['recipe_name'],
        'recipes': recipe['recipes'],
        'ingredients': recipe['ingredients'],
        'urls': urls['result']
    }


def get_urls_market(prompt_ingredients):
    prompt = f"""
        Retorna una lista de los siguientes productos con sus urls y su precio
        {prompt_ingredients}
        El resultado debe estar en formato HTML y las URLs como elementos link HTML
        """
    urls = recipe_product_question(prompt, "retail")
    print('URL', urls['result'])
    return urls

def generate_recipe(query):

    messages = [
        {"role": "system", "content": "Eres un experto cocinero"},
        {"role": "user", "content": [
            {"type": "text", "text": f"""
                Genera una receta de cocina con el siguiente requerimiento, puedes agregar otros ingredientes
                
                requerimiento: {query}
                
                Retorna la respuesta en un json válido con la siguiente estructura:
                
                recipe_name:
                recipes:
                ingredients:
                prompt_ingredients:

                recipe_name tendrá el nombre de la receta
                recipes tendrá los pasos en formato de lista para elaborar la receta 
                ingredients tendrá un listado de ingredientes
                query_ingredients contendra una lista separada por comas con el nombre de los ingredientes que no 
                estan en el requerimiento
            """}
        ]}
    ]

    ai_message = llm.invoke(messages)
    response = ai_message.content
    print('response', response)
    response = response.replace("```json", "")
    response = response.replace("```", "")

    return json.loads(response)

