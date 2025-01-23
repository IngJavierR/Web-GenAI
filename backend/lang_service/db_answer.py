import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

load_dotenv()
# setup llm
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)

def answer_db_question(question, catalog):

    db = setup_database(catalog)
    db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, use_query_checker=True, verbose=False)

    prompt = f"""{question}
    
    Double check the Postgres query above for common mistakes, including:
     - Remembering to add `NULLS LAST` to an ORDER BY DESC clause
     - Handling case sensitivity, e.g. using ILIKE instead of LIKE
     - Ensuring the join columns are correct
     - Casting values to the appropriate type
    
    Rewrite the query here if there are any mistakes. If it looks good as it is, just reproduce the original query.
    Always return responses in spanish méxico"""

    return db_chain.invoke(prompt)


def recipe_product_question(question, catalog):
    db = setup_database(catalog)
    db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, use_query_checker=True, verbose=False)

    prompt = f"""{question}

    Double check the Postgres query above for common mistakes, including:
     - Remembering to add `NULLS LAST` to an ORDER BY DESC clause
     - Handling case sensitivity, e.g. using ILIKE instead of LIKE
     - Ensuring the join columns are correct
     - Casting values to the appropriate type

    Rewrite the query here if there are any mistakes. If it looks good as it is, just reproduce the original query.
    Always return responses in spanish méxico
    """

    return db_chain.invoke(prompt)


def setup_database(catalog):
    DB_USER, DB_PASS, DB_PORT, IP_DB, DATABASE_NAME = database_origin(catalog)
    # Setup database
    return SQLDatabase.from_uri(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{IP_DB}:{DB_PORT}/{DATABASE_NAME}",
    )


def database_origin(catalog):
    DB_USER = ''
    DB_PASS = ''
    DB_PORT = ''
    IP_DB = ''
    DATABASE_NAME = ''

    if catalog == 'itsm':
        DB_USER = os.environ.get('DBUSER')
        DB_PASS = os.environ.get('DBPASS')
        DB_PORT = os.environ.get('DBPORT')
        IP_DB = os.environ.get('IPDB')
        DATABASE_NAME = os.environ.get('DATABASE')

    elif catalog == 'retail':
        DB_USER = os.environ.get('DBUSER')
        DB_PASS = os.environ.get('DBPASS')
        DB_PORT = os.environ.get('DBPORT')
        IP_DB = os.environ.get('IPDB')
        DATABASE_NAME = os.environ.get('DATABASE_PRODUCTS')

    return DB_USER, DB_PASS, DB_PORT, IP_DB, DATABASE_NAME