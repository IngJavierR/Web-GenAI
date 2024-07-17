import os
import boto3
from langchain_community.embeddings import BedrockEmbeddings, OpenAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from glob import glob
from langchain.vectorstores import Epsilla
from pyepsilla import vectordb
from dotenv import load_dotenv

load_dotenv()
UPLOAD_FOLDER = './files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set LLM and embeddings
session = boto3.Session(profile_name='genai-admin')

bedrock_runtime = session.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

bedrock_embeddings = BedrockEmbeddings(
    client=bedrock_runtime,
    model_id="amazon.titan-embed-text-v1"
)

openai_embeddings = OpenAIEmbeddings()

client = vectordb.Client(host=os.environ.get('EPSILLA_IP'),
                         port=os.environ.get('EPSILLA_PORT'))


def url_loader(urls: []):
    loader = UnstructuredURLLoader(urls=urls)
    splitted_documents = splitter_loaders(loader)
    embeddings_store(splitted_documents)


def docs_loader(file):
    split_document = None

    if file.endswith('.pdf'):
        loader = PyPDFLoader(file)
        split_document = splitter_loaders(loader)

    return split_document


def splitter_loaders(loader):
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200)
    docs = loader.load()
    return text_splitter.split_documents(docs)


def embeddings_store(splitted_documents, catalog):
    embedding_type, db_path, db_name, collection_name = document_store_type(catalog)
    embedding = openai_embeddings if type == 'openai' else bedrock_embeddings

    Epsilla.from_documents(
        splitted_documents,
        embedding,
        client,
        db_path=db_path,
        db_name=db_name,
        collection_name=collection_name
    )


def get_retriever(catalog):
    embedding_type, db_path, db_name, collection_name = document_store_type(catalog)

    embedding = openai_embeddings if embedding_type == "openai" else bedrock_embeddings

    vector_store = Epsilla(
        client,
        embedding,
        db_path=db_path,
        db_name=db_name
    )
    vector_store.use_collection(collection_name)

    return vector_store

def delete_retriever(catalog):
    embedding_type, db_path, db_name, collection_name = document_store_type(catalog)
    vector_store = get_retriever(catalog)
    vector_store.clear_data(collection_name)

def document_store_type(catalog):
    embedding_type = ''
    db_path = ''
    db_name = ''
    collection_name = ''

    if catalog == 'chatbot':
        embedding_type = 'openai'
        db_path = '/tmp/localchatdb'
        db_name = 'LocalChatDB'
        collection_name = 'ChatbotKnowledgeBase'

    elif catalog == 'contentmanager':
        embedding_type = 'bedrock'
        db_path = '/tmp/localcontentdb'
        db_name = 'LocalContentDB'
        collection_name = 'ContentKnowledgeBase'

    return embedding_type, db_path, db_name, collection_name