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
            "You are part of a team that builds solutions. Your name is Middle_llama . You are {Profession} and topic of discussion is {topic}. Participate in discussion. don't use your name in response ",
        ),
        ('human','{Discussion}')
    ]
)

lll_chain = prompt | Middle_llama
def middle_llama_answer(Profession,topic,Discussion):
    answer = lll_chain.invoke({
        "Profession": Profession,
        "topic": topic,
        "Discussion": Discussion,
    })
    Discussion +=f'\n Middle_llama: {answer.content}\n'
    return answer.content,Discussion

