from django.db import models
from MySQLdb import connect
from MySQLdb.cursors import DictCursor


def conn():

    db = connect(
        host="192.168.1.118",
        port=3307,
        db="mysite",
        user="mysite",
        password="mysite",
        charset="utf8"
    )
    return db


def insert(user_info: dict):

    db = conn()
    cursor = db.cursor()
    sql = """insert 
               into user 
             values(
             NULL,
             '{name}',
             '{email}',
             password('{password}'),
             '{gender}',
             sysdate(),
             sysdate()
             )""".format_map(user_info)
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return result


def login(login_info: dict):

    db = conn()
    cursor = db.cursor(DictCursor)
    sql = """select no,
                    name,
                    email,
                    gender
               from user
              where 1=1
                and email="{email}"
                and password=password('{password}')""".format_map(login_info)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()

    return result


def update(update_info: dict):

    db = conn()
    cursor = db.cursor(DictCursor)
    sql = """update user 
                set name='{name}',
                    password= password('{password}'),
                    gender='{gender}'
              where 1=1
                and no={no}""".format_map(update_info)
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

    return result


def select_one(no:int):

    result = dict()
    db = conn()
    cursor = db.cursor(DictCursor)
    sql = """select no,
                    name,
                    email,
                    gender
               from user
              where 1=1
                and no={no}""".format(no=no)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    db.close()

    return result



