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

for key in ['ds_clicked', 'ps_clicked', 'plan_disable', 'plan']:
    if key not in st.session_state:
        st.session_state[key] = True if key in ['plan_disable'] else False
for var in ['topic', 'name1', 'prof1','name2', 'prof2','plan','Discussion']:
    if var not in st.session_state:
        st.session_state[var] = ""

form = st.form("Input form")
st.session_state.topic = form.text_input("Topic for discussion")
st.session_state.name1 = form.text_input("Name of 1st Character",)
st.session_state.prof1 = form.text_input(f"Profession of 1st Character")
st.session_state.name2 = form.text_input("Name of 2nd Character")
st.session_state.prof2 = form.text_input(f"Profession of 2nd Character")

states = [st.session_state[var] for var in ['topic', 'name1', 'name2', 'prof1', 'prof2']]
def discuss_button():
    flag=0
    for i in range(len(states)):
        if states[i] == '':
            st.warning(f"Please fill {i} field before starting.")
            flag=1
            break   
    if flag ==0:
        st.session_state.ds_clicked = True

def plan_button():
    st.session_state.ps_clicked = True   
    st.session_state.plan_disable = True
start_clicked = form.form_submit_button("Start",on_click=discuss_button)

if st.session_state.ds_clicked:
    st.title(f"{st.session_state.topic} Discussion")
    for i in range(10):
        l_answer,st.session_state.Discussion = little_llama_answer(st.session_state.name1,st.session_state.prof1,st.session_state.topic,st.session_state.Discussion)
        st.write(f"{st.session_state.name1}: {l_answer}")
        m_answer,st.session_state.Discussion = middle_llama_answer(st.session_state.name2,st.session_state.prof2,st.session_state.topic,st.session_state.Discussion)
        st.write(f"{st.session_state.name2}: {m_answer}")
    st.session_state.plan = summarize(st.session_state.Discussion)
    st.session_state.plan_disable= False
    st.session_state.ds_clicked = False

plan_clicked = st.button("Summarize",on_click=plan_button, disabled=st.session_state.plan_disable)

if st.session_state.ps_clicked:
    
    st.markdown(f"concluder: {st.session_state.plan}")
    
