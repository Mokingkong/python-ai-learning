import requests

url = "http://api.agify.io?name=mike"
response = requests.get(url)

print(f"状态码:{response.status_code}")

print(f"返回文本:{response.text}")

data = response.json()
print(f"解析后的数据:{data}")
print(f"name:{data['name']}")
print(f"预测年龄:{data['age']}")
print(f"统计人数:{data['count']}")