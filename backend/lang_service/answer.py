import os
from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from dotenv import load_dotenv

load_dotenv()
# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://{os.environ.get('DBUSER')}:{os.environ.get('DBPASS')}@{os.environ.get('IPDB')}:5432/{os.environ.get('DATABASE')}",
)

# setup llm
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
# Setup the database chain
db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, use_query_checker=True, verbose=False)


def answer_question(question):
    prompt = f"""{question}
    
    Double check the Postgres query above for common mistakes, including:
     - Remembering to add `NULLS LAST` to an ORDER BY DESC clause
     - Handling case sensitivity, e.g. using ILIKE instead of LIKE
     - Ensuring the join columns are correct
     - Casting values to the appropriate type
    
    Rewrite the query here if there are any mistakes. If it looks good as it is, just reproduce the original query.
    Always return responses in spanish méxico"""

    return db_chain.invoke(prompt)