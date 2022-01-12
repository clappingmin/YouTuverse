from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

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
        user = db.users.find_one({'user_id': payload['user_id']})
        youtubers = list(db.youtuber.find({}, {'_id': False}).sort("name"))
        top3youtubers = list(db.youtuber.find({}, {'_id': False}).limit(3).sort("likes", -1))

        return render_template('index.html', user = user, top3youtubers = top3youtubers, youtubers=youtubers)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login_page', msg = '로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login_page', msg = '로그인 정보가 없습니다.'))

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

# URL 추가 페이지
@app.route('/urlsave')
def url_save_page():
    token = request.cookies.get('YouTuverse_token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ['HS256'])
        user = db.users.find_one({'user_id': payload['user_id']})

        return render_template('urlsave.html', user = user)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login_page', msg = '로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login_page', msg = '로그인 정보가 없습니다.'))

# 유튜버 상세페이지로 데이터 전달
@app.route('/youtuber/<name>')
def show_want_youtuber(name):
    token = request.cookies.get('YouTuverse_token')
    # name, photoURL, likes, url, videoSrc
    youtuber = db.youtuber.find_one({'name': name})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({'user_id': payload['user_id']})
        return render_template('detail.html', user = user, youtuber=youtuber)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login_page', msg = '로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login_page', msg = '로그인 정보가 없습니다.'))

# 검색 결과 페이지로 이동
@app.route('/search/<keyword>')
def search(keyword):
    token = request.cookies.get('YouTuverse_token')
    youtubers = list(db.youtuber.find({'name':keyword}, {'_id': False}).sort("likes", -1))
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({'user_id': payload['user_id']})
        return render_template('search.html', user = user, keyword=keyword, youtubers=youtubers)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login_page', msg = '로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login_page', msg = '로그인 정보가 없습니다.'))

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

# 로그아웃
@app.route('/api/user/logout', methods=['GET'])
def logout():
    return jsonify({ 'msg': 'success' })

# 비밀번호 찾기
@app.route('/api/user/password', methods=['POST'])
def find_password():
    user_id = request.form['user_id']
    new_password = request.form['password']

    user = db.users.find_one({ 'user_id': user_id }, { '_id': False })
    if user is None:
        return jsonify({ 'msg': '존재하지 않는 ID입니다.' })

    hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
    db.users.update_one({ 'user_id': user_id }, { '$set': { 'password': hashed_password } })

    return jsonify({ 'msg': '비밀번호를 재설정하였습니다.' })

# 좋아요 버튼 누르면 1개 증가하는 API
@app.route('/api/like', methods=['POST'])
def like_youtube():
    name_receive = request.form['name_give']
    a_like = db.youtuber.find_one({'name': name_receive})
    current_like = a_like['likes']
    new_like = current_like + 1
    db.youtuber.update_one({'name': name_receive}, {'$set': {'likes': new_like}})
    return jsonify({'msg': '좋아요!'})

# 유튜버 크롤링
@app.route('/api/urlsave', methods=['POST'])
def collect_youtuber_info():

    # 드라이버를 실행합니다.
    url = request.form['url_give']
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url, headers=headers)

    ##창 보이지 않기
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    s = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s, chrome_options=options)
    driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
    sleep(5)  # 페이지가 로딩되는 동안 5초 간 기다립니다.

    req = driver.page_source  # html 정보를 가져옵니다.
    driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

    # soup = BeautifulSoup(data.text, 'html.parser')
    soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

    name = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    numofSub = soup.select_one('yt-formatted-string#subscriber-count').text
    photoURL = soup.select_one('meta[property="og:image"]')['content']
    videoSrc = 'https://www.youtube.com' + soup.select_one('div#items a#thumbnail', href=True)['href']

    doc = {
        'likes': 0,
        'name': name,
        'desc': desc,
        'photoURL': photoURL,
        'videoSrc': videoSrc,
        'numofSub': numofSub,
    }

    db.youtuber.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '업로드 완료!'})
    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)