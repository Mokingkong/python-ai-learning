# ========== 1. 异常处理：try-except（对应Java的try-catch） ==========
# def divide(a, b):
#     try:
#         result = a/b
#         return result
#     except ZeroDivisionError:
#         print("错误：除数不能为0")
#         return None
#     except TypeError:
#         print("错误：输入类型不对")
#         return None
#     finally:
#         pass

# print(f"10/2 = {divide(10,2)}")
# print(f"10/0 = {divide(10,0)}")
# print(f"10/a = {divide(10,a)}")

# ========== 2. 捕获通用异常 + 获取错误信息 ==========

# def read_file_safe(filename):
#     try:
#         with open(filename,"r",encoding="utf-8")as f:
#             return f.read()
#     except Exception as e:
#         print(f"读取文件失败:{e}")
#         return None

# content = read_file_safe("不存在的文件.txt")
# print(f"读取结果:{content}")

# def check_age(age):
#     if age < 0 :
#         raise ValueError("年龄不能为负数")
#     if age > 150:
#         raise ValueError("NB长寿人")
#     return age

# try:
#     check_age(-5)
# except ValueError as e:
#     print(f"捕获到异常:{e}")

# ========== 4. 模块导入 ==========
# 方式1：导入整个模块
import math
# print({math.pi})
# print({math.sqrt(16)})
# print({math.ceil(3.2)})
# print({math.floor(3.8)})
# from random import randint,choice
# print(f"随机整数(1-100):{randint(1,100)}")
# print(f"随机选择:{choice(['Apple','Banana','orange','grape'])}")

# import datetime as dt
# now = dt.datetime.now()
# print(f"NOW TOME:{now.strftime('%Y-%m-%d %H:%M:%S')}")

# import sys
# print(f"Python version:{sys.version}")
# print(f"当前平台:{sys.platform}")

def input_int(prompt):
    while True:
        try:
            result = int(input(prompt))
            return result
        except ValueError:
            print("Not int")

age = input_int("请输入你的年龄: ")
print(f"你的年龄是: {age}")

score = input_int("请输入你的分数: ")
print(f"你的分数是: {score}")
    