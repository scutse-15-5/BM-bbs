# encoding: utf-8
import urllib.parse
import os

import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.websocket
from tornado.options import define, options

import system
import database

'''
用户认证的基类
'''


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        if not self.get_cookie("_xsrf"):
            self.clear_all_cookies()
            return None
        username = self.get_secure_cookie("name")
        if username:
            return username.decode()
        return None


class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('main.html', parts=parts,
                    page={'title': 'welcome to BMBBS!'})


class PartHandler(BaseHandler):
    def get(self):
        partname = urllib.parse.unquote(self.get_argument('partname'))
        notice = system.Part.get_notice(partname)
        topics = system.Part.load_topics(partname)

        self.render('part.html', parts=parts, topics=topics, notice=notice,
                    page={'title': partname})

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        partname = urllib.parse.unquote(self.get_argument('partname'))
        title = self.get_argument("title")
        content = self.get_argument('content')
        system.Part.new_topic(partname, user, title, content)
        self.write("succeed")


class TopicHelper(object):
    callbacks = []

    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)

    def add_comment(self, new_comment):
        for callback in self.callbacks:
            callback(new_comment)


class TopicWebSocket(tornado.websocket.WebSocketHandler):
    #users =user()

    def open(self):
        self.application.topic_helper.register(self.callback)
    def on_close(self):
        self.application.topic_helper.unregister(self.callback)

    def on_message(self):
        pass

    def callback(self, comment):
        self.write_message(comment)


class TopicHandler(BaseHandler):
    def get(self):
        topic_id = urllib.parse.unquote(self.get_argument('id'))
        topic = system.Topic.load_topic(topic_id)
        comments = system.Topic.load_comments(topic_id)
        self.render('topic.html', parts=parts, topic=topic, comments=comments,
                    page={'title': topic["title"]})

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        topic_id = urllib.parse.unquote(self.get_argument('id'))
        content = self.get_argument('content')
        new_comment = system.Topic.new_comment(topic_id, user, content)
        self.application.topic_helper.add_comment(new_comment)
        self.write("succeed")


'''
登陆注册如果成功会进入用户界面， 失败页面会刷新
'''


class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/user")
        else:
            self.render("login.html")

    def post(self):
        name = self.get_argument("name")
        psw = self.get_argument("password")
        rep_psw = self.get_argument("repPassword", None)
        if rep_psw:
            if rep_psw != psw:
                self.redirect("/login")
            elif system.User.register(name, psw):
                self.set_secure_cookie("name", name)
                self.set_secure_cookie("psw", psw)
                self.redirect("/user")
            else:
                self.redirect("/login")

        else:
            if system.User.login(name, psw) == 0:
                self.set_secure_cookie("name", name)
                self.set_secure_cookie("psw", psw)
                self.redirect("/user")
            else:
                self.redirect("/login")


class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_info = system.User.get_user_info(self.current_user)
        if user_info:
            topics = system.User.get_user_topic(self.current_user)
            self.render("user.html", parts=parts, user=user_info, topics=topics,
                        page={"title": self.current_user, })
        else:
            self.clear_all_cookies()
            self.redirect("/login")

    @tornado.web.authenticated
    def post(self):
        topic_id = self.get_argument("id")
        status = self.get_argument("status")
        if status == "0":
            system.Topic.delete_topic(topic_id)
        elif status == "1":
            content = system.Topic.get_topic_content(topic_id)
            self.write(content)
        elif status == "2":
            content = self.get_argument("content")
            system.Topic.edit_topic(topic_id, content)


class IconHandler(BaseHandler):
    def get(self):
        self.redirect("/user")

    @tornado.web.authenticated
    def post(self):
        name = self.current_user
        icon = self.get_argument("icon")
        system.User.set_icon(name, icon)


class TopicModule(tornado.web.UIModule):
    def render(self, topic, part):
        return self.render_string("modules/topicTuple.html", topic=topic, partname=part)


class CommentModule(tornado.web.UIModule):
    def render(self, comment):
        return self.render_string("modules/commentTuple.html", comment=comment)


class UserTopicModule(tornado.web.UIModule):
    def render(self, topic):
        return self.render_string("modules/userTopicTuple.html", topic=topic)


class Application(tornado.web.Application):
    def __init__(self):

        self.topic_helper = TopicHelper()

        handlers = [
            (r'/', MainPageHandler),
            (r'/part/', PartHandler),
            (r'/topic/', TopicHandler),
            (r'/login', LoginHandler),
            (r'/user', UserHandler),
            (r'/icon', IconHandler),
            (r'/topic/websocket', TopicWebSocket)
        ]
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "ui_modules": {"Topic": TopicModule,
                           "Comment": CommentModule,
                           "UserTopic": UserTopicModule},
            "login_url": "/login",
            "xsrf_cookies": True,
            "autoescape": None,
            "debug": True
        }
        tornado.web.Application.__init__(self, handlers, **settings)


define("port", default=8000, help="run on the given port", type=int)

if __name__ == "__main__":
    options.parse_command_line()

    parts = database.get_partname()

    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
