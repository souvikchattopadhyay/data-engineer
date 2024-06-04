import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
# from langchain.chains import SQLDatabaseSequentialChain
from langchain_experimental.sql  import SQLDatabaseChain

# db connection
host = 'localhost'
port = '3306'
username = 'root'
password = 'root1234'
database_schema = 'datadb'
mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"


db = SQLDatabase.from_uri(mysql_uri)

#create llm
OPENAI_API_KEY= st.secrets["open_api_key"]
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

#create chain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
#run

question = st.text_input("Ask your question")
# PROMPT = f""" 
# Given an input question, first create a syntactically correct postgresql query to run,  
# then look at the results of the query and return the answer.  
# The question: {question}
# """
 
# use db_chain.run(question) instead if you don't have a prompt
result = db_chain.invoke(question)
st.write(result.get("result"))
