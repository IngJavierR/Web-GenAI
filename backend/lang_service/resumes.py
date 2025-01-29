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

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=IP_DB,
            port=DB_PORT
        )

        # Consulta SQL
        query = """
            SELECT 
                c.id AS consultor_id,
                c.nombre,
                c.apellido,
                c.fecha_nacimiento,
                c.email,
                c.telefono,
                c.direccion,
                c.fecha_ingreso,
                c.descripcion AS descripcion_consultor,

                el.id AS experiencia_id,
                el.empresa,
                el.puesto,
                el.fecha_inicio AS experiencia_fecha_inicio,
                el.fecha_fin AS experiencia_fecha_fin,
                el.descripcion AS experiencia_descripcion,

                a.id AS actividad_id,
                a.descripcion AS actividad_descripcion,

                ct.id AS conocimiento_id,
                ct.conocimiento,
                ct.nivel AS conocimiento_nivel,

                i.id AS idioma_id,
                i.idioma,
                i.nivel AS idioma_nivel,

                cert.id AS certificacion_id,
                cert.certificacion,
                cert.institucion AS certificacion_institucion,
                cert.fecha_obtencion,
                cert.fecha_expiracion,

                h.id AS herramienta_id,
                h.herramienta,
                h.nivel AS herramienta_nivel,

                e.id AS educacion_id,
                e.institucion AS educacion_institucion,
                e.titulo AS educacion_titulo,
                e.fecha_inicio AS educacion_fecha_inicio,
                e.fecha_fin AS educacion_fecha_fin

            FROM Consultores c
            LEFT JOIN Experiencia_Laboral el ON c.id = el.consultor_id
            LEFT JOIN Actividades a ON el.id = a.experiencia_id
            LEFT JOIN Conocimientos_Tecnicos ct ON c.id = ct.consultor_id
            LEFT JOIN Idiomas i ON c.id = i.consultor_id
            LEFT JOIN Certificaciones cert ON c.id = cert.consultor_id
            LEFT JOIN Herramientas h ON c.id = h.consultor_id
            LEFT JOIN Educacion e ON c.id = e.consultor_id
            ORDER BY c.id, el.id, a.id, ct.id, i.id, cert.id, h.id, e.id;
            """

        # Conexión a la base de datos
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            # Estructurar los datos por consultor
            consultores = {}

            for row in rows:
                consultor_id = row["consultor_id"]

                if consultor_id not in consultores:
                    consultores[consultor_id] = {
                        "id": consultor_id,
                        "nombre": row["nombre"],
                        "apellido": row["apellido"],
                        "fecha_nacimiento": row["fecha_nacimiento"],
                        "email": row["email"],
                        "telefono": row["telefono"],
                        "direccion": row["direccion"],
                        "fecha_ingreso": row["fecha_ingreso"],
                        "descripcion": row["descripcion_consultor"],
                        "experiencia": [],
                        "conocimientos": [],
                        "idiomas": [],
                        "certificaciones": [],
                        "herramientas": [],
                        "educacion": []
                    }

                # Experiencia laboral
                if row["experiencia_id"]:
                    experiencia = {
                        "id": row["experiencia_id"],
                        "empresa": row["empresa"],
                        "puesto": row["puesto"],
                        "fecha_inicio": row["experiencia_fecha_inicio"],
                        "fecha_fin": row["experiencia_fecha_fin"],
                        "descripcion": row["experiencia_descripcion"],
                        "actividades": []
                    }
                    if experiencia not in consultores[consultor_id]["experiencia"]:
                        consultores[consultor_id]["experiencia"].append(experiencia)

                # Actividades de cada experiencia
                if row["actividad_id"]:
                    actividad = {
                        "id": row["actividad_id"],
                        "descripcion": row["actividad_descripcion"]
                    }
                    if actividad not in experiencia["actividades"]:
                        experiencia["actividades"].append(actividad)

                # Conocimientos técnicos
                if row["conocimiento_id"]:
                    conocimiento = {
                        "id": row["conocimiento_id"],
                        "conocimiento": row["conocimiento"],
                        "nivel": row["conocimiento_nivel"]
                    }
                    if conocimiento not in consultores[consultor_id]["conocimientos"]:
                        consultores[consultor_id]["conocimientos"].append(conocimiento)

                # Idiomas
                if row["idioma_id"]:
                    idioma = {
                        "id": row["idioma_id"],
                        "idioma": row["idioma"],
                        "nivel": row["idioma_nivel"]
                    }
                    if idioma not in consultores[consultor_id]["idiomas"]:
                        consultores[consultor_id]["idiomas"].append(idioma)

                # Certificaciones
                if row["certificacion_id"]:
                    certificacion = {
                        "id": row["certificacion_id"],
                        "certificacion": row["certificacion"],
                        "institucion": row["certificacion_institucion"],
                        "fecha_obtencion": row["fecha_obtencion"],
                        "fecha_expiracion": row["fecha_expiracion"]
                    }
                    if certificacion not in consultores[consultor_id]["certificaciones"]:
                        consultores[consultor_id]["certificaciones"].append(certificacion)

                # Herramientas
                if row["herramienta_id"]:
                    herramienta = {
                        "id": row["herramienta_id"],
                        "herramienta": row["herramienta"],
                        "nivel": row["herramienta_nivel"]
                    }
                    if herramienta not in consultores[consultor_id]["herramientas"]:
                        consultores[consultor_id]["herramientas"].append(herramienta)

                # Educación
                if row["educacion_id"]:
                    educacion = {
                        "id": row["educacion_id"],
                        "institucion": row["educacion_institucion"],
                        "titulo": row["educacion_titulo"],
                        "fecha_inicio": row["educacion_fecha_inicio"],
                        "fecha_fin": row["educacion_fecha_fin"]
                    }
                    if educacion not in consultores[consultor_id]["educacion"]:
                        consultores[consultor_id]["educacion"].append(educacion)

            return list(consultores.values())

    except Exception as e:
        print('Error al insertar', e)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

    return []