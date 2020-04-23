from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

## API 역할을 하는 부분
@app.route('/glossary', methods=['POST'])
def glossary_post():
   # 1) 클라이언트로부터 데이터 받기
   japanese_receive = request.form['japanese_give']
   korean_receive = request.form['korean_give']
   comments_receive = request.form['comments_give']

   # 2) 1)에서 받은 데이터를 DB에 넣을 딕셔너리로 지정
   term = {'japanese_term': japanese_receive, 'korean_term': korean_receive, 'comments_term': comments_receive}

   # 3) mongoDB에 데이터 넣기
   db.terms.insert_one(term)

   return jsonify({'result':'success'})

@app.route('/glossary', methods=['GET'])
def glossary_get():
   # 모든 document 찾기 $ _id값은 출력에서 제외하기
   result = list(db.terms.find({}, {'_id': 0}))
   # terms라는 키값으로 단어정보 내려주기
   return jsonify({'result':'success', 'terms': result})

## 클라이언트로부터 요청받은 단어 삭제요청을 POST하여 mongoDB 데이터를 삭제하는 API가 필요

if __name__ == '__main__':
   app.run('127.0.0.1',port=5000,debug=True)