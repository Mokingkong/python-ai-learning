class Student:
    def __init__(self,name,age,major):
        self.name = name
        self.age = age
        self.major = major
        self.grades = {}

    def introduce(self):
        print(f"我叫{self.name},今年{self.age}岁，专业是{self.major}")

    def add_grade(slef,subject,score):
        slef.grades[subject] = score

    def average_grade(self):
        if not self.grades:
            return 0
        return sum(self.grades.values())/len(self.grades)

    def __str__(self):
        return f"Student(name={self.name},age={self.age},major={self.major})"


s1 = Student("ZhangSan",20,"APP")
s1.introduce

s1.add_grade("High Math",90)
s1.add_grade("English",85)
s1.add_grade("Python Design",75)

print(f"各科成绩:{s1.grades}")
print(f"平均分:{s1.average_grade()}")
print(s1)


print(f"姓名:{s1.name}")
s1.age = 21
print(f"修改后年龄:{s1.age}")

# ========== 3. 继承 ==========

class GraduateStudent(Student):
    def __init__(self,name, age, major,advisor):
        super().__init__(name, age, major)
        self.advisor = advisor

    def introduce(self):
        super().introduce()
        print(f"我的导师是:{self.advisor}")

    def research(self,topic):
        print(f"{self.name}正在研究{topic}")


s2 = GraduateStudent("LiSi",25,"AI","Prof Wang")
s2.introduce()
s2.add_grade("深度学习",95)
print(f"{s2.name}的平均分:{s2.average_grade():.1f}")
s2.research("大语言模型")

class Dog:
    species = "犬科动物"
    count = 0

    def __init__(self,name):
        self.name = name
        Dog.count += 1

    @classmethod
    def get_count(cls):
        return cls.count

    @staticmethod
    def bark():
        print("汪汪汪！")

d1 = Dog("旺财")
d2 = Dog("大黄")
d3 = Dog("小白")

print(f"狗的物种:{Dog.species}")
print(f"创建了{Dog.get_count()}只狗")

# ========== 5. 自己练习 ==========

class Shape:
    def __init__(self):
        pass

    def area(self):
        return 0

class Circle(Shape):
    def __init__(self,radius):
        super().__init__()
        self.radius = radius

    def area(self):
        result = 3.14159 * self.radius**2
        return result

class Rectangle(Shape):
    def __init__(self,side1,side2):
        super().__init__()
        self.long = side1
        self.width = side2

    def area(self):
        result = self.long * self.width
        return result


c = Circle(5)
r = Rectangle(3,4)
print(f"圆面积: {c.area():.2f}")
print(f"矩形面积: {r.area():.2f}")