from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import re
deepllm = ChatGroq(
    model="qwen-qwq-32b",
    temperature = 1,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
        "system",
        """Your name is {name}, and you are {Profession}. 
        The topic of discussion is {topic}.         
        The ongoing discussion is: {Discussion}"""
    ),
    ('human', 'Now your turn and word limit is 100 words, **behave strictly according to your profession** and **answer in a single paragraph** and **neither write your name nor profession in the paragraph**.' )
    ]
)

def clean_deepseek_response(response):
    """Extracts text after </think> and removes the <think> section."""
    if "</think>" in response:
        return re.sub(r".*</think>", "", response, flags=re.DOTALL).strip()
    return response  # Return original response if no </think>


lll_chain = prompt | deepllm
def dee_see_answer(name,Profession,topic,Discussion):
    answer = lll_chain.invoke({
        "name": name,
        "Profession": Profession,
        "topic": topic,
        "Discussion": Discussion,
    })
    filter_answer = clean_deepseek_response(answer.content)
    Discussion +=f'\n {name}: {filter_answer}\n'
    return filter_answer,Discussion

