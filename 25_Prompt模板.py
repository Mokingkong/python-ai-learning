from langchain_zhipu import ChatZhipuAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

print(" LangChain B2:Prompt模板 + 链式调用")

llm = ChatZhipuAI(model="glm-4-flash",api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr",temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    ("system","你是一位专业的文案专家，擅长写各种类型的文案。""要求：语言生动有感染力，适当使用emoji，字数200字左右。"),
    ("human","请写一篇{type}文案,主题是{topic},目标受众是{audience}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

print("\n----第一次调用:小红薯文案----")
result1 = chain.invoke({
    "type":"小红薯种草笔记",
    "topic":"Python自动化办公",
    "audience":"职场小白"
})
print(result1)

print("\n----第二次调用:朋友圈文案----")
result2 = chain.invoke({
    "type":"朋友圈文案",
    "topic":"周末学习Python",
    "audience":"朋友"
})
print(result2)

print("\n----第三次调用:淘宝标题----")
result3 = chain.invoke({
    "type":"淘宝商品标题",
    "topic":"机械键盘",
    "audience":"游戏玩家"
})
print(result3)

