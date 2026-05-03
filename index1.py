import streamlit as st


st.title("知识问答助手")

uploaded_file = st.sidebar.file_uploader(label='上传文件',type=['txt'])
def extract_text(uploaded_file):

    if uploaded_file is not None:
        content = uploaded_file.read().decode('utf-8')
        return content
    else:
        return ''


que = st.text_input(label='小助手',placeholder='请输入您的问题')
btn = st.button(label='提交')
if btn:
    f = extract_text(uploaded_file)
    if que.strip() == '':
        st.warning('请输入您的问题')
    elif not f:
        st.warning('请上传文件')

    else:
        st.success('提交成功')
        st.markdown(f'您的问题是:,{que}')
        st.write(f[:200])


