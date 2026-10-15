from zhipuai import ZhipuAI

client = ZhipuAI(api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr")
system_prompt="你是一个Python编程老师，用户会给你一段Python代码，你用通俗的语言解释：1.这段代码是干什么的 2.核心原理 3.关键知识点 4.可能的改进点。分点说明，清晰易懂。"

print("="*50)
print("     AI代码解释器（输入quit退出）")
print("     粘贴Python代码，AI会解释这段代码的功能和原理")
print("="*50)

while True:
    print("\n请粘贴代码（输入完后按回车，再单独输入end按回车结束）")

    code_lines = []
    while True:
        line = input()
        if line.strip().lower() == "end":
            break
        if line.strip().lower() == "quit":
            print("\n再见!")
            exit()
        code_lines.append(line)

    code = "\n".join(code_lines)

    if not code.strip():
        continue

    print("\nAI 正在分析...")

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":f"请解释这段代码:\n```python\n{code}\n```"}
        ]
    )

    print("\n"+"="*50)
    print("AI解释:")
    print("="*50)
    print(response.choices[0].message.content)