def add(a,b):
    return a+b

result = add(3,5)
print(f"3+5={result}")

def is_even(n):
    return n%2==0

print(f"4是偶数吗:{is_even(4)}")
print(f"7是偶数吗:{is_even(7)}")

def greet(name,greeting="Hello"):
    print(f"{greeting},{name}")

greet("Little Ming")
greet("Kingkong","Moring")

#练习2：列表的常用操作
numbers = [3,1,4,1,5,9,2,6]
print(f"origin:{numbers}")
print(f"min:{min(numbers)}")
print(f"max:{max(numbers)}")
print(f"sum:{sum(numbers)}")
print(f"sorted:{sorted(numbers)}")
print(f"reverse:{list(reversed(numbers))}")  #list.reverse 会修改原列表

# 列表推导式（Python特色，Java没有，重点学）
squares = [x * x for x in range(1,6)]  #x^6
print(f"1-5的平方:{squares}")

evens = [x for x in range(1,11) if x % 2 == 0]
print(f"1-10的偶数:{evens}")

#练习3：字典的常用操作
person = {"name":"zhang 3","age":20,"major":"app"}

for key in person:
    print(f"键:{key}")

for key,value in person.items():
    print(f"{key} -> {value}")
# 安全取值（键不存在时不报错，返回默认值）
grade = person.get("grade","None")
print(f"年级:{grade}")

person["grade"]="senior 3"
person["age"]=21
print(f"updated:{person}")

#练习4：字符串常用方法

text="Hello,Python World"

print(f"orgin Str:'{text}'")
print(f"delete space:'{text.strip()}'")
print(f"ALL full:'{text.upper().strip()}'")
print(f"ALL min:'{text.lower().strip()}'")
print(f"replace:'{text.replace('Python','java')}'")
print(f"Head Hello:'{text.strip().startswith('Hello')}'")
print(f"!!!split:'{text.strip().split(',')}'")
print(f"length:'{len(text.strip())}'")

# f-string的高级用法

pi = 3.1415926
print(f"pi keep 2 minnum:{pi:.2f}")
print(f"pi keep 4 minnum:{pi:.4f}")
print(f"percent:{0.856:.1%}")

Height = 1.7
Wight = 80
def bmi(weight,height):
    result = weight/(height**2)
    return result
res = bmi(Wight,Height)
print(f"BMI:{res:.2f}")