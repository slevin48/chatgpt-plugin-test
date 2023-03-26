import streamlit as st
import requests
import openai
# import os
# from dotenv import load_dotenv

# load_dotenv()
# BEARER_TOKEN = os.environ.get("BEARER_TOKEN") 

BEARER_TOKEN = st.secrets["BEARER_TOKEN"]
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

endpoint_url = "https://seal-app-ulquy.ondigitalocean.app"

limit = 3750

def answers(queries):
    res = requests.post(
        f"{endpoint_url}/query",
        headers=headers,
        json={
            'queries': queries
        }
    )
    # st.write(res)
    # st.write(res.json()['results'][0]['query'])
    # st.write(res.json()['results'][0]['results'])

    # # Multiple queries at once
    # for query_result in res.json()['results']:
    #     query = query_result['query']
    #     answers = []
    #     scores = []
    query_result = res.json()['results'][0]
    for result in query_result['results']:
        st.write('answer: ',result['text'])
        st.write('score: ',round(result['score'], 2))
        st.write('url: ',result['metadata']['url'].replace('\\','/'))
        st.write('---')
    #         answers.append(result['text'])
    #         scores.append(round(result['score'], 2))
    #     st.write(query+"\n\n"+"\n".join([f"{s}: {a}" for a, s in zip(answers, scores)]))


def retrieve(queries,show_context=False,show_prompt=False,show_sources=True):
   
    # First query API to get relevant doc chunks 
    res = requests.post(
        f"{endpoint_url}/query",
        headers=headers,
        json={
            'queries': queries
        }
    )

    query_result = res.json()['results'][0]
    contexts = [result['text'] for result in query_result['results']]
    
    if show_context:
        st.write(contexts)
    
    # Then build our prompt with the retrieved contexts included
    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {q}\nAnswer:"
    )
    # append contexts until hitting limit
    for i in range(1, len(contexts)):
        if len("\n\n---\n\n".join(contexts[:i])) >= limit:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts[:i-1]) +
                prompt_end
            )
            break
        elif i == len(contexts)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts) +
                prompt_end
            )

    if show_prompt:
        st.write(prompt)

    rag = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "user", "content": prompt }
            ])

    st.write(rag.choices[0].message.content)

    if show_sources:
        st.write('Sources:')
        for result in query_result['results']:
            st.write('- ',result['metadata']['url'].replace('\\','/'))
    # return rag

st.title('Test ChatGPT Plugin 🤖')

st.write('This retrieval plugin has been build on the [LangChain documentation](https://python.langchain.com/en/latest/index.html)',
         '\n\n',
         'it can answer queries by augmenting the ChatGPT response by information retrived from the doc.')

# d = "What is the LLMChain in LangChain?"
d = "How do I use Pinecone in LangChain"
# d = "What is the difference between Knowledge Graph memory and buffer memory for conversational memory?"

q = st.text_input('query',d)

queries = [{'query': q}]

if st.button('Send'):
    # answers(queries)
    retrieve(queries)