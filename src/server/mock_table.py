from test import Connect
import random

con = Connect("localhost", "root", "test1234", "attendance")
x = ["2018-1-1", "2018-1-2", "2018-1-3", "2018-1-4", "2018-1-6", "2018-1-7", "2018-1-8", "2018-1-9", "2018-1-10"]
y = [("8:0:0", "18:0:0", 6), ("10:0:0", "16:0:0", 3), ("8:0:0", "16:0:0", 2), ("10:0:0", "18:0:0", 1),
     ("8:0:0", None, 5), (None, None, 4)]
for a in range(2, 131):
    for b in range(len(x)):
        checkin, checkout, status = y[random.randint(0, 5)]
        con.insert({"table": "attendance_table",
                    "args": {"user_id": a, "m_date": x[b], "check_in_time": checkin, "check_out_time": checkout,
                             "status": status}})
e = ["2017-12-21", "2017-12-22", "2017-12-23", "2017-12-24", "2017-12-26", "2017-12-27", "2017-12-28", "2017-12-29",
     "2017-12-30"]
s = ["2017-12-11", "2017-12-12", "2017-12-13", "2017-12-14", "2017-12-16", "2017-12-17", "2017-12-18", "2017-12-19",
     "2017-12-20", "2017-12-21"]
for a in range(2, 131):
    begin = s[random.randint(0, 9)]
    end = e[random.randint(0, 8)]
    m_type = (random.randint(0, 3))
    status = random.randint(0, 3)
    reply = "hello world"
    reason = "test"
    con.insert({"table": "leave_table",
                "args": {"user_id": a, "begin_time": begin, "end_time": end, "reason": reason, "reply": reply,
                         "m_type": m_type,
                         "status": status}})
e = ["2017-11-21", "2017-11-22", "2017-11-23", "2017-11-24", "2017-11-26", "2017-11-27", "2017-11-28", "2017-11-29",
     "2017-11-30"]
s = ["2017-11-11", "2017-11-12", "2017-11-13", "2017-11-14", "2017-11-16", "2017-11-17", "2017-11-18", "2017-11-19",
     "2017-11-20", "2017-11-21"]
for a in range(2, 131):
    begin = s[random.randint(0, 9)]
    end = e[random.randint(0, 8)]
    m_type = (random.randint(0, 1))
    status = random.randint(0, 3)
    reply = "hello world"
    reason = "test"
    con.insert({"table": "trip_table",
                "args": {"user_id": a, "begin_time": begin, "end_time": end, "reason": reason, "reply": reply,
                         "m_type": m_type,
                         "status": status}})

for day in x:
    con.insert({"table": "check_time", "args": {"c_date": day, "check_in_time": "9:0:0", "check_out_time": "17:0:0"}})
