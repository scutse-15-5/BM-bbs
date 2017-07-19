# 为了实现中文插入，运行这个脚本之前把Python36\Lib\site-packages\pymysql\connection.py的第105行的DEFAULT_CHARSET = 'latin1'改成'utf8'

import pymysql

class DBService:
    # 这些是数据库连接的信息，后期改成配置文件导入的方式读取
    __dbsource = "localhost"
    __user = "root"
    __password = "1998"
    __dbname = "bmbbs"
    __db = pymysql.connect(__dbsource, __user, __password, __dbname)
    __cursor = __db.cursor()
    #单例
    __dbService = None
    def __init__(self):
        pass
    def __new__(cls, *args, **kw):
        if not cls.__dbService:
            cls.__instance = super(DBService, cls).__new__(cls, *args, **kw)
        return cls.__instance
    # 支持输入数字和字符串

    def inserNewAccount(self, name, password):
        ifInUse = 1
        self.__cursor.execute("SELECT COUNT(*) FROM ACCOUNT WHERE NAME LIKE '%s'" % name)
        count = self.__cursor.fetchone()
        if count == 0:
            ifInUse = 0
        if ifInUse:
            new_account_tuple = ["ACCOUNT", name, password]
            return self.__insertTuple(new_account_tuple)

    def insertNewTopic(self, partname, ownername, content):
        id = time.strftime("%Y%m%d-%H%M", time.localtime())
        new_topic_tuple = ["TOPIC", partname, ownername, id, content]
        return self.__insertTuple(new_topic_tuple)

    def insertNewPart(self, partname):
        newPartTuple = ["PART", partname]
        return self.__insertTuple(newPartTuple)

    def insertNewComment(self, topicid, ownername, content):
        self.__cursor.execute("SELECT COUNT(*) FROM COMMENT WHERE TOPICID LIKE '%s'" % (topicid))
        result = self.__cursor.fetchone()
        layer = result[0][0] + 1
        newCommentTuple = ["COMMENT", topicid, ownername, layer, content]
        return self.__insertTuple(newCommentTuple)

    def insertNewNotice(self, partname, content):
        newNoticeTuple = ["NOTICE", partname, content]
        return self.__insertTuple(newNoticeTuple)

    #插入元组
    def __insertTuple(self, tupleList):
        sql = "INSERT INTO " + str(tupleList[0]) + " VALUE("
        for element in tupleList[1:]:
            sql += "'" + str(element) + "',"
        sql = sql[0:-1]
        sql += ")"
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return 1
        except:
            self.__db.rollback()
            return 0

    #修改元组
    def updateTuple(self, table, editAttri, selectFactor):
        sql = "UPDATE %s SET " % table
        length  = len(editAttri)
        index = 0
        while index < length:
            sql += str(editAttri[index]) + " = '" + str(editAttri[index + 1]) + "', "
            index += 2
        sql = sql[:-2]
        length = len(selectFactor)
        index = 0
        sql += " WHERE "
        while index < length:
            sql += str(selectFactor[index]) + " = '" + str(selectFactor[index + 1]) + "' AND "
            index += 2
        sql = sql[:-4]

        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return 1
        except:
            self.__db.rollback()
            return 0

    #删除元组
    def deleteTuple(self, table, selectFactor):
        sql = "DELETE FROM %s WHERE " % table

        length =len(selectFactor)
        index = 0

        while index < length:
            sql += str(selectFactor[index]) + " = '" + str(selectFactor[index + 1]) + "' AND "
            index += 2
        sql = sql[:-4]

        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return 1
        except:
            self.__db.rollback()
            return 0

    def selectTuple(self, table, selectAttri, selectFactor):
        sql = "SELECT "
        for element in selectAttri:
            sql += str(element) + ", "
        sql = sql[:-2] + " WHERE "

        index = 0
        while index < len(selectFactor):
            sql += str(selectFactor[index]) + " = '" + str(selectFactor[index + 1]) + "' AND "
            index += 2
        sql = sql[:-4]
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()







'''
这个版本是最初版本0.1，经过一些测试没有大bug

以下是调用这些函数的实例：
instance = DBService()
instance.insertNewAccount('name','password') 所有的插入函数都是一样的调用方法
instance.updateTuple('ACCOUNT', ['要更改的属性', ‘更新值'，.......], ['选择的属性', '选择值',......]) 选择也是一样的操作， 删除的元组不需要第一个列表
'''
