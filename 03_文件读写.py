import os

# ========== 练习1：写入文件 ==========
# 写一个文本文件

with open("test.txt","w",encoding="utf-8")as f:
    f.write("first  line \n")
    f.write("second line \n")
    f.write("third  line \n")

print("write complete")

#练习2：读取文件

with open("test.txt","r",encoding="utf-8")as f:
    content = f.read()
print(f"All content:\n{content}")

#line read
with open("test.txt","r",encoding="utf-8")as f:
    lines = f.readline()
print(f"read1Line:{lines}")

#逐行遍历（大文件推荐，省内存
with open("test.txt","r",encoding="utf-8")as f:
    for i,line in enumerate(f,1):
        print(f"第{i}行:{line.strip()}")

#CSV
import csv

data = [
    ["name","age","major"],
    ["Zhang 3","20","APP"],
    ["Li 4","30","Tec"],
    ["Wang 4","40","AI"],
]

with open("student.csv","w",newline="",encoding="utf-8")as f:
    writer = csv.writer(f)
    writer.writerow(data)        #writerow() VS writerows()

print("CSV write complete")

with open("student.csv","r",encoding="utf-8")as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# ========== 练习4：文件和文件夹操作 ==========

print(f"test,txt cunzai?:{os.path.exists('test.txt')}")
print(f"NOW mulu:{os.getcwd()}")

files = os.listdir(".")
py_files = [f for f in files if f.endswith(".py")]
print(f"NOW ALL mulu py files:{py_files}")

os.rename("test.txt","test_rename.txt")
print("file have been renamed")

os.remove("test_rename.txt")
print("file have been deleted")

#将一个文件夹里所有的.txt文件列出，并保存到一个名为file_list.txt的文件夹中

fileT = os.listdir(".")
txt_fileT = [f for f in fileT if f.endswith(".txt")]
print(f"ALL .txt file:{txt_fileT}")

with open("file_list.txt","w",encoding="utf-8")as f:
    for filename in txt_fileT:
        f.write(filename + "\n")
print(f"writ complete")

