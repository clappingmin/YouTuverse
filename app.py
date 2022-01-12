from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

app = Flask(__name__)

client = MongoClient('52.78.133.86', 27017, username="test", password="test")
db = client.YouTubeList

# 홈화면
@app.route('/')
def home():
    youtubers = list(db.youtube.find({}, {'_id': False}))
    return render_template('prac.html', youtubers=youtubers)


# 상세페이지
@app.route('/detail/<keyword>')
def detail(keyword):
    youtubers = list(db.youtube.find({}, {'_id': False}))
    return render_template('detail.html', youtubers=youtubers, keyword=keyword)

# 좋아요 버튼 누르면 1개 증가하는 API
@app.route('/api/like', methods=['POST'])
def like_youtube():
    name_receive = request.form['name_give']
    a_like = db.youtube.find_one({'name': name_receive})
    current_like = a_like['likes']
    new_like = current_like + 1
    db.youtube.update_one({'name': name_receive}, {'$set': {'likes': new_like}})
    return jsonify({'msg': '좋아요!'})

# URL 저장
@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/api/search', methods=['POST'])
def signUp():

    # 드라이버를 실행합니다.
    url = request.form['url_give']
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url, headers=headers)

    s = Service('C:/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
    sleep(1)  # 페이지가 로딩되는 동안 5초 간 기다립니다.

    req = driver.page_source  # html 정보를 가져옵니다.
    driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

    # soup = BeautifulSoup(data.text, 'html.parser')
    soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

    name = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    numofSub = soup.select_one('yt-formatted-string#subscriber-count').text
    photoURL = soup.select_one('meta[property="og:image"]')['content']
    thumbnail_video = 'https://www.youtube.com' + soup.select_one('div#items a#thumbnail', href=True)['href']

    doc = {
        'likes': 0,
        'name': name,
        'desc': desc,
        'photoURL': photoURL,
        'thumbnail_video': thumbnail_video,
        'numofSub': numofSub,
    }

    db.youtube.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '업로드 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
