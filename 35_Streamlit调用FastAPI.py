import streamlit as st
import requests
#后端API地址
API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="AI聊天（前后端分离版）",page_icon="🤖",layout="wide")

st.title("AI聊天助手（前后端分离版）")
st.caption("Streamlit前端 + FastAPI后端,通过HTTP接口通信")#caption是小号灰色说明文字

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("设置")
    if st.button("清空对话"):
        st.session_state.messages = []
        st.rerun()
    st.write(f"当前对话轮数:{len(st.session_state.messages) // 2}")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("输入你的问题")

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI正在思考"):
            try:
                payload = {
                 "message":user_input,
                 "history":st.session_state.messages[:-1] #获取除了最后一条
                }
                response = requests.post(API_URL,json=payload)
                response.raise_for_status()
                result = response.json()

                ai_reply = result["reply"]
                st.write(ai_reply)
                st.session_state.messages.append({"role":"assistant","content":ai_reply})
            except requests.exceptions.ConnectionError:
                st.error("无法连接后端API，请确认FastAPI已启动")
            except Exception as e:
                st.error(f"调用API出错：{e}")