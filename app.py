from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

SECRET_KEY = 'YOUTUVERSE'

import jwt

import datetime

import hashlib

# router
@app.route('/')
def home_page():
    token = request.cookies.get('YouTuverse_token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ['HS256'])
        print(payload)
        user = db.users.find_one({ 'user_id': payload['user_id'] })
        return render_template('index.html', user = user)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login_page', msg = '로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login_page', msg = '로그인 정보가 존재하지 않습니다.'))

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    msg = request.args.get('msg')
    return render_template('login.html', msg = msg)

@app.route('/login/pw')
def pw_find_page():
    return render_template('login_pw.html')


# APIs
# 회원가입
@app.route('/api/user/new', methods=['POST'])
def signup():
    user_id = request.form['ID']
    nickname = request.form['NICKNAME']
    pw = request.form['PW']

    is_exist = db.users.find_one({ 'user_id': user_id })
    if is_exist:
        return jsonify({ 'msg': '이미 존재하는 아이디입니다.' })

    hashed_pw = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    doc = {
        'user_id': user_id,
        'nickname': nickname,
        'password': hashed_pw,
    }

    db.users.insert_one(doc)

    return jsonify({ 'result': 'success', 'msg': '회원가입에 성공하였습니다.' })

# 로그인
@app.route('/api/user', methods=['POST'])
def login():
    user_id = request.form['ID']
    password = request.form['PW']

    user = db.users.find_one({ 'user_id': user_id }, { '_id': False })
    if user is None:
        return jsonify({ 'msg': '존재하지 않는 ID입니다.' })
    
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if hashed_password != user['password']:
        return jsonify({ 'msg': '비밀번호가 일치하지 않습니다.' })

    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return jsonify({ 'token': token })

# 비밀번호 찾기
@app.route('/api/user/password', methods=['POST'])
def find_password():
    user_id = request.form['user_id']
    new_password = request.form['password']

    user = db.users.find_one({ 'user_id': user_id}, { '_id': False } )
    if user is None:
        return jsonify({ 'msg': '존재하지 않는 ID입니다.' })

    hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
    db.users.update_one({ 'user_id': user_id }, { '$set': { 'password': hashed_password } })

    return jsonify({ 'msg': '비밀번호를 재설정하였습니다.' })

# 유튜버 좋아요 상위 3명 목록 가져오기
@app.route('/api/youtuber/top', methods=['GET'])
def show_top3_youtuber():
    youtuber = list(db.youtuber.find({}, {'_id': False}).limit(3).sort("likes", -1))

    return jsonify({'youtubers': youtuber})

# 유튜버 전체 목록 가져오기
@app.route('/api/youtuber/all', methods=['GET'])
def show_all_youtuber():
    youtuber = list(db.youtuber.find({}, {'_id': False}).sort("name"))
    return jsonify({'youtubers': youtuber})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
