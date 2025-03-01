import getpass
import os
from dotenv import load_dotenv
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#loading environment variables api key will be automatically fetched by chatgroq
load_dotenv()

#In case api not in environment so manual pass on terminal
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

class DataModel(BaseModel):
    topic: str
    name: str
    profession: str
    name1: str
    profession1: str
    name2: str
    profession2: str
    name3: str
    profession3: str
    name4: str
    profession4: str

from models.llama_model_1 import little_llama_answer   #LLama3.1
from models.middle_llama import middle_llama_answer    #LLama3.2
from services.event_summarizer import summarize          #LLama3.3 to summarize the discussion
from models.dee_see import dee_see_answer              #deepseek distilled by qwen
from models.dee_see_meta import dee_see_meta_answer    #deepseek distilled by meta
from models.gemma_model import gemma_answer            #Gemma model

Discussion = ""

# def data_stream(data: DataModel):
#     global Discussion
#     for i in range(3):
#         answer1, Discussion = little_llama_answer(data.name, data.profession, data.topic, Discussion)
#         yield {"message": 'f"{data.name}: {answer1}"'}


# @app.post("/discussion/")
# async def process_data(data: DataModel):
#     return StreamingResponse(data_stream(data), media_type="text/event-stream")