#voice to voice output

import streamlit as st
import os
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr


def txs(text):
    engine=pyttsx3.init()
    engine.setProperty('rate',150)
    engine.say(text)
    engine.runAndWait()

def txs2(text):
    engine=pyttsx3.init()
    engine.setProperty('rate',150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()



def voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand audio.")
        return ""

st.title("Dynamo AI 🎙")

os.environ['GOOGLE_API_KEY'] = "YOUR_GOOGLE_API_KEY_HERE"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])


model = genai.GenerativeModel('gemini-pro')

#chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"How can I help you today ? "
        }
    ]
col1, col2 = st.columns(2)
with col1:
    button1=st.button("Get Voice Input")
with col2:
    button2=st.toggle("👩")
strings=""
if button1:
    voice_input = voice()
    #st.write("Voice input:", voice_input)
    if voice_input:
        strings+=voice_input

#chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# response
def llm_function(query):
    response = model.generate_content(query)
    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response.text)

    
    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )

    
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response.text
        }
    )
    if response.text:
            if button2:
                txs2(response.text)
            else:
                txs(response.text)


# Accept input
query = strings


if query:
   
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(query)



