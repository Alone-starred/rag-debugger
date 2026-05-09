# RAG 调试工具

一个用于可视化 RAG（检索增强生成）内部流程的调试工具。支持上传文档、调节切分参数、查看检索片段和相似度分数，帮助开发者理解和优化 RAG 系统。

## 功能

- 支持上传 txt、pdf、docx 文件，自动提取文本
- 可调节切分大小（chunk_size）、重叠长度（chunk_overlap）和检索数量（top_k）
- 使用 TF-IDF + 余弦相似度进行本地检索，无需外网
- 调用智谱 AI 免费模型生成答案
- 展示调试信息：
  - 文档切分结果
  - 检索到的片段及相似度分数
  - 发送给大模型的完整 Prompt
  - 最终答案
  - JSON 格式调试数据

## 技术栈

- Python 3.10+
- Streamlit
- LangChain（文本切分）
- scikit-learn（TF-IDF 检索）
- 智谱 AI API（免费模型 glm-4-flash）
- pdfplumber, python-docx（文件解析）

## 安装与运行

1. 克隆仓库
   git clone https://github.com/你的用户名/rag-debugger.git
   cd rag-debugger

2. 创建虚拟环境并激活
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows

3. 安装依赖
   pip install -r requirements.txt

4. 配置 API Key
   - 注册 智谱AI开放平台（https://open.bigmodel.cn/）（免费）
   - 在项目根目录创建 .env 文件，内容：
     ZHIPU_API_KEY=你的API密钥

5. 运行
   streamlit run app.py

## 项目结构

rag-debugger/
├── app.py              # 主界面
├── rag_debugger.py     # RAG 核心逻辑
├── file_utils.py       # 文件文本提取
├── requirements.txt    # 依赖列表
├── .env                # 密钥文件（不提交）
└── README.md           # 项目说明

## 团队分工

- [Alone-starred]：后端 RAG 核心开发（切分、检索、调试信息、API 调用）
- [not-sk]：前端界面（Streamlit）、文件提取模块

## 许可证

MIT