from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

Gemma_model = ChatGroq(
    model="qwen-2.5-32b",
    max_tokens=150,
    temperature=1,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your name is {name} and you are {Profession} and topic of discussion is {topic}. You are in a disussion meeting and the ongoing discussion is {Discussion}",
        ),
        ('human','Now your turn and word limit is 100 words, and **behave stictly according to your profession** and **answer in a single paragraph** and **neither write your name nor profession in the paragraph**')
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
