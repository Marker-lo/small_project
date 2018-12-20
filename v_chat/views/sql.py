import pymysql


class gecMysql():
    # 初始化
    def __init__(self, host, user, pwd, dbName):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.dbName = dbName

    # 连接
    def connect(self):
        self.db = pymysql.connect(self.host, self.user, self.pwd, self.dbName)
        # 创建游标  操作数据库
        self.cursor = self.db.cursor()

    def close(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库
        self.db.close()

    # 查询一条数据    传入sql语句
    def get_one(self, sql):
        ret = None
        try:
            self.connect()
            self.cursor.execute(sql)    # 执行sql语句
            ret = self.cursor.fetchone()
            self.close()
        except:
            print("get_one errror")
        return ret

    # 查询全部数据    传入sql语句
    def get_all(self, sql):
        res = ()
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except:
            pass
        return res

    def get_all_obj(self, sql, tableName, *args):
        resList = []
        fieldList = []
        if (len(args) > 0):
            for item in args:
                fieldList.append(item)
        else:
            fieldsSql = "select COLUMN_NAME from information_schema.COLUMNS " \
                        "where table_name ='%s' and table_schema = '%s'" % (
                            tableName, self.dbName)
            print(fieldsSql)
            # 获得所有的列的名字
            fields = self.get_all(fieldsSql)
            print(fields)
            for item in fields:
                fieldList.append(item[0])

        res = self.get_all(sql)
        print(sql)
        print(res)
        for item in res:
            obj = {}
            count = 0
            for x in item:
                obj[fieldList[count]] = x
                count += 1
            resList.append(obj)
        return resList

    def insert(self, sql):
        ret = self.sql_exe(sql)
        return ret

    def sql_exe(self, sql):
        print(sql)
        ret = 0
        try:
            self.connect()
            ret = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except:
            self.db.rollback()
        return ret
