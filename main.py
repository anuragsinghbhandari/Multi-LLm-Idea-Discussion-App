import getpass
import os
from dotenv import load_dotenv
import streamlit as st
import time
#loading environment variables api key will be automatically fetched by chatgroq
load_dotenv()

#In case api not in environment so manual pass on terminal
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    
from models.llama_model_1 import little_llama_answer   #LLama3.1
from models.middle_llama import middle_llama_answer    #LLama3.2
from services.event_summarizer import summarize          #LLama3.3 to summarize the discussion
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
for key in ['active_states1', 'active_states2', 'active_states3', 'active_states4', 'active_states5']: #boolean variables for activation of participants
    if key not in st.session_state:
        st.session_state[key] = False
st.session_state.speed = 1 #speed of discussion

#storing all input variable for checking later
name_states = ['name1', 'name2', 'name3', 'name4', 'name5']
prof_states = ['prof1', 'prof2', 'prof3', 'prof4', 'prof5'] 
main_states = name_states+prof_states
#function to set ds_clicked true for starting discussion
def discuss_button():
    st.session_state.Discussion = ""
    st.session_state.ps_clicked =  False
    if st.session_state.topic == "":
        st.warning("Please fill the topic field before starting.")
        return   
    least = 0
    #to check all inputs are filled
    for i in range(len(name_states)):
        if (st.session_state[f"active_states{i+1}"]==True):
            least +=1
            if (st.session_state[name_states[i]] == '' or st.session_state[prof_states[i]] == ''):
                st.warning(f"Please fill details of participant {i+1} before starting.")
                return  
    
    if least<2:
        st.warning("Please select atleast Two participant before starting.") 
    if least >1:
        st.session_state.ds_clicked = True

#button to display the summary
def plan_button():
    st.session_state.ps_clicked = True   #enables the summarry display
    st.session_state.plan_disable = True    #Disables the summarize button

def response_generator(answer, speed=st.session_state.speed):
    for word in answer.split():
        yield word + " "
        time.sleep(0.5/speed)



#form creation to collect all inputs together on submit
with st.container(height=None): #initializing form
    st.session_state.topic = st.text_input("Topic for discussion", placeholder = "Ensure you finalize participants before topic")

    rows = []
    for _ in range(5):
        rows.append(st.columns([0.45, 0.45, 0.1], vertical_alignment='center'))

    for i, row in enumerate(rows):
        # Get active state first
        active = st.session_state[f"active_states{i+1}"]

        # Create inputs based on the updated state
        st.session_state[name_states[i]] = row[0].text_input(
            f"Name of Character {i+1}",
            value=st.session_state[name_states[i]],
            disabled=not active
        )

        st.session_state[prof_states[i]] = row[1].text_input(
            f"Profession of Character {i+1}",
            value=st.session_state[prof_states[i]],
            disabled=not active
        )
        st.session_state[f"active_states{i+1}"] = row[2].toggle(
            label='',
            value=active,
            help=f'Activate participant {i+1}',
        )

    finalize_participants = st.button("Finalize Participants", help="Click this to activate the required participant") #button to finalize participants
    # input submission button for form and direct to discuss_button func on click
    col1, col2 = st.columns([1,3],vertical_alignment='center')
    with col1:
        start_clicked = st.button("Start",on_click=discuss_button)
    with col2:
        options = {'1x':1, '2x':2, '4x':4,'ASAP':100}
        selection = st.segmented_control("Speed of discussion", options.keys(),default='1x',on_change=discuss_button)
        st.session_state.speed = options[selection]
        
#starting of discussion after submission of inputs
if st.session_state.ds_clicked:
    st.title(f"{st.session_state.topic} Discussion")

    #discussion till 10 turns of each
    for i in range(5):
        if st.session_state.active_states1:
            name1_avat = st.chat_message(f"{st.session_state.name1}")
            l_answer,st.session_state.Discussion = little_llama_answer(st.session_state.name1,st.session_state.prof1,st.session_state.topic,st.session_state.Discussion)
            name1_avat.write(f"{st.session_state.name1}:")
            name1_avat.write_stream(response_generator(l_answer, st.session_state.speed)) #Idea by name1
        if st.session_state.active_states2:
            name2_avat = st.chat_message(f"{st.session_state.name2}")
            m_answer,st.session_state.Discussion = middle_llama_answer(st.session_state.name2,st.session_state.prof2,st.session_state.topic,st.session_state.Discussion)
            name2_avat.write(f"{st.session_state.name2}:") #Idea by name2
            name2_avat.write_stream(response_generator(m_answer, st.session_state.speed))
        if st.session_state.active_states3:
            name3_avat = st.chat_message(f"{st.session_state.name3}")
            d_answer,st.session_state.Discussion = dee_see_answer(st.session_state.name3,st.session_state.prof3,st.session_state.topic,st.session_state.Discussion)
            name3_avat.write(f"{st.session_state.name3}:") #Idea by name3
            name3_avat.write_stream(response_generator(d_answer, st.session_state.speed))
        if st.session_state.active_states4:
            name4_avat = st.chat_message(f"{st.session_state.name4}")
            d_m_answer, st.session_state.Discussion = dee_see_meta_answer(st.session_state.name4,st.session_state.prof4,st.session_state.topic,st.session_state.Discussion)
            name4_avat.write(f"{st.session_state.name4}:") #Idea by name4
            name4_avat.write_stream(response_generator(d_m_answer,st.session_state.speed))
        if st.session_state.active_states5:
            name5_avat = st.chat_message(f"{st.session_state.name5}")
            g_answer,st.session_state.Discussion = gemma_answer(st.session_state.name5,st.session_state.prof5,st.session_state.topic,st.session_state.Discussion)
            name5_avat.write(f"{st.session_state.name5}") #Idea by name5
            name5_avat.write_stream(response_generator(g_answer, st.session_state.speed))
    st.session_state.plan = summarize(st.session_state.Discussion)  #discussion summarized and stored in plan
    st.session_state.plan_disable= False    #False to enable the visibility of summarize button
    st.session_state.ds_clicked = False  #False to rediscission on rerun

#Button to summarize initial state is disabled enables after discussion
plan_clicked = st.button("Summarize",on_click=plan_button, disabled=st.session_state.plan_disable)

#Shows summary
if st.session_state.ps_clicked:
    st.title("Summary")
    st.markdown(f"{st.session_state.plan}")
    st.download_button("Download Summary", data=st.session_state.plan, file_name="summary.txt", mime="text/plain",disabled= not st.session_state.ps_clicked)
    st.download_button("Download Discussion", data=st.session_state.Discussion, file_name="discussion.txt", mime="text/plain", disabled= not st.session_state.ps_clicked)

