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
from models.dee_see import dee_see_answer              #deepseek distilled by qwen
from models.dee_see_meta import dee_see_meta_answer    #deepseek distilled by meta
from models.gemma_model import gemma_answer            #Gemma model

# Initializing variables in session to perssist even after rerun
for key in ['ds_clicked', 'ps_clicked', 'plan_disable']: #boolean variables for proper working of functions
    if key not in st.session_state:
        st.session_state[key] = True if key in ['plan_disable'] else False
for var in ['topic', 'name1', 'prof1','name2', 'prof2','name3','prof3','name4','prof4','name5','prof5','plan','Discussion']: #normal variables used as input or storage of data
    if var not in st.session_state:
        st.session_state[var] = ""

#storing all input variable for checking later
name_states = ['name1', 'name2', 'name3', 'name4', 'name5']
prof_states = ['prof1', 'prof2', 'prof3', 'prof4', 'prof5'] 
active_states = ['active_name1', 'active_name2', 'active_name3', 'active_name4', 'active_name5']

main_states = name_states+prof_states
#function to set ds_clicked true for starting discussion
def discuss_button():   
    flag=0
    #to check all inputs are filled
    for i in range(len(main_states)):
        if st.session_state[main_states[i]] == '':
            st.warning(f"Please fill {i} field before starting.")
            flag=1
            break   
    if flag ==0:
        st.session_state.ds_clicked = True

#button to display the summary
def plan_button():
    st.session_state.ps_clicked = True   #enables the summarry display
    st.session_state.plan_disable = True    #Disables the summarize button


#form creation to collect all inputs together on submit
with st.container(height=None): #initializing form
    st.session_state.topic = st.text_input("Topic for discussion")    #27-31 input inside form
    row1 = st.columns([0.45,0.45,0.1], vertical_alignment='center')
    row2 = st.columns([0.45,0.45,0.1], vertical_alignment='center')
    row3 = st.columns([0.45,0.45,0.1], vertical_alignment='center')
    row4 = st.columns([0.45,0.45,0.1], vertical_alignment='center')
    row5 = st.columns([0.45,0.45,0.1], vertical_alignment='center')  #splitting the screen into 3 columns
    i = 0
    rows = [row1,row2,row3,row4,row5]
    for row in rows:
        st.session_state[name_states[i]] = row[0].text_input(f"Name of Character{i+1}")
        st.session_state[prof_states[i]] = row[1].text_input(f"Profession of Character {i+1} ")
        active_states[i] = row[2].toggle(label = '',value=False, help = f'Activate participant {i+1}')
        i+=1


    # input submission button for form and direct to discuss_button func on click
    start_clicked = st.button("Start",on_click=discuss_button)

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
        d_m_answer, st.session_state.Discussion = dee_see_meta_answer(st.session_state.name4,st.session_state.prof4,st.session_state.topic,st.session_state.Discussion)
        st.write(f"{st.session_state.name4}: {d_m_answer}") #Idea by name4
        g_answer,st.session_state.Discussion = gemma_answer(st.session_state.name5,st.session_state.prof5,st.session_state.topic,st.session_state.Discussion)
        st.write(f"{st.session_state.name5}: {g_answer}") #Idea by name5

    st.session_state.plan = summarize(st.session_state.Discussion)  #discussion summarized and stored in plan
    st.session_state.plan_disable= False    #False to enable the visibility of summarize button
    st.session_state.ds_clicked = False     #False to stop chances of further discussion on rerun

#Button to summarize initial state is disabled enables after discussion
plan_clicked = st.button("Summarize",on_click=plan_button, disabled=st.session_state.plan_disable)  

#Shows summary
if st.session_state.ps_clicked:
    st.markdown(f"concluder: {st.session_state.plan}")
    
