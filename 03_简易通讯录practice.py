import os

contacts = {}

def load_contacts():
    if os.path.exists("contacts.txt"):
        with open("contacts.txt","r",encoding="utf-8")as f:
            for line in f:
                line = line.strip()
                if line:
                    whole = line.split(",")
                    part1 = whole[0]
                    part2 = whole[1]
                    contacts[part1]=part2
                    

def save_contacts():
    with open("contacts.txt","w",encoding="utf-8")as f:
        for name,phone in contacts.items():
            f.write(f"{name},{phone}")
            

def add_contact():
    name = input("input name:")
    phone = input("input phone:")
    contacts[name]=phone

def show_contacts():
    if not contacts:
        print("empty")
        return
    print("\n----- 联系人列表 -----")
    for key,value in contacts.items():
        print(f"{key}:{value}")

def delete_contact():
    name = input("input delete name:")
    if name in contacts:
        del contacts[name]
        print(f"Have been delete {name}")
    else:
        print("Not Found")

def search_contact():
    name = input("input search name:")
    if name in contacts:
        print(f"Found:{name}, {contacts[name]}")
    else:
        print("Not Found")

def main():
    load_contacts()

    while True:
        print("\n===== 简易通讯录 =====")
        print("1. 添加联系人")
        print("2. 查看所有联系人")
        print("3. 删除联系人")
        print("4. 搜索联系人")
        print("5. 退出")

        choice = input("请输入选项(1-5): ")
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            save_contacts()   # 退出前保存
            print("通讯录已保存，再见！")
            break             # 跳出while循环，结束程序
        else:
            print("无效选项，请重新输入")

# 程序入口
if __name__ == "__main__":
    main()