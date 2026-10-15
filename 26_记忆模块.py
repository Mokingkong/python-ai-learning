from langchain_zhipu import ChatZhipuAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

print("=" * 55)
print("  LangChain B3：记忆模块 - 有记忆的AI助手")
print("  输入 '退出' 结束对话")
print("=" * 55)

llm = ChatZhipuAI(model="glm-4-flash", api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr", temperature=0.7)

messages = [
    SystemMessage(content="你是一位贴心的AI助手，会记住用户之前说过的话。"
                          "回答时可以引用之前的对话内容，让用户感受到你有记忆。")
]

print("\nAI：你好！我是有记忆的AI助手，我们聊聊吧！\n")

while True:
    user_input = input("你：")
    
    if user_input in ["退出", "exit", "quit"]:
        print("AI：再见！期待下次和你聊天～")
        break
    
    messages.append(HumanMessage(content=user_input))
    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))
    
    print(f"AI：{response.content}\n")

print("\n" + "=" * 55)
print("  对话结束，看看AI记住了什么：")
print("=" * 55)
for i, msg in enumerate(messages):
    if msg.type == "system":
        role = "系统设定"
    elif msg.type == "human":
        role = "你"
    else:
        role = "AI"
    print(f"  [{i+1}] {role}：{msg.content[:50]}...")