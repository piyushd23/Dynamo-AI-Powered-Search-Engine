import streamlit as st
import os
import google.generativeai as genai
import time

def caltime():
    st.session_state.start_time=time.time()
def stptime():
    if 'start_time' in st.session_state:
            elapsed_time = round(time.time() - st.session_state.start_time, 2)
            st.write(f"Results Generated in: {elapsed_time} seconds.")
            del st.session_state.start_time

st.title("Dynamo AI ⌨")

os.environ['GOOGLE_API_KEY'] = "AIzaSyCzQwDWn-Kftv7tsOl5lxBKSZml48DsRX8"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# model is "gemini pro"
model = genai.GenerativeModel('gemini-pro')

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"How can I help you today ? "
        }
    ]

# old msgs display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and run Query and return Response
def llm_function(query):
    response = model.generate_content(query)
    if response:
        stptime()
    # Displaying result
    with st.chat_message("assistant"):
        st.markdown(response.text)

    # display input prompt in chatbot ui
    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )

    # display input prompt
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response.text
        }
    )
    

# Accept user input
query = st.chat_input("Ask Me Anything ")

# Calling function 
if query:
    caltime()
    
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(query)