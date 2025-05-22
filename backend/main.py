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
    allow_origins=["https://discussion-pannel-ai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
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

from .models.llama_model_1 import little_llama_answer   #LLama3.1
from .models.middle_llama import middle_llama_answer    #LLama3.2
from .models.dee_see import dee_see_answer              #deepseek distilled by qwen
from .models.dee_see_meta import dee_see_meta_answer    #deepseek distilled by meta
from .models.gemma_model import gemma_answer            #Gemma model
from .services.event_summarizer import summarize

Discussion = ""

@app.post("/send_data/")
async def recieve_json(data: DataModel):
    global Discussion
    Discussion = ""
    global main_data
    main_data = data
    print(main_data)
    print("starting")
    return {"message": "started"}


def data_stream():
    global Discussion
    global main_data
    for i in range(3):
        print("loop")
        answer, Discussion = little_llama_answer(main_data.name, main_data.profession, main_data.topic, Discussion)
        yield f"data: {main_data.name}: {answer}\n\n"
        answer1, Discussion = middle_llama_answer(main_data.name1, main_data.profession1, main_data.topic, Discussion)
        yield f"data: {main_data.name1}: {answer1}\n\n"
        answer2, Discussion = dee_see_answer(main_data.name2, main_data.profession2, main_data.topic, Discussion)
        yield f"data: {main_data.name2}: {answer2}\n\n"
        answer3, Discussion = dee_see_meta_answer(main_data.name3, main_data.profession3, main_data.topic, Discussion)
        yield f"data: {main_data.name3}: {answer3}\n\n"
        answer4, Discussion = gemma_answer(main_data.name4, main_data.profession4, main_data.topic, Discussion)
        yield f"data: {main_data.name4}: {answer4}\n\n"
        


@app.get("/discussion/")
async def process_data():
    print('processing')
    return StreamingResponse(data_stream(), media_type="text/event-stream")

@app.get('/summarize/')
async def summarize_data():
    global Discussion
    print("summarizing")
    summary = summarize(Discussion)
    return {"summary": summary}
