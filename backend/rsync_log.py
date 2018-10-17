from sqlalchemy import create_engine, Column, VARCHAR, INT, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
import hashlib
import json
import re

"""
CREATE TABLE IF NOT EXISTS `jserror`(
   `uid` INT UNSIGNED AUTO_INCREMENT,
   `lineno` VARCHAR(20),
   `url` VARCHAR(100),
   `ip` VARCHAR(100),
   `stack` VARCHAR(255),
   `user_id` VARCHAR(20),
   `column` VARCHAR(20),
   `message` VARCHAR(255),
   `error` VARCHAR(255),
   `agent` VARCHAR(255),
   `referer` VARCHAR(255),
    `create_time` DATETIME,
   PRIMARY KEY ( `uid` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""

TIME = datetime.strftime(datetime.today(), '%Y%m%d')
EXP_TIME = datetime.strftime(datetime.today() - timedelta(days=2), '%Y-%m-%d')
log_path = '/home/ubuntu/logs/jserror'
log_file = '%s/jserror.%s.log' % (log_path, TIME)
seek_file = '/tmp/.jserror_seek'

def _hash(arg):
    arg = str(arg).encode('utf8')
    md5 = hashlib.md5(arg)
    ret = md5.hexdigest()
    return ret


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

engine = create_engine('mysql://error:error@192.168.4.55:3306/error_report')
DBSession = sessionmaker(bind=engine)

session = DBSession()
with open(log_file, 'rb') as f:
    curr_hash = _hash(log_file)
    try:
        s = open(seek_file)
        tell = s.read().split(' ')
        s.close()
        if tell[0] == curr_hash:
            f.seek(int(tell[1]))
    except Exception as e:
        print(str(e))
    for i in f.readlines():
        log = i.split('\t', 1)
        js = json.loads(log[1])
        js = json.loads(js)
        new_js = JsError(lineno=js.get('lineno'), url=js.get('url').encode('utf8'),
                        ip=js.get('ip'), stack=js.get('stack','null').encode('utf8'),
                        user_id=js.get('user_id'), column=js.get('column'),
                        message=js.get('message').encode('utf8'), error=str(js.get('error')),
                        agent=js.get('agent').encode('utf8'), referer=js.get('referer').encode('utf8'),create_time=log[0])

        session.add(new_js)
        session.commit()
        session.close()

    ret = curr_hash + ' ' + str(f.tell())
    s = open(seek_file, 'w')
    s.write(ret)
    s.close()

session.query(JsError).filter(JsError.create_time < EXP_TIME).delete()
session.commit()


