from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

Little_llama = ChatGroq(
    model="llama-3.1-8b-instant",
    max_tokens=100,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your name is {name} and you are {Profession} and topic of discussion is {topic}. your response format is like this 'hm in my opinion .....' and the ongoing discussion is {Discussion}",
        ),
        ('human','Now your turn')
    ]
)

lll_chain = prompt | Little_llama
def little_llama_answer(name,Profession,topic,Discussion):
    answer = lll_chain.invoke({
        "name": name,
        "Profession": Profession,
        "topic": topic,
        "Discussion": Discussion,
    })
    Discussion +=f'{name}: {answer.content}'
    return answer.content,Discussion

