from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
import numpy as np
from sklearn.cluster import KMeans

api_key='api_key'
client = OpenAI(api_key=api_key)
model_type='gpt-4'

def llm(text, user_query):
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=3000,
                                                   chunk_overlap=1000)
    docs = text_splitter.create_documents([text])
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectors = embeddings.embed_documents([x.page_content for x in docs])
    num_clusters = len(docs)
    closest_indices = []

    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)

    # Loop through the number of clusters you have
    for i in range(num_clusters):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)

        # Find the list position of the closest one (using argmin to find the smallest distance)
        closest_index = np.argmin(distances)
        # Append that position to your closest indices list
        closest_indices.append(closest_index)
        selected_indices = sorted(closest_indices)

    llm4 = ChatOpenAI(temperature=.25,
                      openai_api_key=api_key,
                      max_tokens=1000,
                      model=model_type,
                      request_timeout=180
                      )

    combine_prompt ="""
    Given a some user personal data which will be enclosed in triple backticks (```)
    Your goal is to provide summary insights on the text and tell about user activity behaviour
    The user should be able to understand the insights
    ```{text}```
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])
    reduce_chain = load_summarize_chain(llm=llm4,
                                        chain_type="map_reduce",
                                        map_prompt = combine_prompt_template,
                                        combine_prompt = combine_prompt_template
                                       )
    selected_docs=[docs[doc] for doc in selected_indices]
    summary_list = []

    # Loop through a range of the lenght of your selected docs
    for i, doc in enumerate(selected_docs):
        chunk_summary = reduce_chain.run([doc])
        # Append that summary to your list
        chunk_summary+=" "
        summary_list.append(chunk_summary)
        # print(f"Summary #{i} (chunk #{selected_indices[i]}) - Preview: {chunk_summary[:250]} \n")
    # summaries = "\n\n\n".join(summary_list)

    # print("summary_list ", summary_list)
    return  summary_list
