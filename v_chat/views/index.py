import tornado.websocket
import logging
import uuid
import json
import tornado.web

dict_session = {}


class baseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        print("get_current_user")
        try:
            session_id = self.get_secure_cookie("session_id")
            session_str = str(session_id, 'utf-8')
            # 返回session_id 所对应的用户的名字
            return dict_session.get(session_str)
        except:
            return None


class MainHandler(baseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index1.html")


class chatHandler(tornado.websocket.WebSocketHandler):
    user_list = []
    group = []

    def open(self):
        session_id = self.get_secure_cookie("session_id")
        data = None
        if not session_id:
            # fp = open("templates/login.html", "r")
            # data = fp.read()
            # fp.close()
            # self.write_message(data)
            # self.redirect("/login")
            # super().set_header("","HTTP/1.1 101 Switching Protocols\n
            # Server: TornadoServer/5.1.1\nDate: Tue, 13 Nov 2018 03:42
            # :27 GMT\nUpgrade: websocket\nConnection: Upgrade\nSec-We
            # bsocket-Accept: aBfDmtYWFN6W9TY4ien1FtUnGe8=")
            super().clear()

            super().redirect("/login")
        else:
            name = dict_session[str(session_id, 'utf-8')]
            user_dict = {}
            user_dict["name"] = name
            user_dict["obj"] = self

            self.group.append(name)
            self.user_list.append(user_dict)
            print(self.user_list)

            msg = "[%s]: 上线了^_^ " % (name)
            for user in self.user_list:
                data = {
                    "data": msg,
                    "user": user["name"],
                    "group": self.group
                }
                data_str = json.dumps(data)
                # 向客户端发送消息
                user["obj"].write_message(data_str)

    def on_close(self):
        name = ""
        for user in self.user_list:
            if user["obj"] == self:
                name = user["name"]
                self.user_list.remove(user)
                self.group.remove(name)

        msg = "[%s]: 下线了^_^ " % (name)
        for user in self.user_list:
            data = {
                "data": msg,
                "user": user["name"],
                "group": self.group
            }
            data_str = json.dumps(data)
            # 向客户端发送消息
            user["obj"].write_message(data_str)

    def on_message(self, message):
        msg = json.loads(message)['message']
        name = ""
        for user in self.user_list:
            if user["obj"] == self:
                name = user["name"]
                break

        for user in self.user_list:
            send_msg = "[%s]说：%s" % (name, msg)
            data = {
                "data": send_msg,
                "user": user["name"],
                "group": self.group
            }
            data_str = json.dumps(data)
            user['obj'].write_message(data_str)

    def check_origin(self, origin):
        return True


class loginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self, *args, **kwargs):
        name = self.get_argument("name")
        pwd = self.get_argument("pwd")
        print("name: %s, pwd: %s" % (name, pwd))

        sql = "select name from chat where name = '%s'" % (name)
        db = self.application.db.get_all_obj(sql, "chat", 'name')
        if db:
            sql = "select pwd from chat where name = '%s'" % (name)
            db = self.application.db.get_all_obj(sql, "chat", 'pwd')
            # print(db.get('pwd'))
            if db[0].get('pwd') == pwd:
                print("login success")

                session_id = str(uuid.uuid1())
                dict_session[session_id] = name
                self.set_secure_cookie("session_id", session_id)

                self.redirect("/")
            else:
                print("login error")
                self.redirect("/login")
        else:
            self.redirect("/signIn")
