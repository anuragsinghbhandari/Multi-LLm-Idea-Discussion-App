from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are expert in making presentations and notes of event discussion. Given a discussion extract the information out of it and organize it so that it looks like a final plan.",
        ),
        ('human','{Discussion}')
    ]
)

lll_chain = prompt | llm
def summarize(Discussion):
    answer = lll_chain.invoke({
        "Discussion": Discussion,
    })
    
    return answer.content

