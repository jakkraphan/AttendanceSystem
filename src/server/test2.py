import json
from datetime import date
from datetime import datetime


class JsonExtendEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    d = [[datetime.now(),1,1],[datetime.now(),1,1]]
    ds = json.dumps(d, cls=JsonExtendEncoder)
    print("ds type:", type(ds), "ds:", ds)
    l = json.loads(ds)
    print("l  type:", type(l), "ds:", l )
