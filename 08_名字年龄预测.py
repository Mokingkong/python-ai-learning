import requests

def predict_age(name):
    url = f"http://api.agify.io?name={name}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"请求失败，状态码:{response.status_code}")
        return None

    data = response.json()
    return data

def predict_gender(name):
    url = f"http://api.genderize.io?name={name}"
    response = requests.get(url)

    if response.status_code != 200:
            print(f"请求失败，状态码:{response.status_code}")
            return None

    data = response.json()
    return data

while True:
    name = input("\n请输入一个英文名（输入q退出）:")
    if name.lower() == 'q':
        print("886!")
        break

    age_data = predict_age(name)
    gender_data = predict_gender(name)
    print(f"age_data完整内容: {age_data}")
    print(f"gender_data完整内容: {gender_data}")

    if age_data and gender_data:
        age = age_data.get('age','unknow')
        gender = gender_data.get('gender','unknow')
        probability = gender_data.get('probability',0)

        if gender is None:
            gender_text = "Unknow"
        elif gender =='male':
            gender_text = '男'
        else:
            gender_text = '女'
        

        print(f"\n名字: {name}")
        print(f"预测年龄: {age}岁")
        print(f"预测性别: {'男' if gender == 'male' else '女'}")
        print(f"性别概率: {probability:.0%}")
    else:
        print("获取数据失败，请稍后再试")