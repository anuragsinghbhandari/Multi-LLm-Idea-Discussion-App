from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import re
deepllm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
        "system",
        """Your name is {name}, and you are {Profession}. 
        The topic of discussion is {topic}. 
        Your format is like this: 'hm in my opinion .....'.
        
        The ongoing discussion is: {Discussion}"""
    ),
    ('human', 'Now your turn and answer in less than 150 words, avoid repeating')
    ]
)

def clean_deepseek_response(response):
    """Extracts text after </think> and removes the <think> section."""
    if "</think>" in response:
        return re.sub(r".*</think>", "", response, flags=re.DOTALL).strip()
    return response  # Return original response if no </think>


lll_chain = prompt | deepllm
def dee_see_meta_answer(name,Profession,topic,Discussion):
    answer = lll_chain.invoke({
        "name": name,
        "Profession": Profession,
        "topic": topic,
        "Discussion": Discussion,
    })
    filter_answer = clean_deepseek_response(answer.content)
    Discussion +=f'\n {name}: {filter_answer}\n'
    return filter_answer,Discussion

