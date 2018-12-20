import tornado.web


class signInHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("signIn.html")

    def post(self, *args, **kwargs):
        name = self.get_argument("name")
        pwd = self.get_argument("pwd")

        sql = "insert into chat values('%s', '%s')" % (name, pwd)
        ret = self.application.db.sql_exe(sql)
        if ret == 0:
            print("signIn error")
        else:
            self.redirect("/login")
