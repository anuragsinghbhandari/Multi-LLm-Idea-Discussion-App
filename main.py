import getpass
import os
from models.llama_model_1 import little_llama_answer
from models.middle_llama import middle_llama_answer
from models.event_summarizer import summarize

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
Discussion = ""
for i in range(10):
    l_answer,Discussion = little_llama_answer("Entrepreneur ","Real world problem tech solution",Discussion)
    #print(f"Little_llama: {l_answer}")
    m_answer,Discussion = middle_llama_answer("Software engineer","Real world problem tech solution",Discussion)
    #print(f"Middle_llama: {m_answer}")
print(Discussion)
plan = summarize(Discussion)
print(plan)