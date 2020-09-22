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
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result


def fetchlist(page_no):
    db = conn()
    cursor = db.cursor(DictCursor)
    page_no = (int(page_no)-1) * 5
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
           limit {page_no} , 5""".format(page_no=page_no)
    cursor.execute(sql)
    print(sql)
    result = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    return result


def select_order(board_info: dict) -> int:
    db = conn()
    cursor = db.cursor(DictCursor)

    sql = """ select min(o_no) as o_no
                from board
               where 1=1
                 and depth = (select depth 
                                from board x
                               where 1=1
                                 and no = {parent_no} )
                 and o_no >  (select o_no
                                 from board y
                                where 1=1
                                  and no = {parent_no} ) """.format_map(board_info)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result['o_no'] is None:
        sql = """select max(o_no)  as o_no 
                                 from board"""
        cursor.execute(sql)
        result = cursor.fetchone()
        update_yn = False
    else:
        update_yn = True
    print("board select order query", sql)
    cursor.close()
    db.close()
    return result, update_yn


def update_order(o_no: int) -> dict:
    db = conn()
    cursor = db.cursor()

    sql = """ update board
                 set o_no = o_no +1
                 where 1=1 
                   and o_no  >= {o_no}
                 """.format(o_no=o_no)
    result = cursor.execute(sql)
    print("board update_order query", sql)
    db.commit()
    cursor.close()
    db.close()
    return result


def insert(board_info: dict):

    sql = """insert 
              into board ( title, context, user_no, g_no, depth, o_no, register_ymdt, update_ymdt)
               values(
                       "{title}",
                       "{context}",
                       '{user_no}',
                       ifnull((select max(g_no) +1 
                                 from board
                                where 1=1), 1) as g_no,
                       1 as depth,
                       ifnull((select max(o_no) +1
                                from board
                                where 1=1),1 ) as o_no,
                       sysdate(),
                       sysdate()                        
               )""".format_map(board_info)
    print("board insert query", sql)
    db = conn()
    cursor = db.cursor()
    result = cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return result


def insertReply(board_info: dict):

    sql = """ insert 
                into board (title, context, user_no, g_no, depth, o_no, hit, register_ymdt, update_ymdt)
                values(
                "{title}",
                "{context}",
                {user_no},
                {g_no},
                {depth},
                {o_no},
                0,
                sysdate(),
                sysdate()
                )""".format_map(board_info)
    print("board insert query", sql)
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


