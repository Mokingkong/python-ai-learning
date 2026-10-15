name = "KingKong"
age = 22
print(f"my name{name},jin nian{age}")

a = 10
b = 3
print(f"add:{a+b},minus:{a-b},multiply:{a*b}")
print(f"whole division:{a//b},yu:{a%b},mi:{a**b}")
print(f"actl div:{a/b}")

fruits = ["apple","banana","orange","grape","peach"]
print(f"fruits num:{len(fruits)}")
print(f"first:{fruits[0]}")
print(f"last:{fruits[-1]}")  #python拥有正负索引
print(f"last2:{fruits[-2]}")
for fruit in fruits:
    print(f" -{fruits}")

#字典
student = {"name":"zhang3","age":20,"major":"app"}
for key,value in student.items():
    print(f"{key}:{value}")

score = 59
if score >= 90:
    print("excellent")
elif score >= 60:
    print("good")
else:
    print("bad")

