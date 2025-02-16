import getpass
import os

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
from llama_model_1 import little_llama_answer
answer = little_llama_answer("Cloud Engineer","Email Automation Saas",[])

print(answer)