import streamlit as st
import requests
import openai

limit = 3750

def weather(city):
    res = requests.get(f"{endpoint_url}/weather?q={city}")
    st.write(res.json())


def retrieve(query,show_context=False,show_prompt=False):
   
    # First query API to get relevant doc chunks 
    res = requests.get(f"{endpoint_url}/weather?q={query}")
    d = res.json()

    # Transform dict into list of strings with key and value
    contexts = [k+': '+str(d[k]) for k in d.keys()]
    if show_context:
        st.write(contexts)
    
    # Then build our prompt with the retrieved contexts included
    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n\n"
    )
    prompt_end = (
        f"\n\nQuestion: {q}\nAnswer:"
    )
    # append contexts until hitting limit
    prompt = (
                prompt_start +
                "\n".join(contexts) +
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

st.title('Test ChatGPT Plugin 🤖')

st.write('This plugin has been build on the [OpenWeatherMap](https://openweathermap.org/api) API. \n\n',
         'it can answer queries by augmenting the ChatGPT response by information retrieved from the weather.')

endpoint_url = st.text_input('Endpoint URL',"https://weather-plugin-yanndebray.replit.app/")

q = st.text_input('query','What is the weather in London?')

show_context=st.checkbox('Show context',value=False)
show_prompt=st.checkbox('Show prompt',value=False)

if st.button('Send'):
    # weather(q)
    retrieve(q,show_context=show_context,show_prompt=show_prompt)