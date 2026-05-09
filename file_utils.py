# ============================================================
# 块1：函数定义及扩展名判断
# 队友的代码：定义了read_file函数，试图处理多种扩展名，但endswith用法错误（'.txt' or '.pdf' or '.docx' 永远为True），且只实现了txt读取。
# 没实现：正确判断扩展名、支持pdf/docx、不支持Streamlit上传对象。
# ============================================================
# def read_file(filePath):
#     if filePath.endswith('.txt' or '.pdf' or '.docx'):
#        with open (filePath,'r',encoding='utf-8') as f:content= f.read()
#        return content
#     else:
#         print('暂不支持')
#         return''
# 正确代码（支持txt/pdf/docx，接收上传文件对象）：
import io
import pdfplumber
from docx import Document

def extract_text_from_uploaded_file(uploaded_file) -> str:
    """从Streamlit上传的文件对象中提取文本内容，支持txt/pdf/docx"""
    if uploaded_file is None:
        return ""
    filename = uploaded_file.name
    content = ""
    try:
        if filename.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
        elif filename.endswith('.pdf'):
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"
        elif filename.endswith('.docx'):
            doc = Document(io.BytesIO(uploaded_file.read()))
            content = '\n'.join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("不支持的文件格式")
    except Exception as e:
        return f"文件读取错误: {str(e)}"
    return content.strip()

# ============================================================
# 块2：测试代码（队友在模块中直接调用了read_file和打印）
# 队友的代码：调用了read_file('TEST.txt')并打印前200字符，以及遍历问题列表。
# 没实现：这些代码在作为模块导入时会被执行，不适合放在全局作用域。
# 正确做法：将测试放在 if __name__ == '__main__': 块中，不影响导入。
# ============================================================
# read_file('TEST.txt')
# content = read_file('TEST.txt')
# if __name__ == '__main__':
#     rs = content[:200]
#     print('测试结果:',rs)
# 
# questions = ["什么是RAG？","如何切分文档?"]
# [print(i) for i in questions]
# 正确代码（仅自测，不会被Streamlit导入时执行）：
if __name__ == "__main__":
    print("file_utils.py 模块加载成功，可在此编写本地测试代码。")
    # 示例：如果本地有TEST.txt，可以测试提取函数（需要模拟上传对象，较复杂，略）