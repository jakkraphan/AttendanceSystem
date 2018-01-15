import pymysql
from utils import JsonExtendEncoder
import json

class EM(object):
    def __init__(self):
        self.user_id = 0
        self.password = 0
        self.name = 0
        self.info = 0
        self.department = 0
        self.is_login = False
        self.con = 0

    def login(self, json):
        user_id = json["user_id"]
        password = json["password"]
        self.con = Connect("localhost", "root", "123654", "attendance")
        result = self.con.select(self.con.select_sql("*", "user", str(
            "user_id = " + user_id + " and " + " password = '" + password + "' and d_id>2")))

        if len(result) > 0:
            self.is_login = True
            for user in result:
                self.user_id = user[0]
                self.department = user[1]
                self.password = user[2]
                self.name = user[3]
                self.info = user[4]
                self.con.insert({"table": "log", "args": {"user_id": self.user_id, "info": "login"}})
        else:
            self.is_login = False
        self.con.close()
        return result

    def change_info(self, attr):
        if self.is_login:
            self.con = Connect("localhost", "root", "123654", "attendance")
            for k in attr.keys():
                if hasattr(self, k):
                    setattr(self, k, attr[k])
            self.con.update({"table": "user", "key": {"user_id": self.user_id}, "args": attr})
            self.con.insert({"table": "log", "args": {"user_id": self.user_id, "info": "modify_user"}})
            self.con.close()
            return True
        return False

    def attendance_search(self, json1):
        if self.is_login:
            start = json1["start"]
            end = json1["end"]
            user_id = self.user_id
            if self.is_login:
                self.con = Connect("localhost", "root", "123654", "attendance")
                sql = self.con.select_sql("*", "attendance_table", "user_id =" + str(user_id))
                if start != -1:
                    sql = sql + " and m_date>='" + str(start) + "'"
                if end != -1:
                    sql = sql + " and m_date<='" + str(end) + "'"
                sql = sql + " order by m_date DESC"
                print(sql)
                results = self.con.select(sql)
                results=json.loads(json.dumps(results,cls=JsonExtendEncoder))                
                self.con.close()
                return results

    def tl_search(self, json1):
        if self.is_login:
            #json = {"table": "trip_table", "order": [["begin"], ["asc"]], "days": {"min": 0/, "max": -1}}
            table = json1["table"]
            min_days = json1["days"]["min"] - 1
            max_days = json1["days"]['max'] - 1
            k_order = json1["order"][0]
            v_order = json1["order"][1]
            # d_order=json["order"]["days"]
            self.con = Connect("localhost", "root", "123654", "attendance")
            sql = self.con.select_sql("*", table, str("user_id =" + str(self.user_id)))
            if self.is_login:
                if max_days <= -2:
                    sql = sql + " and (end_time-begin_time)>=" + str(min_days)
                else:
                    sql = sql + " and (end_time-begin_time)>=" + str(min_days) + " and (end_time-begin_time)<= " + str(
                        max_days)
                sql = sql + " order by "
                for index in range(len(k_order)):
                    sql += str(k_order[index] + " " + v_order[index] + ",")
                sql = sql[:-1]
                print(sql)
                results = self.con.select(sql)
                results=json.loads(json.dumps(results,cls=JsonExtendEncoder))                
                self.con.close()
                return results

    def d_search(self, json1):
        if self.is_login:
            if self.department <= 2:
                did = json1["d_id"]
            else:
                did = self.department
            name = json1["d_name"]
            k_order = json1["order"][0] # asc
            v_order = json1["order"][1] # 
            self.con = Connect("localhost", "root", "123654", "attendance")
            sql = self.con.select_sql("*", "department", "")
            if did > 0:
                sql = sql + " d_id=" + str(did)
            else:
                sql = sql + " d_id > 1"
            sql = sql + " order by "
            for index in range(len(k_order)):
                sql += str(k_order[index] + " " + v_order[index] + ",")
            sql = sql[:-1]
            results = self.con.select(sql)
            self.con.close()
            return results

    def insert(self, json):  # 保存
        # json = {"table": "trip_table","args": {"status": 2}}
        print('want to insert\n')
        if self.is_login:
            log = json["log"]
            self.con = Connect("localhost", "root", "123654", "attendance")
            reply = self.con.insert(json)
            if log == "add_user":
                self.con.insert({"table": "log", "args": {"user_id": self.user_id, "info": log}})
            self.con.close()
            return reply

    def update(self, json):  # 修改，提交，签到，签出
        # json = {"table": "trip_table", "key": {"number": 1}, "args": {"status": 2},"log":}
        if self.is_login:
            self.con = Connect("localhost", "root", "123654", "attendance")
            reply = self.con.update(json)
            log = json["log"]
            if log in ["submit_leave", "submit_trip", "checkin", "checkout", "modify_user", "reject_leave", "approve_leave",
                       "reject_trip", "approve_trip"]:
                self.con.insert({"table": "log", "args": {"user_id": self.user_id, "info": log}})
            self.con.close()
            return reply


class Manager(EM):
    def __init__(self):
        EM.__init__(self)

    def login(self, json):
        user_id = json["user_id"]
        password = json["password"]
        self.con = Connect("localhost", "root", "123654", "attendance")
        sql = "(" + self.con.select_sql("user.*", "user,manage", "user.user_id = manage.user_id") + ") as tmp"
        sql2 = self.con.select_sql("*", sql, str("user_id = " + user_id + " and " + " password = '" + password + "'"))
        print(sql2)
        result = self.con.select(sql2)

        if len(result) > 0:
            self.is_login = True
            for user in result:
                self.user_id = user[0]
                self.department = user[1]
                self.password = user[2]
                self.name = user[3]
                self.info = user[4]
        else:
            self.is_login = False
        self.con.close()
        return result

    def e_search(self, json):
        if self.is_login:
            if self.department <= 2:
                did = json["d_id"]
            else:
                did = self.department
            name = json["name"]
            user_id = json["user_id"]
            k_order = json["order"][0]
            v_order = json["order"][1]
            self.con = Connect("localhost", "root", "123654", "attendance")
            sql = self.con.select_sql("*", "user", "")
            if did > 0:
                sql = sql + " d_id=" + str(did)
            else:
                sql = sql + " d_id >1"
            if user_id >= 0:
                sql = sql + " and user_id = " + str(user_id)
            if name != -1:
                sql = sql + " and name = '" + str(name) + "'"
            sql = sql + " order by "
            for index in range(len(k_order)):
                sql += str(k_order[index] + " " + v_order[index] + ",")
            sql = sql[:-1]
            print(sql)
            results = self.con.select(sql)
            self.con.close()
            return results

    def tl_search(self, json1):  # 为更高级的权限服务
        # json = {"table": "", "status": 1, "did": 1, "start": 1, "end": 1, "user_id": 1, "name": 1,
        #         "days": {"min": 1, "max": -1},
        #         "order": [["begin"], ["asc"]]}
        if self.is_login:
            if self.department <= 2:
                did = json1["d_id"]
            else:
                did = self.department
            status = json1["status"]
            user_id = json1["user_id"]
            table = json1["table"]
            name = json1["name"]
            start = json1["start"]
            end = json1["end"]
            m_type = json1["type"]
            min_days = json1["days"]["min"] - 1
            max_days = json1["days"]['max'] - 1
            k_order = json1["order"][0]
            v_order = json1["order"][1]
            self.con = Connect("localhost", "root", "123654", "attendance")
            sql = self.con.select_sql("*", table + ",user ", str(table) + ".user_id =user.user_id")
            if user_id >= 0:
                sql = sql + " and user.user_id = " + str(user_id)
            if name != -1:
                sql = sql + " and name = '" + str(name) + "'"
            if status != -1:
                sql = sql + " and status = " + str(status)
            if m_type != -1:
                sql = sql + " and m_type = " + str(m_type)
            if start != -1:
                sql = sql + " and begin_time>= '" + str(start) + "'"
            if end != -1:
                sql = sql + " and end_time<= '" + str(end) + "'"
            sql = sql + " and (end_time-begin_time)>= " + str(min_days)
            if max_days != -2:
                sql = sql + " and (end_time-begin_time)<= " + str(max_days)
            if did > 0:
                sql = sql + " and d_id=" + str(did)
            else:
                sql = sql + " and d_id >1"
            sql = sql + " order by "
            for index in range(len(k_order)):
                sql += str(k_order[index] + " " + v_order[index] + ",")
            sql = sql[:-1]
            print(sql)
            results = self.con.select(sql)
            results=json.loads(json.dumps(results,cls=JsonExtendEncoder))            
            self.con.close()
            return results

    def attendance_search(self, json1):  # 时间段 指定部门 制定工号 指定姓名  指定类型（状态）
        # json = {"status": 1, "did": 1, "start": 1, "end": 1, "user_id": 1, "name": 1,
        #         "order": {"did": 1, "start": 1, "end": 1, "user_id": 1, "name": 1, "status": 1, "days": 1}}
        if self.is_login:
            if self.department <= 2:
                did = json1["d_id"]
            else:
                did = self.department
            status = json1["status"]
            user_id = json1["user_id"]
            name = json1["name"]
            start = json1["start"]
            end = json1["end"]
            k_order = json1["order"][0]
            v_order = json1["order"][1]
            self.con = Connect("localhost", "root", "123654", "attendance")
            sql = self.con.select_sql("*", "attendance_table, user ", "attendance_table.user_id = user.user_id")
            if user_id >= 0:
                sql = sql + " and user.user_id = " + str(user_id)
            if name != -1:
                sql = sql + " and name = '" + str(name) + "'"
            if status != -1:
                sql = sql + " and status = " + str(status)
            if start != -1:
                sql = sql + " and m_date>= '" + str(start) + "'"
            if end != -1:
                sql = sql + " and m_date<= '" + str(end) + "'"
            if did > 0:
                sql = sql + " and d_id=" + str(did)
            else:
                sql = sql + " and d_id >1"
            sql = sql + " order by "
            for index in range(len(k_order)):
                sql += str(k_order[index] + " " + v_order[index] + ",")
            sql = sql[:-1]
            print(sql)
            results = self.con.select(sql)
            results=json.loads(json.dumps(results,cls=JsonExtendEncoder))
            # for x in results

            self.con.close()
            return results

    def sum_a_search(self, json):  # 这里总的早退天数逃不掉了，按工号和状态先group count 一遍,要不要再按照部门待定，
        # json={"group":""}#date status  user_id name d_id
        # sql="select * from "
        if self.is_login:
            group = json["group"]
            if self.department <= 2:
                did = json["d_id"]
            else:
                did = self.department
            if group == "user":
                selector = "user.user_id,d_id,status,count(*) "
                groupby = " user_id, status) as user_count"
                # out_selector=""
            elif group == "department":
                selector = "d_id,status,count(*)"
                groupby = " d_id, status) as user_count"
            else:
                selector = "status,count(*)"
                groupby = " status) as user_count"

            self.con = Connect("localhost", "root", "123654", "attendance")
            sql = self.con.select_sql(selector, "attendance_table,user ", "attendance_table.user_id = user.user_id")
            status = json["status"]
            user_id = json["user_id"]
            name = json["name"]
            start = json["start"]
            end = json["end"]
            if user_id >= 0:
                sql = sql + " and user.user_id = " + str(user_id)
            if name != -1:
                sql = sql + " and name = '" + str(name) + "'"
            if status != -1:
                sql = sql + " and status = " + str(status)
            if start != -1:
                sql = sql + " and m_date>= '" + str(start) + "'"
            if end != -1:
                sql = sql + " and m_date<= '" + str(end) + "'"
            if did > 0:
                sql = sql + " and d_id=" + str(did)
            else:
                sql = sql + " and d_id >1"
            sql = "(" + sql + " group by " + groupby
            sql = "select * from " + sql
            print(sql)
            results = self.con.select(sql)
            self.con.close()
            return results


class PM(Manager):
    def __init__(self):
        Manager.__init__(self)

    def login(self, json):
        user_id = json["user_id"]
        user_id = json["user_id"]
        password = json["password"]
        self.con = Connect("localhost", "root", "123654", "attendance")
        result = self.con.select(self.con.select_sql("*", "user", str(
            "user_id = " + user_id + " and " + " password = '" + password + "' and d_id=2")))

        if len(result) > 0:
            self.is_login = True
            for user in result:
                self.user_id = user[0]
                self.department = 2
                self.password = user[2]
                self.name = user[3]
                self.info = user[4]
                self.con.insert({"table": "log", "args": {"user_id": self.user_id, "info": "login"}})

        else:
            self.is_login = False
        self.con.close()
        return result




class SM(PM):  # 设置节假日
    def __init__(self):
        PM.__init__(self)

    def login(self, json):
        print(json)
        user_id = json["user_id"]
        password = json["password"]
        self.con = Connect("localhost", "root", "123654", "attendance")
        result = self.con.select(self.con.select_sql("*", "user", str(
            "user_id = " + user_id + " and " + " password = '" + password + "' and d_id=1")))

        if len(result) > 0:
            self.is_login = True
            for user in result:
                self.user_id = user[0]
                self.department = 1
                self.password = user[2]
                self.name = user[3]
                self.info = user[4]
                self.con.insert({"table": "log", "args": {"user_id": self.user_id, "info": "login"}})

        else:
            self.is_login = False
        self.con.close()
        return result

    def delete(self, json):
        if self.is_login:
            log = json["log"]
            self.con = Connect("localhost", "root", "123654", "attendance")
            reply = self.con.delete(json)
            if log == "del_user":
                self.con.insert({"table": "log", "args": {"user_id": self.user_id, "info": log}})
            self.con.close()
            return reply
    def log_search(self,json1):
        if self.is_login:
            user_id = json1["user_id"]

            k_order = json1["order"][0]
            v_order = json1["order"][1]
            self.con = Connect("localhost", "root", "123654", "attendance")
            sql = self.con.select_sql("*", "log", "")
            if user_id >= 0:
                sql = sql + " user_id = " + str(user_id)
            else:
                sql=sql+" user_id>0"

            sql = sql + " order by "
            for index in range(len(k_order)):
                sql += str(k_order[index] + " " + v_order[index] + ",")
            sql = sql[:-1]
            results = self.con.select(sql)
            results=json.loads(json.dumps(results,cls=JsonExtendEncoder))
            self.con.close()
            return results

    def check_search(self, data):
        if self.is_login:
            self.con = Connect("localhost", "root", "123654", "attendance")
            sql = self.con.select_sql("*", "check_time", "")
            sql += "c_date='" + data["c_date"] + "'"
            print(sql)
            results = self.con.select(sql)
            results=json.loads(json.dumps(results,cls=JsonExtendEncoder))
            self.con.close()
            return results



class System(object):  # 三次更新
    def __init__(self):
        self.con = 0

    def new_day(self, date):
        self.con = Connect("localhost", "root", "123654", "attendance")
        # sql="select * from trip_table where status=2 and

        sql = "insert into attendance_table select user_id," + str(date) + ",null,null,0 from user"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        self.con.excute(sql)

        sql = self.con.select_sql('user_id', "trip_table",
                                  "status=2 and end_time>=" + str(date) + " and begin_time<= " + str(date))
        sql = "update attendance_table set status=7 where user_id in" + "(" + sql + ") and m_date= " + str(date)
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        self.con.excute(sql)
        sql = self.con.select_sql('user_id', "leave_table",
                                  "status=2 and end_time>=" + str(date) + " and begin_time<= " + str(date))
        sql = "update attendance_table set status=8 where user_id in" + "(" + sql + ") and m_date= " + str(date)
        self.con.excute(sql)
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        self.con.close()
        return True

        # manager=Manager()
        # manager.tl_search()

    def check_in(self, date):
        self.con = Connect("localhost", "root", "123654", "attendance")
        # sql = self.con.select_sql("user_id,m_date", "attendance_table",
        #                           " status=0 and check_in_time is not null and m_date=" + str(date))
        # sql = "update attendance_table set status=6 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        # sql = self.con.select_sql("user_id,m_date", "attendance_table",
        #                           " status=0 and check_in_time is null and m_date=" + str(date))
        # sql = "update attendance_table set status=1 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        self.check(self.con, " status=0 and check_in_time is not null and m_date=", date, 6)
        self.check(self.con, " status=0 and check_in_time is null and m_date=", date, 1)
        self.con.close()
        return True

    def check_out(self, date):
        self.con = Connect("localhost", "root", "123654", "attendance")
        # sql = self.con.select_sql("user_id,m_date", "attendance_table",
        #                           " status=6 and check_out_time is not null and m_date=" + str(date))
        # sql = "update attendance_table set status=2 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        # delete a line
        # sql = "update attendance_table set status=3 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        # sql = self.con.select_sql("user_id,m_date", "attendance_table",
        #                           " check_in_time is null and check_out_time is not null and m_date=" + str(date))
        # sql = "update attendance_table set status=5 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        self.check(self.con, " status=6 and check_out_time is not null and m_date=", date, 2)
        self.check(self.con, " status=1 and check_in_time is not null and check_out_time is not null and m_date=", date,
                   3)
        self.check(self.con, " check_in_time is null and check_out_time is not null and m_date=", date, 5)
        self.con.close()
        return True

    def check_the_day(self, date):
        self.con = Connect("localhost", "root", "123654", "attendance")
        # sql = self.con.select_sql("user_id,m_date", "attendance_table",
        #                           " check_in_time is null and check_out_time is not null and m_date=" + str(date))
        # sql = "update attendance_table set status=5 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        #
        # sql = self.con.select_sql("user_id,m_date", "attendance_table",
        #                           " check_in_time is null and check_out_time is null and m_date=" + str(date))
        # sql = "update attendance_table set status=4 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()

        # sql = self.con.select_sql("user_id,m_date", "attendance_table",
        #                           " status=6 and check_out_time is null and m_date=" + str(date))
        # sql = "update attendance_table set status=5 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        # sql = self.con.select_sql("user_id,m_date", "attendance_table",
        # delete a line
        # sql = "update attendance_table set status=5 where (user_id,m_date) in" + "(" + sql + ")"
        # try:
        #     self.con.cursor.execute(sql)
        #     self.con.db.commit()
        # except:
        #     self.con.db.rollback()
        self.check(self.con, " check_in_time is null and check_out_time is not null and m_date=", date, 5)
        self.check(self.con, " check_in_time is null and check_out_time is null and m_date=", date, 4)
        self.check(self.con, " status=6 and check_out_time is null and m_date=", date, 5)
        self.check(self.con, " status=1 and check_in_time is not null and check_out_time is null and m_date=", date, 5)
        self.con.close()
        return True

    def check(self, con, para, date, num):
        sql = con.select_sql("user_id,m_date", "attendance_table", para + str(date))
        sql = "update attendance_table set status=" + str(num) + " where (user_id,m_date) in" + "(" + sql + ")"
        try:
            con.cursor.execute(sql)
            con.db.commit()
        except:
            con.db.rollback()


class Connect(object):
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host="localhost",user="root",password="",db="attendance",port=3306)
        self.cursor = self.db.cursor()

    def insert(self, json):
        table = json["table"]
        obj = json["args"]
        values = tuple(obj.values())
        keys = tuple(obj)
        attr = str(keys).replace('\'', '')
        sql = "insert into " + table + attr + " values("
        for x in keys:
            sql += ("%s,")
        sql = sql[:-1] + ")"
        print(sql,values)
        try:
            self.cursor.execute(sql, values)
            self.db.commit()
            print("success")
            return True
        except:
            self.db.rollback()
            print("fail")
            return False

    def delete(self, json):
        table = json["table"]
        obj = json["args"]
        values = tuple(obj.values())
        keys = tuple(obj)
        sql = "delete from " + table + " where "
        for x in keys:
            sql += (str(x) + " =  %s and ")
        sql = sql[:-5]

        print(sql)
        try:
            self.cursor.execute(sql, values)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

            # print(sql, values)

    def update(self, json):
        table = json["table"]
        obj = json['key']

        change = json['args']
        o_v = list(obj.values())
        o_k = list(obj)
        c_v = list(change.values())
        c_k = list(change)

        sql = "update " + table + " set "
        for x in c_k:
            sql += (str(x) + " = " + "%s" + ",")
        sql = sql[:-1]
        sql += " where "
        for x in o_k:
            sql += (str(x) + " = %s and ")
        sql = sql[:-5]
        values = tuple(c_v + o_v)
        print(sql, values)
        
        try:
            self.cursor.execute(sql, values)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
            # print(sql, values)

    def select_sql(self, selector, from_sql, where_sql):
        sql = "select " + selector + " from " + from_sql + " where " + where_sql
        return sql

    def select(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")

    def close(self):
        self.cursor.close()
        self.db.close()

    def reconnect(self, host, user, password, database):
        self.cursor.close()
        self.db.close()
        self.db = pymysql.connect(host, user, password, database)
        self.cursor = self.db.cursor()

    def excute(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


db = Connect("localhost", "root", "", "attendance")
# db.insert("employee", {"user_id": 1, "password": "1234"})
# db.delete("employee", {"user_id": 1, "password": "1234"})
# db.update("employee", {"obj": {"user_id": 1, "password": "1234"}, "change": {"date": 123, "password": "12345"}})
# db.select_sql("*", "account", "a.b=a")
