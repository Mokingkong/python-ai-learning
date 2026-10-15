from fastapi import FastAPI
from pydantic import BaseModel
from langchain_zhipu import ChatZhipuAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from typing import List,Optional

app = FastAPI(title="AI助手API",version="1.0",description="基于LangChain的智能对话API接口")
llm = ChatZhipuAI(
    model="glm-4-flash",
    api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr",
    temperature=0.7
)

class ChatMessage(BaseModel):
    role:str
    content:str

class ChatRequest(BaseModel):
    message:str
    history:Optional[List[ChatMessage]] = None
    system_prompt:Optional[str] = None

class ChatResponse(BaseModel):
    reply:str
    history:List[ChatMessage]

@app.get("/")         #用来检查服务器是否在运行
def root():
    return {"name":"AI助手API","version":"1.0","status":"运行中"}

@app.post("/chat",response_model=ChatResponse)
def chat(request:ChatRequest):
    messages = []

    if request.system_prompt:
        messages.append(SystemMessage(content=request.system_prompt))
    else:
        messages.append(SystemMessage(content="你是一个友好的AI助手，用中文回答问题，简洁明了"))

    if request.history:
        for msg in request.history:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))

    messages.append(HumanMessage(content=request.message))

    response = llm.invoke(messages)
    reply = response.content

    new_history = []
    if request.history:
        new_history = request.history.copy()
    new_history.append(ChatMessage(role="user",content=request.message))
    new_history.append(ChatMessage(role="assistant",content=reply))

    return ChatResponse(reply=reply,history=new_history)

@app.post("/chat/clear")
def clear_chat():
    return {"status":"success","message":"对话已清空，请前端清除本地history"}