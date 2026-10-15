from langchain_zhipu import ChatZhipuAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
from datetime import datetime

print(" LangChain B5:Agent智能体 - 多步自主执行")
print(" AI会自己规划、反复调用工具，直到人物完成")
print("="*55)

llm = ChatZhipuAI(model="glm-4-flash",api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr",temperature=0.7)

@tool
def calculator(expression :str) -> str:
    """计算数学表达式，比如‘1234*5678’或‘（2+3）*4’。参数expression是要计算的数学表达式字符串"""
    try:
        result = eval(expression)                  #eval() 将括号内的字符串当代码执行
        return f"计算结果:{expression} = {result}"
    except Exception as e:
        return f"计算错误:{e}"

@tool 
def get_current_time() -> str:
    """获取当前日期和时间，不需要参数"""
    now = datetime.now()
    return f"当前时间:{now.strftime('%Y年%m月%d日 %H:%M:%S')},星期{'一二三四五六日'[now.weekday()]}"

@tool
def get_weather(city:str) -> str:
    """查询指定城市的天气。参数city是城市名称，比如‘北京’、‘上海’、‘广州’。"""
    weather_data = {
        "北京": "晴，25°C，微风",
        "上海": "多云，28°C，东南风3级",
        "广州": "雷阵雨，32°C，湿度80%",
        "深圳": "阵雨，30°C，海风",
        "珠海": "晴转多云，29°C，微风"
    }
    return weather_data.get(city,f"暂无{city}的天气数据")

tools_map = {
    "calculator" : calculator,
    "get_current_time" : get_current_time,
    "get_weather" : get_weather
}
llm_with_tools =  llm.bind_tools(list(tools_map.values()))

system_msg = SystemMessage(content="""你是一个智能助手，可以使用以下工具完成任务：
- calculator：计算数学表达式
- get_current_time：获取当前时间
- get_weather：查询城市天气

当用户的问题需要多步操作时，请一步步调用工具，每步调用一个工具，拿到结果后再决定下一步。
所有需要的信息都获取到后，再给出最终回答。
如果不需要工具，直接回答。""")

def agent_run(user_input):
    messages = [system_msg,HumanMessage(content=user_input)]
    step = 0
    max_steps = 10   #最大循环此书

    while step < max_steps:
        step += 1
        print(f"\n----第{step}步----")

        response = llm_with_tools.invoke(messages)

        #检查AI是否调用工具
        if response.tool_calls:
            messages.append(response)    #AI工具调用请求加入消息
            #执行所有的工具调用
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                print(f"调用工具:{tool_name},参数:{tool_args}")

                if tool_name in tools_map:
                    result = tools_map[tool_name].invoke(tool_args)
                else:
                    result = f"未知工具:{tool_name}"

                print(f"返回:{result}")
                messages.append(ToolMessage(content=result,tool_call_id = tool_id))

            continue
        else:
            print(f"\n   最终回答：{response.content}")
            return response.content

    print("\n达到最大步数，任务未完成")
    return "任务超时"

test_questions = [
    "现在几点了?",
    "广州天气怎么样？用计算器酸以下32度等于多少华氏度(华氏度=摄氏度*9/5+32)",
    "查一下北京和上海的天气，然后告诉我哪个城市天气更好"
]

for i,question in enumerate(test_questions,1):
    print(f"任务{i}:{question}")
    agent_run(question)

print("Agent完成!")
print(" 重点看：任务2和任务3需要多步调用工具，AI自己规划步骤")