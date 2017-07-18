# 为了实现中文插入，运行这个脚本之前把Python36\Lib\site-packages\pymysql\connection.py的第105行的DEFAULT_CHARSET = 'latin1'改成
import pymysql
import time


class DBService:
    # 这些是数据库连接的信息，后期改成配置文件导入的方式读取
    __dbsource = "localhost"
    __user = "root"
    __password = "1998"
    __dbname = "bmbbs"
    __db = pymysql.connect(__dbsource, __user, __password, __dbname)
    __cursor = __db.cursor()

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

    def __insertTuple(self, tuplelist: list):
        sql = "INSERT INTO " + str(tuplelist[0]) + " VALUE("
        for element in tuplelist[1:]:
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
    def updateTuple(self, table: str, editAttribute: list, selectAttribute: list):
        sql = "UPDATE %s SET " % table
        length  = len(editAttribute)
        index = 0
        while index < length:
            sql += str(editAttribute[index]) + " = '" + str(editAttribute[index + 1]) + "', "
            index += 2
        sql = sql[:-2]
        length = len(selectAttribute)
        index = 0
        sql += " WHERE "
        while index < length:
            sql += str(selectAttribute[index]) + " = '" + str(selectAttribute[index + 1]) + "' AND "
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
    def deleteTuple(self, table: str, selectAttribute: list):
        sql = "DELETE FROM %s WHERE " % table

        length =len(selectAttribute)
        index = 0

        while index < length:
            sql += str(selectAttribute[index]) + " = '" + str(selectAttribute[index + 1]) + "' AND "
            index += 2
        sql = sql[:-4]

        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            return 1
        except:
            self.__db.rollback()
            return 0



#这个版本是最初版本0.1，经过一些测试没有大bug
