# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 10:45:29 2024

@author: user
"""

import streamlit as st
import pandas as pd

import plotly.express as px

st.title('Souvik Chattopadhyay')
st.markdown("<description>Lets walkthrough the profile of Souvik</description>",unsafe_allow_html=True)

st.sidebar.title('Select options for detailed view')
detail_check=st.sidebar.checkbox('Get Detailed Experience')

detail_data=pd.read_csv('https://docs.google.com/spreadsheets/d/'+
                         '1w9ygDJHd1e9g9LARlZu9nmWa-OUDpkMtKmwIXKsQY3g/export?format=csv&gid=0')
if(detail_check):
    st.dataframe(detail_data)
   
tabluar_check=st.checkbox('View Tabluar')

summary_data=pd.read_csv('https://docs.google.com/spreadsheets/d/'+
                         '1w9ygDJHd1e9g9LARlZu9nmWa-OUDpkMtKmwIXKsQY3g/export?format=csv&gid=1508555704',
                          parse_dates=['Start Date','End Date'])
if(tabluar_check):
    st.write(summary_data)

exp_summary_graph=px.bar(data_frame=summary_data,x='Organization',y='Experience',
                         labels={'Experience':'Experience (in months)'},color='Organization')
st.plotly_chart(exp_summary_graph)

skill_data = pd.read_csv('https://docs.google.com/spreadsheets/d/'+
                         '1w9ygDJHd1e9g9LARlZu9nmWa-OUDpkMtKmwIXKsQY3g/export?format=csv&gid=1094379956')
skill_summary_graph=px.bar(data_frame=skill_data,x='Skill',y='Experience',
                         labels={'Experience':'Experience (in years)'},color='Skill')
st.plotly_chart(skill_summary_graph)

education_data=pd.read_csv('https://docs.google.com/spreadsheets/d/'+
                         '1w9ygDJHd1e9g9LARlZu9nmWa-OUDpkMtKmwIXKsQY3g/export?format=csv&gid=1412439148')
st.header('Educational Details')

st.dataframe(education_data)