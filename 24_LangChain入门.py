from langchain_zhipu import ChatZhipuAI
from langchain_core.messages import HumanMessage,SystemMessage

print(" LangChain 入门:第一个程序")

llm = ChatZhipuAI(
    model = "glm-4-flash",
    api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr",
    temperature=0.7
)

messages = [
    SystemMessage(content="你是一位Python编程老师，用简单易懂的方式回答问题，每次回答后给一个小练习。"),
    HumanMessage(content="什么是列表推导式")
]

response = llm.invoke(messages)

print("\nAI回答:")
print(response.content)