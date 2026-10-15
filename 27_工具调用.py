from langchain_zhipu import ChatZhipuAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
from datetime import datetime

print(" LangChain B4:工具调用 - 让AI能整整做事")

llm = ChatZhipuAI(model="glm-4-flash",api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr",temperature=0.7)


@tool
def calculator(expression:str) -> str:
    """计算数学表达式,比如‘1234*5678’或‘（2+3）*4’。参数expression是要计算的数学表达式字符串"""
    try:
        result = eval(expression)
        return f"计算结果:{expression} = {result}"
    except Exception as e:
        return f"计算错误:{e}"

@tool
def get_current_time() -> str:
    """获取当前日期和时间，不需要参数。"""
    now = datetime.now()
    return f"当前时间:{now.strftime('%Y年%m月%d日 %H:%M：%S')}，星期{'一二三四五六日'[now.weekday()]}"

@tool
def get_weather(city:str) -> str:
    """查询指定城市的天气。参数city是城市名称，比如‘北京、‘上海’、‘广州’。"""
    weather_data = {
        "北京":"晴，25度，微风",
        "上海":"多云，28度，东南风3级",
        "广州":"雷阵雨,32度，湿度80%",
        "深圳":"阵雨，30度，海风",
        "珠海":"青砖多云,29度，微风"
    }
    return weather_data.get(city,f"暂无{city}的天气数据")

tools = [calculator,get_current_time,get_weather]
llm_with_tools = llm.bind_tools(tools)

system_msg = SystemMessage(content = "你是一个智能助手，当用户的问题需要计算、查时间、查天气时，请主动调用对应的工具，不要自己瞎猜。调用工具后，根据工具返回的结果回答用户")

test_questions = [
    "1234*5678等于多少?",
    "现在几点了?",
    "广州今天天气怎么样?",
    "你好，你叫什么名字?"
]

for i,question in enumerate(test_questions,1):
    print(f"\n{'='*50}")
    print(f"问题{i}:{question}")
    print(f"{'='*50}")
    messages = [system_msg,HumanMessage(content=question)] #前面是系统消息，后面是用户问题
    response = llm_with_tools.invoke(messages)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            print(f"AI调用工具：{tool_name}，参数：{tool_args}")

            messages.append(response)

            if tool_name == "calculator":
                result = calculator.invoke(tool_args)
            elif tool_name == 'get_current_time':
                result = get_current_time.invoke(tool_args)
            elif tool_name == "get_weather" :
                result = get_weather.invoke(tool_args)
            else:
                result = "未知工具"

            print(f"工具返回:{result}")

            messages.append(ToolMessage(content=result,tool_call_id=tool_id))
            final_response = llm_with_tools.invoke(messages)
            print(f"\nAI回答:{final_response.content}")
    else:
        print(f"AI回答:{response.content}")

print("  工具调用完成！AI能自己判断该调用什么工具")