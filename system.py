# encodeing:utf-8
'''
业务逻辑模块
'''

import database


class User:
    '''
    主要负责用户登陆
    '''
    @staticmethod
    def login(name, psw):
        user = database.get_user(name, psw)
        if user:
            if user["password"] == psw:
                return 0
            return 1
        return 2

    @staticmethod
    def register(name, psw):
        return database.new_account(name, psw)

    @staticmethod
    def get_user_info(name):
        return database.get_user_info(name)

    @staticmethod
    def get_user_topic(name):
        return Topic.get_user_topic(name)

    @staticmethod
    def set_icon(name, icon):
        database.set_icon(name, icon)


class Admin:
    '''
    管理员操作
    '''

    pass


class Part:
    '''
    与分区相关的操作
    '''

    @staticmethod
    def load_topics(partname):
        return database.get_topic(partname)

    @staticmethod
    def new_topic(partname, name, title, content):
        database.new_topic(partname, name, title, content)

    @staticmethod
    def get_notice(partname):
        return database.get_notice(partname)["notice"]


class Topic:
    '''
    帖子的相关操作
    '''

    @staticmethod
    def load_topic(topic_id):
        return database.get_topic_content(topic_id)

    @staticmethod
    def load_comments(topic_id):

        return database.get_comment(topic_id)

    @staticmethod
    def new_comment(topic_id, name, content):
        return database.new_comment(topic_id, name, content)

    @staticmethod
    def get_user_topic(name):
        return database.get_user_topic(name)

    @staticmethod
    def delete_topic(topic_id):
        database.delete_topic(topic_id)

    @staticmethod
    def get_topic_content(topic_id):
        return database.get_topic_content(topic_id)["content"]

    @staticmethod
    def edit_topic(topic_id, content):
        database.edit_topic(topic_id, content)
