from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.youtuverse


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# 유튜버 전체 목록 가져오기
@app.route('/api/youtuber/all', methods=['GET'])
def show_all_youtuber():
    youtuber = list(db.youtuber.find({}, {'_id': False}).sort("name"))

    return jsonify({'youtubers': youtuber})


# 유튜버 좋아요 상위 3명 목록 가져오기
@app.route('/api/youtuber/top', methods=['GET'])
def show_top3_youtuber():
    youtuber = list(db.youtuber.find({}, {'_id': False}).limit(3).sort("likes", -1))

    return jsonify({'youtubers': youtuber})






if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
