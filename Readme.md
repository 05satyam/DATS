# Working
    -    This is an implementation of utilizing the text completion and summarization capabilities of LLM's where user can use their personal data and get insights on the same.
    -    By uploading the data using the path of local system folder which containes all files in CSV and then running queries lile "Provide me insights on my job applications                   in 2024 march... etc"
    -    It is a basic implementation, created to understand langchain framework and a small tool for myself.
# Language
    -   Python-3.10.0
# Framerworks:
    -   Langchain - OpenAIEmbeddings, ChatOpenAI
        -   pip install -U langchain-community
    -   Flask
        -   pip install Flask

# DB
    -   DuckDB : feature-rich SQL dialect complemented with deep integrations into client APIs
        -   pip install duckdb==0.10.0

# Libraries 
    -   from langchain_core.documents import Document
    -   from langchain_core.prompts import PromptTemplate
    -   from openai import OpenAI
    -   from langchain.text_splitter import RecursiveCharacterTextSplitter
    -   from langchain.chat_models import ChatOpenAI
    -   from langchain.vectorstores import FAISS
    -   from langchain.embeddings import OpenAIEmbeddings
    -   from langchain.chains.summarize import load_summarize_chain
    -   import numpy as np
    -   from sklearn.cluster import KMeans

# DataLoad to application:
    -   Submit a path to your folder consisting csv's using index.html after running the application
    -   In db.py data is loaded from csv's
        -   Name of csv files are considered as table names
        -   All non empty rows are omitted, any csv with instructions in top rows are omitted
        -   Total number of columns are calculated first to remove rows with columns less than total number of columns
        -   All table names are pre_processed with replacing spaces, - with under_scores
        -   Data is loaded in duckdb in your root folder-path can be changed
    
# API's
    -   /load-data
        -   To load data in the duckdb , give path to folder consisting all csv's with data in them with proper rows and column
    -   /search
        -   Takes user query to generate insights - data loaded from saved duckdb file and then fed to the llm

# OpenAI Model
    -   client = OpenAI(api_key='openai-api-key')
        -   change to your open-api-key
        -   OpenAI config - change as per requirements
            -   temperature=.25,
            -   openai_api_key="openai-api-key",
            -   max_tokens=1000,
            -   model='gpt-4',
            -   request_timeout=180
    -   Strategy to get insights:
        -   User data can be long, so break the data in to chunks using 'RecursiveCharacterTextSplitter' from langchain
        -   Convert to the documents where #ofdocument==#ofchunks
        
        -   SQL query on all tables using LIKE operator for each word submitted my user in user_query (db.py)
            -   Need to optimize this as it is taking long time and quering is not that good

        -   Get data from saved data and feed it to openai by creating embeddings
        -   Create Prompt using langchain 'PromptTemplate'
        -   Using 'load_summarize_chain' following 'map_reduce' strategy to generate summary
        -   In last, fed each document to openai using reduce_chain.run so as to avoid execeeding token limit


# Contribution
    -   Create a repo of this repository, add your changes and submit a pull request.
    -   Want to make it more general and open to everyone, where anyone can submit their own OpenAI key and path to their data-csvs folder and generate insoghts
    -   As it involves users personal data so, anyone can download and run it as personal assistant.
