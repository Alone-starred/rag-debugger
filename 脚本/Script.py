#建立函数
def read_file(filePath):
    if filePath.endswith('.txt' or '.pdf' or '.docx'):
       with open (filePath,'r',encoding='utf-8') as f:content= f.read()#文本读取
       return content#取出结果
    #    print(content)
    else:
        print('暂不支持')
        return''

read_file('TEST.txt')

#测试
content = read_file('TEST.txt')
if __name__ == '__main__':
    rs = content[:200]
    print('测试结果:',rs)

questions = ["什么是RAG？","如何切分文档?"]
# # for i in questions:
# #     print(i)

[print(i) for i in questions]






