import getpass
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    
from models.llama_model_1 import little_llama_answer
from models.middle_llama import middle_llama_answer
from models.event_summarizer import summarize

if 'ds_clicked' not in st.session_state:
    st.session_state.ds_clicked = False
if 'ps_clicked' not in st.session_state:
    st.session_state.ps_clicked = False
if 'plan_disable' not in st.session_state:
    st.session_state.plan_disable = True

Discussion = ""
plan = ""
topic = st.text_input("Topic for discussion")
name1 = st.text_input("Name of 1st Character",)
prof1 = st.text_input(f"Profession of {name1}",key='name1')
name2 = st.text_input("Name of second Character")
prof2 = st.text_input(f"Profession of {name2}",key='name2')

def discuss_button():
    st.session_state.ds_clicked = True

def plan_button():
    st.session_state.ps_clicked = True    
start_clicked = st.button("Start",on_click=discuss_button)
if st.session_state.ds_clicked:
    st.title(f"{topic} Discussion")
    for i in range(10):
        l_answer,Discussion = little_llama_answer(name1,prof1,topic,Discussion)
        st.write(f"{name1}: {l_answer}")
        m_answer,Discussion = middle_llama_answer(name2,prof2,topic,Discussion)
        st.write(f"{name2}: {m_answer}")
    plan = summarize(Discussion)
    st.session_state.plan_disable= False
plan_clicked = st.button("Summarize",on_click=plan_button, disabled=st.session_state.plan_disable)

if st.session_state.ps_clicked:
    st.markdown(f"concluder: {plan}")
