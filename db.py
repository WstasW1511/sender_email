# -*- coding: utf-8 -*-
import sqlite3
import json


def result_sql(result):
    results=[]
    for i in result:
        result = {}
        result['id'] = i[0]
        result['name'] = i[1]
        result['surname'] = i[2]
        result['email'] = i[3]
        result['status'] = i[4]
        results.append(result)
    return results


def recipients():
    try:
        con = sqlite3.connect("send_mail.db")
        cur = con.cursor()
        result=cur.execute('select * FROM users WHERE status=0')
        res=result.fetchall()
        result = result_sql(res)
        con.close()
    except Exception as e:
        print (e)

    data =json.dumps(result)
    print (type(data))
    return data


def get_user(email):
    try:
        con = sqlite3.connect("send_mail.db")
        cur = con.cursor()
        query="SELECT * FROM users WHERE email='%s'"%email
        query=query.encode('utf-8')
        result = cur.execute(query)
        res = result.fetchall()
        result = result_sql(res)
        con.close()
        print ('result=', result)
    except Exception as e:
        print(e)

    if result[0]:
        user = result[0]
    else:
        user = email
    return user
