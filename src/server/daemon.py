# 守护进程
from "db" import System, Connect
import time
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

system = System()
today = datetime.date.today()

def daily_work():
    db = Connect("localhost", "root", "", "attendance")
    tomorrow = today + datetime.timedelta(days=1)
    sql = "select * from check_time where c_date = " + today
    ret = db.select(sql)
    obj = {
        'table': 'check_time',
        'args': {
            'c_date': tomorrow,
            'check_in_time': ret[1],
            'check_out_time': ret[2]
        }
    }
    db.insert(obj)
    db.close()
    system.new_day()

def check_in():
    system.check_in()

def check_out():
    system.check_out()

def check_today():
    system.check_today()

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_in, 'cron', day_of_week='1-7', hour=13, minute=30)
    scheduler.add_job(check_out, 'cron', day_of_week='1-7', hour=19, minute=30)
    scheduler.add_job(check_today, 'cron', day_of_week='1-7', hour=23, minute=30)
    scheduler.add_job(daily_work, 'cron', day_of_week='1-7', hour=23, minute=45)    
    scheduler.start()