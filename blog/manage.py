import redis
from flask import Flask
from flask_session import Session
from flask_script import Manager

from back.models import db
from back.views import blue
from web.views import web

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(blueprint=blue)
app.register_blueprint(blueprint=web)

# 配置数据库连接

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 配置session数据库

app.config['SECRET_KEY'] = '123456'
app.secret_key = '12321<{=．．．．(嘎~嘎~嘎~)'

# 配置redis管理session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='47.102.110.28',port=6379,password='123456')
#app.config['SESSION_REDIS'] = redis.Redis(host='localhost',port=6379,)
# 配置session管理
Session(app)




manage = Manager(app)


if __name__ == '__main__':
    manage.run()
    

