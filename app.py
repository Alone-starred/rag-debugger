import streamlit as st
from rag_debugger import RAGDebugger
from file_utils import extract_text_from_uploaded_file

# ============================================================
# 页面配置和可爱主题 CSS
# ============================================================
st.set_page_config(page_title="🐱 RAG 调试工具", layout="wide")

# 自定义 CSS：粉色可爱风 + 萌字体
st.markdown("""
<style>
    /* 导入 Google Fonts 中的萌字体 */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Quicksand:wght@400;600;700&display=swap');

    /* 整体背景色 */
    .stApp {
        background-color: #FFF5F8;
        font-family: 'Quicksand', 'Comic Neue', 'Comic Sans MS', sans-serif;
    }
    /* 侧边栏背景 */
    section[data-testid="stSidebar"] {
        background-color: #FFE4ED;
    }
    /* 所有标题使用 Fredoka One 字体（更圆润可爱） */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Fredoka One', 'Comic Neue', cursive !important;
        color: #D86F8C !important;
        letter-spacing: 1px;
    }
    /* 普通文字大小和颜色 */
    p, div, span, label, .stTextInput label, .stSlider label {
        font-family: 'Quicksand', 'Comic Neue', sans-serif;
        font-weight: 600;
        color: #A0526D;
    }
    /* 按钮 */
    .stButton > button {
        background-color: #F2A0B5;
        color: white;
        border-radius: 30px;
        font-size: 18px;
        font-weight: bold;
        font-family: 'Quicksand', sans-serif;
        border: none;
        padding: 0.6rem 1.5rem;
        transition: 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #D86F8C;
        transform: scale(1.02);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    /* 文本输入框 */
    .stTextInput > div > div > input {
        border-radius: 30px;
        border: 2px solid #F2A0B5;
        background-color: #FFFFFF;
        font-family: 'Quicksand', sans-serif;
        font-size: 16px;
        padding: 10px 20px;
    }
    /* 文件上传区域 */
    .stFileUploader > div {
        border: 2px dashed #F2A0B5;
        border-radius: 30px;
        background-color: #FFF0F3;
        padding: 1rem;
    }
    /* 滑块样式 */
    .stSlider > div > div > div {
        background-color: #F2A0B5;
    }
    /* 成功提示框 */
    .stSuccess {
        background-color: #FFE4ED;
        border-left-color: #D86F8C;
        color: #A0526D;
        border-radius: 20px;
        font-family: 'Quicksand', sans-serif;
    }
    /* 折叠区域标题 */
    .streamlit-expanderHeader {
        background-color: #FFE4ED;
        border-radius: 30px;
        color: #D86F8C;
        font-weight: bold;
        font-family: 'Quicksand', sans-serif;
    }
    /* 代码块背景 */
    .stCodeBlock {
        background-color: #FFFAFC;
        border-radius: 20px;
    }
    /* 侧边栏滑块标签 */
    .stSlider label {
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# 可爱的标题和副标题
st.title("🐱🌸  RAG 调试工具  🌸🐱")
st.caption("✨ 让检索增强生成变得透明 ✨")

# ============================================================
# 块2：侧边栏文件上传和参数调节（原有功能保持不变）
# ============================================================
with st.sidebar:
    st.header("⚙️ 参数设置")
    chunk_size = st.slider("chunk_size (文本切分大小)", 100, 1000, 500, 50)
    chunk_overlap = st.slider("chunk_overlap (切分重叠)", 0, 200, 50, 10)
    top_k = st.slider("top_k (检索片段数量)", 1, 5, 3, 1)
    
    st.header("📁 文档上传")
    uploaded_file = st.file_uploader("上传文档", type=["txt", "pdf", "docx"])
    if uploaded_file:
        st.success(f"已上传: {uploaded_file.name}")

# ============================================================
# 块3：问题输入和提交按钮
# ============================================================
question = st.text_input("💬 请输入您的问题", placeholder="例如：什么是RAG？")
submit = st.button("🚀 开始回答", type="primary")

if "debug_info" not in st.session_state:
    st.session_state.debug_info = None
if "answer" not in st.session_state:
    st.session_state.answer = None

# ============================================================
# 块4：按钮点击后的处理逻辑（调用 RAGDebugger）
# ============================================================
if submit:
    if not uploaded_file:
        st.warning("请先上传文档")
    elif not question.strip():
        st.warning("请输入问题")
    else:
        with st.spinner("正在处理，请稍候..."):
            text = extract_text_from_uploaded_file(uploaded_file)
            if text.startswith("文件读取错误"):
                st.error(text)
                st.stop()
            rag = RAGDebugger()
            rag.add_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            answer, debug_info = rag.query(question, top_k=top_k)
            st.session_state.answer = answer
            st.session_state.debug_info = debug_info

# ============================================================
# 块5：显示结果（答案和调试信息）
# ============================================================
if st.session_state.answer:
    st.markdown("### 🤖 回答")
    st.success(st.session_state.answer)

if st.session_state.debug_info:
    with st.expander("🔧 调试信息 (RAG 内部流程)", expanded=False):
        info = st.session_state.debug_info
        st.markdown(f"**📄 文档切分结果**：共 {len(info['chunks'])} 个片段")
        for idx, chunk in enumerate(info['chunks'][:5]):
            st.text(f"[{idx}] {chunk['content'][:100]}...")
        if len(info['chunks']) > 5:
            st.text(f"... 还有 {len(info['chunks'])-5} 个片段未显示")
        st.markdown("**🔍 检索到的片段**：")
        for i, doc in enumerate(info['retrieved_chunks']):
            score_display = f" (相似度: {doc['score']:.4f})" if doc['score'] is not None else ""
            st.markdown(f"片段 {i+1}{score_display}")
            st.text(doc['content'][:200] + ("..." if len(doc['content']) > 200 else ""))
        st.markdown("**📝 完整 Prompt**：")
        st.code(info['prompt'], language="text")
        st.markdown("**📋 完整调试信息 (JSON)**：")
        st.json(info)