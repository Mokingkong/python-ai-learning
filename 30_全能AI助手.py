from langchain_zhipu import ChatZhipuAI,ZhipuAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage,ToolMessage
from langchain_core.documents import Document
from datetime import datetime

print("-----全能AI助手(记忆+工具+Agent+RAG)-----")

API_KEY = "a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr"
llm = ChatZhipuAI(model="glm-4-flash",api_key=API_KEY,temperature=0.7)
print("\n[1/4]正在构建知识库...")

knowledge = """
公司报销制度：
1.员工出差需提前3天在OA系统提交出差申请，经部门经理审批后方可出行。
2.交通费报销标准：高铁二等座、飞机经济舱，超出部分自理。
3.住宿费报销标准：一线城市每晚不超过500元，二线城市不超过400元。
4.餐饮补贴：出差期间每人每天100元，无需发票。
5.报销需在出差结束后15个工作日内提交，逾期不予报销。

公司请假制度：
1.年假：入职满1年享受5天年假，每增加1年增加1天，最多15天。
2.病假：需提供三甲医院证明，全年累计不超过30天。
3.事假：全年累计不超过15天，事假期间扣除当日工资。
4.请假需提前1天在OA系统申请，紧急情况可事后补办。

公司产品介绍：
1.智能客服系统：基于大模型的自动客服，支持多轮对话、知识库问答，准确率95%以上。
2.数据分析平台：一站式数据清洗、分析、可视化平台，支持AI自动生成分析报告。
3.AI写作助手：支持公文、营销文案、技术文档自动生成，内置100+模板。

公司联系方式：
1.技术支持：tech@example.com，工作时间9:00-18:00
2.商务合作：business@example.com
3.人事咨询：hr@example.com
4.公司地址：广州市天河区珠江新城XX大厦18楼
"""

chunks = [
    "公司报销制度：1.员工出差需提前3天在OA系统提交出差申请，经部门经理审批后方可出行。2.交通费报销标准：高铁二等座、飞机经济舱，超出部分自理。3.住宿费报销标准：一线城市每晚不超过500元，二线城市不超过400元。4.餐饮补贴：出差期间每人每天100元，无需发票。5.报销需在出差结束后15个工作日内提交，逾期不予报销。",
    "公司请假制度：1.年假：入职满1年享受5天年假，每增加1年增加1天，最多15天。2.病假：需提供三甲医院证明，全年累计不超过30天。3.事假：全年累计不超过15天，事假期间扣除当日工资。4.请假需提前1天在OA系统申请，紧急情况可事后补办。",
    "公司产品介绍：1.智能客服系统：基于大模型的自动客服，支持多轮对话、知识库问答，准确率95%以上。2.数据分析平台：一站式数据清洗、分析、可视化平台，支持AI自动生成分析报告。3.AI写作助手：支持公文、营销文案、技术文档自动生成，内置100+模板。",
    "公司联系方式：1.技术支持：tech@example.com，工作时间9:00-18:00。2.商务合作：business@example.com。3.人事咨询：hr@example.com。4.公司地址：广州市天河区珠江新城XX大厦18楼。"
]
documents = []
for i in range(len(chunks)):
    doc = Document(page_content=chunks[i],metadata={"source":f"文档第{i+1}段"})
    documents.append(doc)
embeddings = ZhipuAIEmbeddings(model="embedding-3",api_key=API_KEY)
vector_store = Chroma.from_documents(documents,embedding=embeddings,persist_directory="./rag_db")
print("知识库构建完成")

print("[2/4]加载工具")

@tool
def calculator(expression:str) ->str:
    """计算数学表达式，比如 '1234*5678' 或 '(2+3)*4'。参数expression是要计算的数学表达式字符串。""" 
    try:
        result = eval(expression)
        return f"计算结果:{expression}={result}"
    except Exception as e:
        return f"计算出现错误:{e}"

@tool
def get_current_time()->str:
    """获取当前日期和时间，不需要参数。"""
    now = datetime.now()
    return  f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')}，星期{'一二三四五六日'[now.weekday()]}"

@tool
def get_weather(city:str)->str:
    """查询指定城市的天气。参数city是城市名称，比如'北京'、'上海'、'广州'。"""
    weather={"北京": "晴，25°C", "上海": "多云，28°C", "广州": "雷阵雨，32°C", "深圳": "阵雨，30°C", "珠海": "晴转多云，29°C"}
    return weather.get(city,f"暂无{city}的天气数据")

@tool
def search_knowledge(query:str)->str:
    """搜索公司知识库，查询公司制度、产品、联系方式等信息。参数query是要查询的问题关键词。"""
    docs = vector_store.similarity_search(query,k=3)
    if docs:
        return "知识库检索结果:\n"+"\n---\n".join([doc.page_content for doc in docs])
    return "没有找到相关信息"

tools_map = {
    "calculator":calculator,
    "get_current_time":get_current_time,
    "get_weather":get_weather,
    "search_knowledge":search_knowledge
}
llm_with_tools = llm.bind_tools(list(tools_map.values()))#bind_tools要求传入列表类型，所以要list转，然后去除所有的value,不要key
print("工具加载完成")

print("[3/4]初始化AI助手...")
system_msg = SystemMessage(content="""
    你是公司全能AI助手，具备以下能力：
    1.知识库问答：使用search_knowledge工具查询公司制度、产品、联系方式等信息，基于知识库内容回答问题，不要编造。
    2.数学计算：使用calculator工具计算数学表达式。
    3.时间查询：使用get_current_time工具获取当前时间。
    4.天气查询：使用get_weather工具查询城市天气。
    5.多步任务：复杂问题请分步骤调用工具，每步调用一个，拿到结果后再决定下一步。
    6.记忆：你会记住用户之前说的话，可以引用之前的对话内容。

    回答规则：
    -需要工具时主动调用，不要自己瞎猜
    -知识库没有的信息，明确说“抱歉，知识库中没有相关信息”
    -回答简洁明了，使用中文
    -如果用户问的问题需要多步操作，先规划再执行
""")

messages = [system_msg]
MAX_HISTORY = 20
print("AI助手初始化完成")
print("[4/4]准备就绪!\n")

print(" 全能AI助手已启动，输入‘退出’结束")
print(" 试试问：报销标准、年假、、产品、邮箱、现在几点、广州天气")

while True:
    user_input = input("\n你:")

    if user_input in ["退出","exit","quit"]:
        print("助手：下次再见！")
        exit()

    if not user_input.strip():
        continue

    messages.append(HumanMessage(content=user_input))

    step = 0
    while step < 8:
        step+=1
        response = llm_with_tools.invoke(messages)   #.invoke(message)把括号内的信息发给AI

        if response.tool_calls:
            messages.append(response)
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                print(f"调用工具:{tool_name}{tool_args}")

                if tool_name in tools_map:
                    result = tools_map[tool_name].invoke(tool_args)
                else:
                    result = f"未知工具:{tool_name}"
                print(f"返回:{result[:80]}..."if len(result)>80 else f"返回{result}")
                messages.append(ToolMessage(content=result,tool_call_id=tool_id))
            continue
        else:
            messages.append(AIMessage(content=response.content))
            print(f"\n助手:{response.content}")
            break
        if len(messages) > MAX_HISTORY +1:
            messages = [messages[0]] + messages[-(MAX_HISTORY):]

print("全能AI助手已关闭")
print("本项目整合：Prompt模板+记忆+工具调用+Agent+RAG")