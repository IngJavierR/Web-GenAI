import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAI
import psycopg2
from psycopg2.extras import RealDictCursor
from db_answer import setup_database, database_origin

load_dotenv()

UPLOAD_FOLDER = './resumes'
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def analize_resumes(files, catalog):
    db = setup_database(catalog)

    filenames = []
    for file in files:

        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        filenames.append(filepath)
        print(filepath)

        response = analize_file(filepath, db.get_context())
        response = response.replace("```sql", "")
        response = response.replace("```", "")
        response = response.replace("\\'", "")
        queries = response.split('\n;')

        for query in queries:
            if query:
                insert_db(catalog, query)
                time.sleep(1)

    # Eliminar archivos después de procesarlos
    for filepath in filenames:
        os.remove(filepath)


def analize_file(file, db_schema):
    loader = PyPDFLoader(file)

    document_fragments = loader.load()

    content = ""
    for document in document_fragments:
        content += document.page_content

    if content == "":
        return ""
    else:
        messages = [
            {"role": "system", "content": "Eres experto en Recursos humanos y bases de datos postgresql "},
            {"role": "user", "content": [
                {"type": "text", "text": f"""
                        Tomando en cuenta el siguiente esquema de base de datos:
                        Schema: {db_schema}

                        Analiza el siguiente archivo:
                        Archivo: {content}

                        Retorna un array de sentencias INSERT en orden correcto para almacenar la información requerida 
                        por el Schema no expliques el resultado, procedimiento ni recomendaciones.

                        Todas las tablas cuenta con el ID como INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY

                        Double check the Postgres query above for common mistakes, including: 
                         - Confirm constraints and keys in every sentence and previews inserts
                         - Handling case sensitivity, e.g. using ILIKE instead of LIKE
                         - Ensuring the join columns are correct
                         - Casting values to the appropriate type
                         - Ensuring not violate not-null constraint
                         - Ignore inserts if table not exists
                         - Escape invalid characters like quotes or double quotes and others

                        Rewrite the query here if there are any mistakes. If it looks good as it is, just reproduce the original query.
                    """}
            ]}
        ]

        ai_message = llm.invoke(messages)
        return ai_message.content

def insert_db(catalog, sentence):
    DB_USER, DB_PASS, DB_PORT, IP_DB, DATABASE_NAME = database_origin(catalog)
    conn = None
    cur = None
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=IP_DB,
            port=DB_PORT
        )

        # Crear un cursor
        cur = conn.cursor()
        # Execute sentence
        cur.execute(sentence)
        # Cerrar comunicación con la base de datos
        conn.commit()
    except Exception as e:
        print('Sentence', sentence)
        print('Error al insertar', e)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


def get_resumes_db(catalog):
    DB_USER, DB_PASS, DB_PORT, IP_DB, DATABASE_NAME = database_origin(catalog)
    conn = None
    cur = None

    # Diccionario para almacenar los resultados de cada tabla
    all_records = {}
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=IP_DB,
            port=DB_PORT
        )

        # Lista de tablas en la estructura proporcionada
        tables = [
            "Consultores",
            "Experiencia_Laboral",
            "Actividades",
            "Conocimientos_Tecnicos",
            "Idiomas",
            "Certificaciones",
            "Herramientas",
            "Educacion",
            "Niveles_Conocimiento",
            "Niveles_Idiomas"
        ]

        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                for table in tables:
                    # Construir y ejecutar la consulta SELECT
                    query = f"SELECT * FROM {table}"
                    cursor.execute(query)

                    # Recuperar los registros como una lista de diccionarios
                    records = cursor.fetchall()

                    # Agregar los registros al diccionario principal
                    all_records[table] = records

    except Exception as e:
        print('Error al insertar', e)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

    return all_records