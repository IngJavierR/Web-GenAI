import boto3
import json
from langchain_community.llms import Bedrock
import base64

session = boto3.Session(profile_name='genai-admin')
bedrock_runtime = session.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

def generate_image(content):
    prompt = f"""
        Genera una imagen que pueda representar de la mejor forma el siguente contenido
        Contenido: {content}
        """
    body = json.dumps(
        {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,  # Required
                #"negativeText": "<text>"  # Optional
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,  # Range: 1 to 5
                "quality": "premium",  # Options: standard or premium
                "height": 768,  # Supported height list in the docs
                "width": 1280,  # Supported width list in the docs
                "cfgScale": 7.5,  # Range: 1.0 (exclusive) to 10.0
                "seed": 42  # Range: 0 to 214783647
            }
        }
    )
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId="amazon.titan-image-generator-v1",
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response["body"].read())
    base64_image_data = response_body["images"][0]

    image = base64.b64decode(base64_image_data, validate=True)
    image_name = 'generated_image'
    image_path = f"images/{image_name}.png"
    with open(image_path, 'wb') as image_file:
        image_file.write(image)

    print('Imagen generada')
    return {
        'image_name': image_name,
        'image_base64': base64_image_data
    }

def generate_content(prompt):
    print('Generating content')
    model_kwargs_titan = {"temperature": 0.5}

    titan_llm = Bedrock(
        model_id="anthropic.claude-instant-v1",
        client=bedrock_runtime,
        credentials_profile_name='genai-admin',
        model_kwargs=model_kwargs_titan
    )

    response = titan_llm.invoke(prompt)
    response = response.replace("```json", "")
    response = response.replace("```", "")
    print('Response Content',response)
    response_json = json.loads(response)

    return response_json
