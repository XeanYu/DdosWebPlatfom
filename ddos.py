
__author__ = 'XeanYu'
from flask import Flask
from conf import db_config,SEO
from exts import db
from models import *
from main import main
from exts import login_manager

login_manager.session_protection = 'strong'
login_manager.login_view = 'main.sgin_in' # 定义验证登录页面

app = Flask(__name__)
app.config.from_object(db_config)

login_manager.init_app(app) # 传入app到login_manager进行初始化
db.init_app(app) # 初始化数据库

with app.app_context():
    db.create_all()


# 将 main 蓝本注册到 app 中
app.register_blueprint(main)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5552)
