import streamlit as st

st.title("我的第一个AI网页")
st.write("欢迎来到AI应用世界")

user_input = st.text_input("请输入你的名字")

if st.button("点击我"):
    if user_input:
        st.success(f"你好,{user_input}")
    else:
        st.warning("请先输入名字!")

with st.sidebar:
    st.header("侧边栏菜单")
    st.write("这里放导航菜单")
    option = st.selectbox("选择功能",["功能1","功能2","功能3"])
    st.write(f"你选择了:{option}")

col1,col2 = st.columns(2)
with col1:
    st.subheader("第一列")
    st.write("左边的内容")
with col2:
    st.subheader("第二列")
    st.write("右边的内容")