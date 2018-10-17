from sqlalchemy import create_engine, Column, VARCHAR, INT, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import flask
import datetime
import json
from functools import wraps
from flask import request, redirect

app = flask.Flask('error_report')
app.secret_key = 'fs2d9s@19cjr%s3x'


Base = declarative_base()
class JsError(Base): 
    __tablename__ = 'jserror';
         
    uid = Column(INT(), primary_key=True)
    lineno = Column(VARCHAR())
    url = Column(VARCHAR())
    ip = Column(VARCHAR())
    stack = Column(VARCHAR()) 
    user_id = Column(VARCHAR())
    column = Column(VARCHAR())
    message = Column(VARCHAR())
    error = Column(VARCHAR())
    agent = Column(VARCHAR()) 
    referer = Column(VARCHAR())
    create_time = Column(TIMESTAMP())
    


def _json_default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')


def send_result(fun):
    @wraps(fun)
    def wrap(*args, **kwargs):
        ret = fun(*args, **kwargs)
        if isinstance(ret, dict):
            return json.dumps(ret, default=_json_default)
        else:
            return ret
    return wrap


@app.route('/', methods=['GET'])
def report():
    return redirect('/report')


@app.route('/info', methods=['GET'])
@send_result
def get_info():
    engine = create_engine('mysql://error:error@192.168.4.55:3306/error_report')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ret = {'code': 0, 'msg': []}
    num = request.args.get('num', 10, type=int)
    uid = request.args.get('uid')
    direction = request.args.get('dire')
    if not uid:
        result = session.query(JsError).order_by(JsError.uid.desc()).limit(num)
    elif uid:
        if direction == 'back':
            result = session.query(JsError).order_by(JsError.uid.desc()).filter(JsError.uid<uid).limit(num)
        elif direction == 'front':
            result = session.query(JsError).order_by(JsError.uid.desc()).filter(JsError.uid>uid).limit(num)

    total = result.count()
    if total == 0 or total < num:
        result = session.query(JsError).order_by(JsError.uid.desc()).limit(num)
        
    key = ['uid', 'lineno', 'url', 'ip', 'stack', 'user_id', 'column', 'message', 'error', 'agent', 'referer', 'create_time']
    for i in result:
        r_dict = {}
        for k in key:
            #r_dict.update({k: datetime.datetime.strftime(getattr(i,k), '%Y-%m-%d %H:%M:%S') if k == 'create_time' else getattr(i,k)})
            r_dict.update({k: getattr(i,k)})
        ret['msg'].append(r_dict)
    else:
        ret['uid'] = i.uid
    session.close()
    return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666, debug=True)


