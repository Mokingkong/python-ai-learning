from langchain_zhipu import ChatZhipuAI,ZhipuAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

print("="*55)
print("     LangChain B6：RAG检索增强生成")
print("     让AI基于你的文档回答问题，不会瞎编")
print("="*55)
#第一：准备知识库文档
print("\n-----准备知识库-----")

knowledge_text = """
公司报销制度：
1. 员工出差需提前3天在OA系统提交出差申请，经部门经理审批后方可出行。
2. 交通费报销标准：高铁二等座、飞机经济舱，超出部分自理。
3. 住宿费报销标准：一线城市每晚不超过500元，二线城市不超过400元。
4. 餐饮补贴：出差期间每人每天100元，无需发票。
5. 报销需在出差结束后15个工作日内提交，逾期不予报销。

公司请假制度：
1. 年假：入职满1年享受5天年假，每增加1年增加1天，最多15天。
2. 病假：需提供三甲医院证明，全年累计不超过30天。
3. 事假：全年累计不超过15天，事假期间扣除当日工资。
4. 请假需提前1天在OA系统申请，紧急情况可事后补办。

公司产品介绍：
1. 智能客服系统：基于大模型的自动客服，支持多轮对话、知识库问答，准确率95%以上。
2. 数据分析平台：一站式数据清洗、分析、可视化平台，支持AI自动生成分析报告。
3. AI写作助手：支持公文、营销文案、技术文档自动生成，内置100+模板。

公司联系方式：
1. 技术支持：tech@example.com，工作时间9:00-18:00
2. 商务合作：business@example.com
3. 人事咨询：hr@example.com
4. 公司地址：广州市天河区珠江新城XX大厦18楼
"""

chunks = [
    "公司报销制度：1.员工出差需提前3天在OA系统提交出差申请，经部门经理审批后方可出行。2.交通费报销标准：高铁二等座、飞机经济舱，超出部分自理。3.住宿费报销标准：一线城市每晚不超过500元，二线城市不超过400元。4.餐饮补贴：出差期间每人每天100元，无需发票。5.报销需在出差结束后15个工作日内提交，逾期不予报销。",
    "公司请假制度：1.年假：入职满1年享受5天年假，每增加1年增加1天，最多15天。2.病假：需提供三甲医院证明，全年累计不超过30天。3.事假：全年累计不超过15天，事假期间扣除当日工资。4.请假需提前1天在OA系统申请，紧急情况可事后补办。",
    "公司产品介绍：1.智能客服系统：基于大模型的自动客服，支持多轮对话、知识库问答，准确率95%以上。2.数据分析平台：一站式数据清洗、分析、可视化平台，支持AI自动生成分析报告。3.AI写作助手：支持公文、营销文案、技术文档自动生成，内置100+模板。",
    "公司联系方式：1.技术支持：tech@example.com，工作时间9:00-18:00。2.商务合作：business@example.com。3.人事咨询：hr@example.com。4.公司地址：广州市天河区珠江新城XX大厦18楼。"
]

documents = [Document(page_content=chunk,metadata={"source":f"文档第{i+1}段"}) for i,chunk in enumerate(chunks)]

#创建向量数据库
print("\n----第二步：创建向量数据库----")

#用智谱AI的embedding模型把文字转成向量
embeddings = ZhipuAIEmbeddings(
    model="embedding-3",
    api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr"
)
#创建Chroma向量数据库，把文档转成向量存进去
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./rag_db"
)
print("向量数据库已创建，文档已向量化比存储")

print("\n----第三步：测试检索----")

test_query = "出差住宿费能报多少？"
results = vector_store.similarity_search(test_query,k=2)
print(f"问题：{test_query}")
print(f"检索到{len(results)}段相关文档:")
for i,doc in enumerate(results):
    print(f"[{i+1}]{doc.page_content[:60]}...")

#RAG回答：检索+AI回答
print("\n----第四步：RAG回答（基于文档回答）")

llm = ChatZhipuAI(model="glm-4-flash",api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr",temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    ("system","你是公司智能客服，请根据以下参考文档回答用户问题。"
            "如果文档中没有相关信息，请回答'抱歉，我在文档中没有找到相关信息'，不要编造。"
            "回答要简洁准确，引用文档内容。\n\n参考文档：\n{context}"),
    ("human","{question}")
])
chain = prompt | llm | StrOutputParser()

questions = [
    "出差住宿费一线城市能报多少？",
    "入职满3年有多少年假",
    "你们公司有什么产品",
    "技术支持邮箱是什么",
    "公司的CEO叫什么名字"
]

for q in questions:
    docs = vector_store.similarity_search(q,k=2)
    context = "\n\n".join([doc.page_content for doc in docs])
    #调用AI
    answer = chain.invoke({"context":context,"question":q})

    print(f"\n问题:{q}")
    print(f"检索到文档:{len(docs)}段")
    print(f"回答:{answer}")

print("RAG完成")
print("重点看：AI只基于文档回答，文档里没有的（如CEO名字）他会说找不到，不会瞎编")