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
    nickname = 'test'
    return render_template('index.html', nickname = nickname)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')


# APIs
@app.route('/api/user/new', methods=['POST'])
def api_register():

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)