from zhipuai import ZhipuAI

client = ZhipuAI(api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr")

prompts = {
    "1": {
        "name": "小红书种草笔记",
        "system": "你是一个小红书爆款文案博主，擅长写种草笔记。要求：标题吸引人（带emoji），正文活泼口语化，多用emoji，每段不超过3行，结尾加3-5个话题标签。用户给你产品信息，你输出完整文案。"
    },
    "2": {
        "name": "朋友圈文案",
        "system": "你是一个朋友圈文案高手，写的文案真实自然，像朋友分享，不生硬。要求：简短（100字以内），有感染力，适当用emoji，结尾可以加互动提问。用户给你产品信息，你输出朋友圈文案。"
    },
    "3": {
        "name": "淘宝商品标题",
        "system": "你是一个淘宝电商标题专家，擅长写搜索流量高的商品标题。要求：标题30字以内，包含核心关键词、品牌词、属性词、卖点词，符合淘宝搜索规则，不要有废话和特殊符号。用户给你产品信息，你输出3个不同的标题选项。"
    },
    "4": {
        "name": "短视频口播脚本",
        "system": "你是一个短视频脚本编剧，擅长写15-30秒的口播脚本。要求：开头3秒抓眼球，中间讲卖点，结尾引导互动。格式：【画面】+【口播】，口语化，有节奏感。用户给你产品信息，你输出完整脚本。"
    }
}

print("=" * 50)
print("  AI 文案生成器")
print("=" * 50)

while True:
    print("\n请选择文案类型:")
    for key,value in prompts.items():
        print(f"    {key}.{value['name']}")
    print("     0. 退出程序")

    choice = input("\n请输入编号:").strip()

    if choice=="0":
        print("\n再见!")
        break

    if choice not in prompts:
        print("输入有误，请重新选择")
        continue

    selected = prompts[choice]
    print(f"\n已选择:{selected['name']}")

    product = input("\n产品名称").strip()
    selling_points = input("产品卖点（逗号分隔）:").strip()
    target = input("目标人群:").strip()

    if not product or not selling_points:
        print("产品名称和产品卖点不能为空")
        continue

    user_input = f"产品名称:{product}\n产品卖点:{selling_points}"
    if target:
        user_input +=f"\n目标人群：{target}"

    print(f"\nAI 正在生成{selected['name']}...")

    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role":"system","content":selected["system"]},
                {"role":"user","content":user_input}
            ],
            temperature=0.8,
            timeout=30
        )

        result = response.choices[0].message.content

        print("\n" + "=" * 50)
        print(f"  生成的{selected['name']}:")
        print("=" * 50)
        print(result)
        print("=" * 50)

        while True:
            again = input("\n是否在来一版不同风格？（y/n）:").strip().lower()
            if again == "y":
                response2 = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[
                        {"role":"system","content":selected["system"]},
                        {"role":"user","content":user_input}
                    ],
                    temperature=0.9,
                    timeout=30
                )
                print("\n" + "=" * 50)
                print(" 第二版： ")
                print("="*50)
                print(response2.choices[0].message.content)
                print("="*50)
                break
            elif again == "n":
                break
            else:
                print("请输入y或n")

    except Exception as e:
        print(f"\n出错了:{e}")
        print("可能是网络超时或API额度问题，重试以下。")