from zhipuai import ZhipuAI

client = ZhipuAI(api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr")

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {"role":"user","content":"你好,请用一句话介绍你自己"}
    ]
)

print("AI回复:",response.choices[0].message.content)