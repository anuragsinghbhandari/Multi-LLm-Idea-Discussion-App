import getpass
import os
from dotenv import load_dotenv
import streamlit as st

#loading environment variables api key will be automatically fetched by chatgroq
load_dotenv()

#In case api not in environment so manual pass on terminal
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    
from models.llama_model_1 import little_llama_answer   #LLama3.1
from models.middle_llama import middle_llama_answer    #LLama3.2
from models.event_summarizer import summarize          #LLama3.3 to summarize the discussion
from models.dee_see import dee_see_answer              #deepseek distilled by meta

# Initializing variables in session to perssist even after rerun
for key in ['ds_clicked', 'ps_clicked', 'plan_disable']: #boolean variables for proper working of functions
    if key not in st.session_state:
        st.session_state[key] = True if key in ['plan_disable'] else False
for var in ['topic', 'name1', 'prof1','name2', 'prof2','plan','Discussion']: #normal variables used as input or storage of data
    if var not in st.session_state:
        st.session_state[var] = ""

#form creation to collect all inputs together on submit
form = st.form("Input form") #initializing form
st.session_state.topic = form.text_input("Topic for discussion")    #27-31 input inside form
st.session_state.name1 = form.text_input("Name of 1st Character")   
st.session_state.prof1 = form.text_input(f"Profession of 1st Character")
st.session_state.name2 = form.text_input("Name of 2nd Character")
st.session_state.prof2 = form.text_input(f"Profession of 2nd Character")
st.session_state.name3 = form.text_input("Name of 3rd Character")
st.session_state.prof3 = form.text_input("Profession of 3rd Character")

#storing all input variable for checking later
states = [st.session_state[var] for var in ['topic', 'name1', 'name2', 'prof1', 'prof2', 'name3', 'prof3']] 

#function to set ds_clicked true for starting discussion
def discuss_button():   
    flag=0
    #to check all inputs are filled
    for i in range(len(states)):
        if states[i] == '':
            st.warning(f"Please fill {i} field before starting.")
            flag=1
            break   
    if flag ==0:
        st.session_state.ds_clicked = True

#button to display the summary
def plan_button():
    st.session_state.ps_clicked = True   #enables the summarry display
    st.session_state.plan_disable = True    #Disables the summarize button

# input submission button for form and direct to discuss_button func on click
start_clicked = form.form_submit_button("Start",on_click=discuss_button)

#starting of discussion after submission of inputs
if st.session_state.ds_clicked:
    st.title(f"{st.session_state.topic} Discussion")
    #discussion till 10 turns of each
    for i in range(5):
        l_answer,st.session_state.Discussion = little_llama_answer(st.session_state.name1,st.session_state.prof1,st.session_state.topic,st.session_state.Discussion)
        st.write(f"{st.session_state.name1}: {l_answer}") #Idea by name1
        m_answer,st.session_state.Discussion = middle_llama_answer(st.session_state.name2,st.session_state.prof2,st.session_state.topic,st.session_state.Discussion)
        st.write(f"{st.session_state.name2}: {m_answer}") #Idea by name2
        d_answer,st.session_state.Discussion = dee_see_answer(st.session_state.name3,st.session_state.prof3,st.session_state.topic,st.session_state.Discussion)
        st.write(f"{st.session_state.name3}: {d_answer}") #Idea by name3
    st.session_state.plan = summarize(st.session_state.Discussion)  #discussion summarized and stored in plan
    st.session_state.plan_disable= False    #False to enable the visibility of summarize button
    st.session_state.ds_clicked = False     #False to stop chances of further discussion on rerun

#Button to summarize initial state is disabled enables after discussion
plan_clicked = st.button("Summarize",on_click=plan_button, disabled=st.session_state.plan_disable)  

#Shows summary
if st.session_state.ps_clicked:
    st.markdown(f"concluder: {st.session_state.plan}")
    
