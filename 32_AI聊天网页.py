import streamlit as st
from langchain_zhipu import ChatZhipuAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

st.set_page_config(page_title="AI聊天助手",page_icon="🤖",layout="wide")
st.markdown("""
<style>
/* 用户消息整体右对齐 */
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
}
/* 用户消息气泡右对齐 */
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) 
.stChatMessage-content {
    text-align: right !important;
}
</style>
""", unsafe_allow_html=True)

st.title("AI聊天助手")
st.caption("基于LangChain + 智谱AI的智能对话")

@st.cache_resource
def get_llm():
    return ChatZhipuAI(
        model="glm-4-flash",
        api_key="a9aa6f9d1b924a68a452387b60581d90.IkoeeTAlWaYcNByr",
        temperature=0.7
    )

llm = get_llm()

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="你是一个友好的AI助手，用中文回答问题，回答简洁明了")
    ]

with st.sidebar:
    st.header("设置")
    if st.button("清空对话:"):
        st.session_state.messages=[
           SystemMessage(content="你是一个友好的AI助手，用中文回答问题，回答简洁明了") 
        ]
        st.rerun()
    st.write(f"当前对话轮数:{len(st.session_state.messages) - 1}")

for msg in st.session_state.messages:
    if isinstance(msg,HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg,AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

user_input = st.chat_input("输入你的问题")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.chat_message("assistant"):
        with st.spinner("AI正在思考"):
            response = llm.invoke(st.session_state.messages)
            st.write(response.content)

    st.session_state.messages.append(AIMessage(content=response.content))