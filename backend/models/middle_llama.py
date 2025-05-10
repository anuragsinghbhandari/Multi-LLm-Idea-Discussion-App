from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

Middle_llama = ChatGroq(
    model="llama3-8b-8192",
    max_tokens=150,
    temperature=1,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your name is {name} and you are {Profession} and topic of discussion is {topic}. You are in a disussion meeting and the ongoing discussion is {Discussion}",
        ),
        ('human','Now your turn and limit is 100 words and **behave strictly according to your profession** and **answer in a single paragraph** and **neither write your name nor profession in the paragraph**')
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

