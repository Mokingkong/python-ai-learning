import requests

def predict_age(name):
    url = f"https://api.agify.io?name={name}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    return None

def predict_gender(name):
    url = f"https://api.genderize.io?name={name}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    return None

print("===== 名字信息预测器 =====")
while True:
    name = input("\n请输入英文名（输入q退出）: ")
    if name.lower() == 'q':
        print("再见！")
        break
    
    age_data = predict_age(name)
    gender_data = predict_gender(name)
    
    if age_data and gender_data and age_data['age']:
        gender_cn = '男' if gender_data['gender'] == 'male' else '女'
        print(f"\n名字: {name}")
        print(f"预测年龄: {age_data['age']} 岁")
        print(f"预测性别: {gender_cn}")
        print(f"性别概率: {gender_data['probability']:.0%}")
    else:
        print(f"\n未能预测 {name} 的信息（可能是名字太少见）")