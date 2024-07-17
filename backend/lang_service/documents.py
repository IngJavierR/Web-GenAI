import os
from langchain.chat_models import ChatOpenAI, BedrockChat
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import boto3
from retrieve_knowledge import docs_loader, embeddings_store, get_retriever, delete_retriever

load_dotenv()

UPLOAD_FOLDER = './files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set LLM and embeddings
session = boto3.Session(profile_name='genai-admin')

bedrock_runtime = session.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)
model_kwargs =  {
    "max_tokens": 2048,
    "temperature": 0.0,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": ["\n\nHuman"],
}

model_id = "anthropic.claude-instant-v1"

llm_bedrock = BedrockChat(
    client=bedrock_runtime,
    model_id=model_id,
    model_kwargs=model_kwargs
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def answer_chatbot_question(question):
    vector_store = get_retriever("chatbot")

    qa = RetrievalQA.from_chain_type(llm=llm,
                                     chain_type="stuff",
                                     retriever=vector_store.as_retriever(),
                                     return_source_documents=True,
                                     verbose=True
                                     )
    prompt = f"""{question}

        Solo responde basado en los documentos, no tomes en cuenta ningun query de base de datos
        
        Always return responses in spanish méxico"""

    return qa({"query": prompt})


def get_content_from_document(topic):
    vector_store = get_retriever("contentmanager")

    qa = RetrievalQA.from_chain_type(llm=llm_bedrock,
                                     chain_type="stuff",
                                     retriever=vector_store.as_retriever(),
                                     return_source_documents=True,
                                     verbose=True
                                     )
    prompt = f"""{topic}

        Solo responde basado en los documentos, no tomes en cuenta ningun query de base de datos

        Always return responses in spanish méxico"""

    return qa({"query": prompt})


def reset_db(catalog):
    delete_retriever(catalog)


def insert_files(files, catalog):

    filenames = []
    for file in files:

        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        filenames.append(filepath)
        print(filepath)

        split_document = docs_loader(filepath)
        embeddings_store(split_document, catalog)

    # Eliminar archivos después de procesarlos
    for filepath in filenames:
        os.remove(filepath)

