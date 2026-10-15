from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="我的第一个API",version="1.0")

@app.get("/")
def root():
    return {"message":"Hellp,FastAPI","status":"success"}

@app.get("/hello")
def hello(name:str = "朋友"):
    return {"message":f"你好,{name}!","greeting":True}

class UserInput(BaseModel):
    text:str
    age: int = 0

@app.post("/echo")
def echo_data(user:UserInput):
    return {
        "你发的文字":user.text,
        "你的年龄":user.age,
        "处理结果":f"收到！你说的是'{user.text}',今年{user.age}岁"
    }

@app.get("/users/{user_id}")
def get_user(user_id:int):
    users = {1:"小明",2:"小红",3:"小刚"}
    name = users.get(user_id,"未知用户")
    return {"user_id":user_id,"name":name}