from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

Middle_llama = ChatGroq(
    model="llama-3.2-3b-preview",
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

lll_chain = prompt | Middle_llama
def middle_llama_answer(name,Profession,topic,Discussion):
    answer = lll_chain.invoke({
        "name": name,
        "Profession": Profession,
        "topic": topic,
        "Discussion": Discussion,
    })
    Discussion +=f'\n {name}: {answer.content}\n'
    return answer.content,Discussion

