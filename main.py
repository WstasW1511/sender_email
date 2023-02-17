# -*- coding: utf-8 -*-
import json

import sqlite3
from flask import render_template
from tasks import send_email_task
from flask import Flask
from flask import request
import db


def start():
    try:
        con = sqlite3.connect("send_mail.db")
        cur = con.cursor()
        result = cur.execute('SELECT * FROM users WHERE status=0')
        con.close()
    except Exception as e:
        con = sqlite3.connect("send_mail.db")
        cur = con.cursor()
        result = cur.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT ,
        surname TEXT,
        email TEXT ,
        status INTEGER)""")
        con.commit()
        result = cur.execute("""INSERT INTO users (name, surname,email, status) VALUES
                  ('Иван','Петров','ivan@gmail.ru',0),
                  ('Виктор','Сизин','vitya@gmail.ru',0),
                  ('Ирина','Петрова','ira123@gmail.ru',0),
                  ('Анна','Петрова','anna@gmail.ru',0),
                  ('Роман','Перевалов','irom@gmail.ru',0)""")
        con.commit()
        con.close()



if __name__ == '__main__':
    start()
    app = Flask(__name__,static_url_path='')

    @app.route("/send", methods=['POST'])
    def send():
        addr_to = []
        data=json.loads(request.data)
        if data == 'get_users':
            users = db.recipients()
            return users
        elif data['send_to'] == 'all':
            users = db.recipients()
            users = json.loads(users)
            for i in users:
                addr_to.append(i['email'])
        else:
            addr_to.append(data['send_to'])
        subject = data['subject']
        body_massage = data['send_text']
        for i in addr_to:
            send_email_task.delay(i,subject,body_massage)
        return ''

    @app.route("/", methods=['GET'])
    def home():
        return render_template('index.html')

    app.run(debug=True)

    # запуск селери: celery -A tasks  worker --pool=solo -l info
