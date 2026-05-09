import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

class RAGDebugger:
    def __init__(self, api_key=None, base_url="https://open.bigmodel.cn/api/paas/v4/"):
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("请在 .env 文件中设置 ZHIPU_API_KEY")
        self.base_url = base_url
        
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            model="glm-4-flash",
            temperature=0
        )
        
        self.chunks = []           # 存储切分后的文本片段
        self.vectorizer = None     # TF-IDF 向量化器
        self.chunk_vectors = None  # 所有片段的 TF-IDF 向量矩阵
        self.debug_info = {
            "chunks": [],
            "retrieved_chunks": [],
            "prompt": "",
            "answer": ""
        }
    
    def add_text(self, text, chunk_size=500, chunk_overlap=50):
        # 切分文本
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        doc = Document(page_content=text)
        chunks = splitter.split_documents([doc])
        
        # 提取文本内容
        self.chunks = [chunk.page_content for chunk in chunks]
        
        # 记录调试信息
        self.debug_info["chunks"] = [
            {"index": i, "content": chunk.page_content, "length": len(chunk.page_content)}
            for i, chunk in enumerate(chunks)
        ]
        
        # 构建 TF-IDF 向量矩阵
        self.vectorizer = TfidfVectorizer()
        self.chunk_vectors = self.vectorizer.fit_transform(self.chunks)
    
    def query(self, question, top_k=3):
        if not self.chunks:
            raise ValueError("请先调用 add_text 添加文档")
        
        # 将问题转换为 TF-IDF 向量
        question_vec = self.vectorizer.transform([question])
        
        # 计算相似度
        similarities = cosine_similarity(question_vec, self.chunk_vectors).flatten()
        
        # 获取 top_k 个最相关片段的索引
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # 记录检索到的片段及相似度分数
        retrieved = []
        for idx in top_indices:
            retrieved.append({
                "content": self.chunks[idx],
                "score": float(similarities[idx])
            })
        self.debug_info["retrieved_chunks"] = retrieved
        
        # 构建 Prompt
        context = "\n\n".join([item["content"] for item in retrieved])
        prompt = f"基于以下内容回答问题：\n\n{context}\n\n问题：{question}\n答案："
        self.debug_info["prompt"] = prompt
        
        # 生成答案
        answer = self.llm.invoke(prompt).content
        self.debug_info["answer"] = answer
        
        return answer, self.debug_info
    
    def get_debug_info(self):
        return self.debug_info
    
    def reset(self):
        self.chunks = []
        self.vectorizer = None
        self.chunk_vectors = None
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
    print(f"检索到的片段数量: {len(info['retrieved_chunks'])}")
    for i, chunk in enumerate(info['retrieved_chunks']):
        print(f"片段{i+1} 相似度: {chunk['score']:.4f}")