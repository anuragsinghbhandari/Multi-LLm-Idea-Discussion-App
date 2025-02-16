from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

Little_llama = ChatGroq(
    model="llama-3.1-8b-instant",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are part of a team that builds solutions. Your name is little_llama . You are {Profession} and topic of discussion is {topic}. Participate in discussion.",
        ),
        ('human','{Discussion}')
    ]
)

lll_chain = prompt | Little_llama
def little_llama_answer(Profession,topic,Discussion):
    answer = lll_chain.invoke({
        "Profession": Profession,
        "topic": topic,
        "Discussion": Discussion,
    })
    return answer.content

