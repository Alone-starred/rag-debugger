import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document  # 修改这一行

load_dotenv()

class RAGDebugger:
    def __init__(self, api_key=None, base_url="https://open.bigmodel.cn/api/paas/v4/"):
        """初始化 RAGDebugger"""
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("请在 .env 文件中设置 ZHIPU_API_KEY")
        self.base_url = base_url
        
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            model="embedding-2"
        )
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            model="glm-4-flash",
            temperature=0
        )
        
        self.vectorstore = None
        self.debug_info = {
            "chunks": [],
            "retrieved_chunks": [],
            "prompt": "",
            "answer": ""
        }
    
    def add_text(self, text, chunk_size=500, chunk_overlap=50):
        """添加文本：切分、向量化、存储"""
        doc = Document(page_content=text)
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_documents([doc])
        
        self.debug_info["chunks"] = [
            {"index": i, "content": chunk.page_content, "length": len(chunk.page_content)}
            for i, chunk in enumerate(chunks)
        ]
        
        self.vectorstore = Chroma.from_documents(chunks, self.embeddings)
    
    def query(self, question, top_k=3):
        """提问：检索、生成答案，返回 (答案, 调试信息)"""
        if self.vectorstore is None:
            raise ValueError("请先调用 add_text 添加文档")
        
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
        retrieved_docs = retriever.invoke(question)
        
        self.debug_info["retrieved_chunks"] = [
            {"content": doc.page_content, "score": None}
            for doc in retrieved_docs
        ]
        
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        prompt = f"基于以下内容回答问题：\n\n{context}\n\n问题：{question}\n答案："
        self.debug_info["prompt"] = prompt
        
        answer = self.llm.invoke(prompt).content
        self.debug_info["answer"] = answer
        
        return answer, self.debug_info
    
    def get_debug_info(self):
        return self.debug_info
    
    def reset(self):
        self.vectorstore = None
        self.debug_info = {
            "chunks": [],
            "retrieved_chunks": [],
            "prompt": "",
            "answer": ""
        }


if __name__ == "__main__":
    rag = RAGDebugger()
    test_text = "RAG（检索增强生成）是一种结合信息检索和大语言模型的技术。它先从知识库中检索相关片段，再将片段与问题一起送给模型生成答案，能有效减少大模型幻觉。"
    rag.add_text(test_text)
    answer, info = rag.query("什么是RAG？")
    print(f"答案: {answer}")
    print(f"调试信息中的 chunks 数量: {len(info['chunks'])}")
    print(f"调试信息中的 retrieved_chunks 数量: {len(info['retrieved_chunks'])}")