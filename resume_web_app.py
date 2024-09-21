# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 10:45:29 2024

@author: user
"""

import streamlit as st
import pandas as pd

import plotly.express as px
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI

OPENAI_API_KEY= st.secrets["open_api_key"]
def get_response(text,user_question,OPENAI_API_KEY):
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    #st.write(chunks)
        
        # generating embedding
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # creating vector store - FAISS
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    match = vector_store.similarity_search(user_question)
    #st.write(match)

    #define the LLM
    llm = ChatOpenAI(
        openai_api_key = OPENAI_API_KEY,
        temperature = 0,
        max_tokens = 1000,
        model_name = "gpt-3.5-turbo"
    )

    #output results
    #chain -> take the question, get relevant document, pass it to the LLM, generate the output
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents = match, question = user_question)
    return response


st.title('Souvik Chattopadhyay')
st.markdown("<description>Lets walkthrough the profile of Souvik</description>",unsafe_allow_html=True)

st.sidebar.title('Select options for detailed view')
detail_check=st.sidebar.checkbox('Get Detailed Experience')

question = st.sidebar.text_input("Ask any sepcific question about Souvik")

resume_file='./CV_Souvik Chattopadhyay_9.pdf'
pdf_reader = PdfReader(resume_file)
text = ""
for page in pdf_reader.pages:
    text += page.extract_text()
if question:
    response=get_response(text,question,OPENAI_API_KEY)
    st.sidebar.write(response)
# print(text)

# detail_data=pd.read_csv('https://docs.google.com/spreadsheets/d/'+
#                          '1w9ygDJHd1e9g9LARlZu9nmWa-OUDpkMtKmwIXKsQY3g/export?format=csv&gid=0')
# if(detail_check):
#     st.dataframe(detail_data)
   
tabluar_check=st.checkbox('View Tabluar')

summary_data=pd.read_csv('https://docs.google.com/spreadsheets/d/'+
                         '1SGudeThfURf7LgVjiSVq2MlLMf17o8Yu1L8YHWgS5ms/export?format=csv&gid=366008444',
                          parse_dates=['Start Date','End Date'])
if(tabluar_check):
    st.write(summary_data)

exp_summary_graph=px.bar(data_frame=summary_data,x='Organization',y='Experience',
                         labels={'Experience':'Experience (in months)'},color='Organization')
st.plotly_chart(exp_summary_graph)

skill_data = pd.read_csv('https://docs.google.com/spreadsheets/d/'+
                         '1SGudeThfURf7LgVjiSVq2MlLMf17o8Yu1L8YHWgS5ms/export?format=csv&gid=0')
skill_summary_graph=px.bar(data_frame=skill_data,x='Skill',y='Experience',
                         labels={'Experience':'Experience (in years)'},color='Skill')
st.plotly_chart(skill_summary_graph)

education_data=pd.read_csv('https://docs.google.com/spreadsheets/d/'+
                         '1w9ygDJHd1e9g9LARlZu9nmWa-OUDpkMtKmwIXKsQY3g/export?format=csv&gid=1412439148')
st.header('Educational Details')

st.dataframe(education_data)
