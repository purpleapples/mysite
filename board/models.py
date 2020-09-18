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


def count():
    db = conn()
    cursor = db.cursor(DictCursor)
    sql = """select count(no)  as count            
                   from board 
               """
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result


def fetchlist(page_no):
    db = conn()
    cursor = db.cursor(DictCursor)
    sql = """select no,
                    title,
                    context,
                    user_no,
                    g_no,
                    depth,
                    o_no,
                    hit,
                    (select name 
                       from user 
                      where 1=1 
                        and no = board.user_no) as user_id,                    
                    date_format(register_ymdt, "%Y-%m-%d_%h:%i:%s") as register_date                     
               from board 
           order by g_no desc, o_no asc
           limit {page_no}, 5""".format(page_no=page_no)
    cursor.execute(sql)
    result = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return result


def select_order(board_info: dict) -> int:
    db = conn()
    cursor = db.cursor()
    sql = """ select max(order_no) as order_no
                from board
                where g_no = {g_no}
                  and depth = {depth}""".format_map(board_info)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result


def update_order(board_info: dict) -> dict:
    db = conn()
    cursor = db.cursor()
    sql = """ update board
                 set order = order +1
                 where 1=1 
                   and g_no = {g_no}
                   and order  > {order}
                 """.format_map(board_info)
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return result


def insert(board_info: dict):
    sql = """"""
    if board_info["g_no"] != 0:
        result = update_order(board_info)
        sql = """ insert 
                    into board (title, context, user_no, g_no, depth, o_no, register_ytdt, update_ymdt)
                    values(
                    "{title}",
                    "{context}",
                    {user_no},
                    {g_no},
                    {depth},
                    {o_no},
                    sysdate()
                    sysdate()
                    )""".format_map(board_info)
    else:
        sql = """insert 
               into board ( title, context, user_no, g_no, depth, o_no, register_ymdt, update_ymdt)
                values(
                        "{title}",
                        "{context}",
                        '{user_no}',
                        (select max(g_no) +1 
                           from board
                          where 1=1)
                        1 as depth,
                        (select max(o_no) 
                          from board
                          where 1=1) as o_no,
                        sysdate(),
                        sysdate()                        
                )""".format_map(board_info)
    db = conn()
    cursor = db.cursor()
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return result


def update(update_info: dict):
    db = conn()
    cursor = db.cursor()
    sql = """update board 
                set title='{title}',
                    context='{context}',
                    update_ymdt=sysdate()
              where 1=1
                and no={no}
                and user_no={user_no}""".format_map(update_info)
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return result


def update_hit(no):
    db = conn()
    cursor = db.cursor()
    sql = """update board 
                set hit = hit +1
              where 1=1
                and no={no}
                """.format(no=no)
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def select_one(no: int):
    db = conn()
    cursor = db.cursor(DictCursor)
    sql = """select no,
                    title,
                    user_no,
                    context,
                    (select name 
                       from user 
                      where 1=1 
                        and no = board.user_no) as user_id,
                    date_format(register_ymdt, "%Y-%m-%d_%h:%i:%s") as register_date
               from board 
              where 1=1
                and no={no}""".format(no=no)
    cursor.execute(sql)
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return result


def delete(no: int):
    db = conn()
    cursor = db.cursor()
    sql = """delete 
               from board
              where 1=1
                and no={no}""".format(no=no)
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return result


