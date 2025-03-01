from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

Middle_llama = ChatGroq(
    model="llama-3.2-3b-preview",
    max_tokens=150,
    temperature=1,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Your name is {name} and you are {Profession} and topic of discussion is {topic}. You are in a disussion meeting and the ongoing discussion is {Discussion}",
        ),
        ('human','Now your turn and limit is 100 words and avoid repeating ideas')
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

