from django.db import models
from MySQLdb import connect
from MySQLdb.cursors import DictCursor
# Create your models here.


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


def fetchall():
    db = conn()
    cursor = db.cursor(DictCursor)
    sql = """select no,
                    name,
                    context,
                    date_format(register_ymdt, "%Y-%m-%d_%h:%i:%s") as register_date                     
               from guestbook 
           order by register_ymdt desc"""
    cursor.execute(sql)
    result = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return result


def insert(guestbook_info: dict):

    db = conn()
    cursor = db.cursor()
    sql = """insert 
               into guestbook 
             values(
             null,
             '{name}',
              password('{password}'),
             '{context}',
             sysdate()
             )""".format_map(guestbook_info)
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return result


def delete(delete_info: str):

    db = conn()
    cursor = db.cursor()
    sql = """delete 
               from guestbook 
             where 1=1
               and no = {no} 
               and password = password('{password}')
             """.format_map(delete_info)
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return result