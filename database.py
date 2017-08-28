# encodeing:utf-8
'''
数据库接口模块
'''

from random import randint
import time as Time

import pymysql


SERVER = "localhost"
ADMIN = "root"
PSD = "1998"
DBNAME = "bmbbs"
CHAR = "utf8"
DB = pymysql.connect(SERVER, ADMIN, PSD, DBNAME, charset=CHAR,
                     cursorclass=pymysql.cursors.DictCursor)
CURSOR = DB.cursor()

'''
new_table样式的用于插入新元组
'''


def new_account(name, psw):
    icon = "/static/icon.jpg"
    time = Time.strftime("%Y-%m-%d %H:%M:%S", Time.localtime())
    account = ["account", name, psw, time, 'NULL', '{}'.format(icon)]
    return __new_data(account)


def new_part(partname):
    part = ["part", partname]
    return __new_data(part)


def new_topic(partname, name, title, content):
    time = Time.strftime("%Y-%m-%d %H:%M:%S", Time.localtime())
    topic_id = "t{0}{1:2d}".format(time, randint(0, 100))
    topic = ["topic", topic_id, partname, time, name, title, content]
    return __new_data(topic)


def new_comment(topic_id, name, content):
    time = Time.strftime("%Y-%m-%d %H:%M:%S", Time.localtime())
    comment_id = "c{0}{1:2d}".format(time, randint(0, 100))
    comment = ["comment", topic_id, comment_id, time, name, content]
    __new_data(comment)
    return generate_comment(name, comment_id)

'''
插入新元组的通用函数
'''


def __new_data(data):
    sql = "INSERT INTO {} VALUE(".format(data[0])

    for element in data[1:]:
        if element != 'NULL':
            sql += "'{}',".format(element)
        else:
            sql += 'NULL,'
    sql = sql[0:-1]
    sql += ")"
    print(sql)
    try:
        CURSOR.execute(sql)
        DB.commit()
        return True
    except:
        DB.rollback()
        return False


def edit_notice(partname, content):
    sql = "UPDATE partname SET notice='{}' WHERE partname='{}'".format(
        content, partname)
    return __edit_tuple(sql)


def set_icon(name, icon):
    sql = "UPDATE account SET icon='{}' WHERE name='{}'".format(icon, name)
    return __edit_tuple(sql)


def edit_topic(topic_id, content):
    sql = "UPDATE topic SET content='{}' WHERE id='{}'".format(
        content, topic_id)
    return __edit_tuple(sql)


def delete_topic(topic_id):
    sql = "DELETE FROM topic WHERE id='{}'".format(topic_id)
    return __edit_tuple(sql)


'''
更新元组的通用元素
'''


def __edit_tuple(sql):
    try:
        CURSOR.execute(sql)
        DB.commit()
        return True
    except:
        DB.rollback()
        return False


def get_notice(partname):
    sql = "SELECT notice FROM part WHERE partname='{}'".format(partname)
    return select_one(sql)


def get_user(name, psw=""):
    sql = "SELECT name, password FROM account WHERE name = '{}'".format(name)
    return select_one(sql)


def get_user_info(name):
    sql = "SELECT icon, name, signature FROM account WHERE name='{}'".format(
        name)
    return select_one(sql)


def get_user_topic(name):
    sql = "SELECT id, title, time FROM topic WHERE name='{}'"\
        "ORDER BY time DESC".format(name)
    return select_all(sql)


def get_topic(partname):
    sql = "SELECT id, title, topic.time, topic.name "\
        "FROM topic JOIN account USING (name) WHERE partname='{}' "\
        "ORDER BY topic.time DESC".format(partname)
    return select_all(sql)


def generate_comment(name, comment_id):
    sql = "SELECT icon, name, account.time as atime, signature, comment.time as ctime, content " \
        "FROM account JOIN comment USING(name) WHERE id='{}'".format(comment_id)
    result = select_one(sql)
    result["atime"] = str(result["atime"])
    result["ctime"] = str(result["ctime"])
    return result

def get_topic_content(topic_id):
    sql = "SELECT icon, name, signature, account.time, partname, title, content, topic.time "\
        "FROM topic JOIN account USING (name) WHERE id='{}' "\
        "ORDER BY topic.time DESC".format(topic_id)
    return select_one(sql)


def get_comment(topic_id):

    sql = "SELECT icon, name, signature, account.time, comment.time, content "\
        "FROM comment JOIN account USING (name) WHERE topic_id='{}' "\
        "ORDER BY comment.time DESC".format(topic_id)
    return select_all(sql)


def get_partname():
    '''
    初始化时获得所有分区
    '''

    sql = "SELECT partname FROM part"
    rowdata = select_all(sql)
    partname = list()
    for part in rowdata:
        partname.append(part["partname"])
    return partname


def select_all(sql=None):
    '''
    获取所有
    '''

    try:
        CURSOR.execute(sql)
        DB.commit()
        return CURSOR.fetchall()
    except:
        DB.rollback()
        return None


def select_one(sql=None):
    '''
    获取单条数据
    '''

    try:
        CURSOR.execute(sql)
        DB.commit()
        return CURSOR.fetchone()
    except:
        DB.rollback()
        return None


def __select_tuple(table, select_attri=None, select_factor=None):
    '''
    最初的选择函数，考虑删掉
    '''

    sql = "SELECT "

    if select_attri:
        for element in select_attri:
            sql += str(element) + ", "
            sql = sql[:-2] + ' FROM ' + str(table)
    else:
        sql = "SELECT * FROM " + str(table)

    if select_factor:
        sql += " WHERE "
        index = 0
        while index < len(select_factor):
            sql += str(select_factor[index]) + " = '" + \
                str(select_factor[index + 1]) + "' AND "
            index += 2
        sql = sql[:-4]
    CURSOR.execute(sql)
    return CURSOR.fetchall()
