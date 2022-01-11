from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# id, name, photoURL, likes, url, videoSrc

doc = {
    'id': 'like99',
    'name': '라이크가 99',
    'photoURL': 'https://t1.daumcdn.net/cfile/tistory/24283C3858F778CA2E',
    'likes': 99,
    'url' : 'https://www.youtube.com/c/%EC%83%BE%EC%9E%89ing',
    'videoSrc' : 'https://youtu.be/tjDJS-2RE-k'
}

db.youtuber.insert_one(doc)
