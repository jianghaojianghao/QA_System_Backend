from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector as mc
from flask_cors import CORS

from question_classifier import *
from question_parser import *
from answer_search import *
from graph_search import *
import json

'''问答类'''


class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.grapSearcher = GraphSearcher()

    def chat_main(self, sent):
        # 如果回答不出则返回这句话
        answer = '您好，您的问题我可能回答不了你！'
        # 将问题进行分类
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        # 获取问题的sql语句
        res_sql = self.parser.parser_main(res_classify)
        # 通过sql语句查询，然后获得模板句返回
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

    def graph_main(self, sent):
        default_reply = 'NotFound'

        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return default_reply

        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.grapSearcher.search_main(res_sql)
        if not final_answers:
            return default_reply
        else:
            return final_answers



# 创建flask类的实例对象
app = Flask(__name__)
CORS(app)

handler = ChatBotGraph()

@app.route('/')
def hello_world():
    conn = mc.connect(user='root', password='Jh8291398', database='test_db')
    cursor = conn.cursor()
    cursor.execute('select * from Course')
    values = cursor.fetchall()
    cursor.close()
    conn.close()

    txt = '' + str(values)

    return '<p>{}</p>'.format(txt)


@app.route('/getAnswer', methods=['GET', 'POST'])
def getAnswer():
    if request.method == 'POST':
        post_data = request.get_json()
        question = post_data.get('question')
        answer = handler.chat_main(question)
    return answer

@app.route('/getGraph', methods=['GET', 'POST'])
def getGraph():
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        question = post_data.get('question')
        answer = handler.graph_main(question)
    return json.dumps(answer)

if __name__ == '__main__':
    app.run(debug=True)
