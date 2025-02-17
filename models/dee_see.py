from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

deepllm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    max_tokens=100,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your name is {name} and you are {Profession} and topic of discussion is {topic}. please dont tell me about yourself and current scienerio give your opinion only. your response format is like this 'hm in my opinion .....' and the ongoing discussion is {Discussion}",
        ),
        ('human','Now your turn')
    ]
)

lll_chain = prompt | deepllm
def dee_see_answer(name,Profession,topic,Discussion):
    answer = lll_chain.invoke({
        "name": name,
        "Profession": Profession,
        "topic": topic,
        "Discussion": Discussion,
    })
    Discussion +=f'\n {name}: {answer.content}\n'
    return answer.content,Discussion

