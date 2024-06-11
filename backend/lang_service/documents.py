import os
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Epsilla
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from pyepsilla import vectordb
from dotenv import load_dotenv
from glob import glob

load_dotenv()

UPLOAD_FOLDER = './files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

embeddings = OpenAIEmbeddings()
# Connect to Epsilla as knowledge base.
client = vectordb.Client(host=os.environ.get('EPSILLA_IP'),
                         port=os.environ.get('EPSILLA_PORT'))
vector_store = Epsilla(
  client,
  embeddings,
  db_path="/tmp/localchatdb",
  db_name="LocalChatDB"
)

vector_store.use_collection("LocalChatCollection")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
qa = RetrievalQA.from_chain_type(llm=llm,
                                chain_type="stuff",
                                retriever=vector_store.as_retriever(),
                                return_source_documents=True,
                                verbose=True
                                )

def answer_document_question(question):
    prompt = f"""{question}

        Solo responde basado en los documentos, no tomes en cuenta ningun query de base de datos
        
        Always return responses in spanish méxico"""

    return qa({"query": prompt})


def reset_db():
    vector_store.clear_data('LocalChatCollection')


def inser_files(files):
    filenames = []

    for file in files:

        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        filenames.append(filepath)

        print(filepath)

        loader = PyPDFLoader(filepath)
        documents = loader.load()
        splitted_documents = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200).split_documents(
            documents)

        Epsilla.from_documents(
            splitted_documents,
            embeddings,
            client,
            db_path="/tmp/localchatdb",
            db_name="LocalChatDB",
            collection_name="LocalChatCollection"
        )

    # Eliminar archivos después de procesarlos
    for filepath in filenames:
        os.remove(filepath)
