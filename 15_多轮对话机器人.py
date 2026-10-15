from zhipuai import ZhipuAI

# 这里直接写你的真实API Key（和14里一模一样的那串）
client = ZhipuAI(api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr")

# 对话历史
messages = [
    {"role": "system", "content": "你是一个小红书爆款文案博主，擅长写种草笔记，风格活泼，多用emoji，每段不超过3行，结尾加3-5个话题标签。用户给你产品信息，你输出完整文案。"}
]

print("=" * 40)
print("  AI 对话机器人（输入 quit 退出）")
print("=" * 40)

while True:
    user_input = input("\n你: ")
    
    if user_input.lower() in ["quit", "exit", "退出"]:
        print("\nAI: 再见！期待下次聊天～")
        break
    
    if not user_input.strip():
        continue
    
    # 把用户输入加入对话历史
    messages.append({"role": "user", "content": user_input})
    
    # 调用 API（用SDK，和14一样）
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=messages
    )
    
    ai_reply = response.choices[0].message.content
    print(f"\nAI: {ai_reply}")
    
    # 把 AI 回复加入对话历史
    messages.append({"role": "assistant", "content": ai_reply})