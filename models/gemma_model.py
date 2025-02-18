from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

Gemma_model = ChatGroq(
    model="gemma2-9b-it",
    max_tokens=100,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your name is {name} and you are {Profession} and topic of discussion is {topic}. You are in a disussion meeting and the ongoing discussion is {Discussion}",
        ),
        ('human','Now your turn and answer in less than 100 words, avoid repeating ideas')
    ]
)

lll_chain = prompt | Gemma_model
def gemma_answer(name,Profession,topic,Discussion):
    answer = lll_chain.invoke({
        "name": name,
        "Profession": Profession,
        "topic": topic,
        "Discussion": Discussion,
    })
    Discussion +=f'\n {name}: {answer.content}\n'
    return answer.content,Discussion
