#!/usr/bin/env python
__author__ = 'XeanYu'
from exts import db
from flask_login import UserMixin
from exts import login_manager
from func.date import now


# Log Users [用户数据]
class Users(db.Model,UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,nullable=False,index=True)
    password = db.Column(db.String(124),nullable=False,index=True)
    mail = db.Column(db.String(124),index=True,nullable=False)
    code = db.Column(db.String(40),nullable=False) # 私密代码
    sgin_up_date = db.Column(db.String(64)) # 登录时间
    login_static = db.Column(db.String(1),default='0') # 是否可以登录
    vip = db.Column(db.String(64),default=0) # 是否是VIP

    # 表中没有id字段，自己定义返回uid字段
    def get_id(self):
        return self.uid

@login_manager.user_loader
def user_load(id):
    return Users.query.get(id)

# Login log [登录日志]
class Login_logs(db.Model):
    __tablename__ = 'login_logs'

    id = db.Column(db.Integer,primary_key=True) # id => 主键
    username = db.Column(db.String(64),index=True) # 用户的用户名
    browser = db.Column(db.String(124),index=True) # 用户使用的浏览器
    device = db.Column(db.String(124),index=True)  # 用户使用的设备
    os = db.Column(db.String(124),index=True)  # 用户的操作系统
    ip = db.Column(db.String(64),index=True) # 用户IP地址
    platform = db.Column(db.String(12),index=True) # user's platform
    login_date = db.Column(db.String(64),default=now()) # 登录时间

class Site(db.Model):
    __tablename__ = 'site_config'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(124),index=True)
    title = db.Column(db.String(124),index=True)
    keywords = db.Column(db.String(246),index=True)
    description = db.Column(db.String(1024),index=True)

class Api(db.Model):
    __tablename__ = 'apis'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(124)) # API名称
    api = db.Column(db.String(1024)) # API

class Vip(db.Model):
    __tablename__ = 'vips'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(124),nullable=False,unique=True)
    attack_num = db.Column(db.Integer,nullable=False)
    max_use_time = db.Column(db.Integer,nullable=False)
    yuan = db.Column(db.Integer)
    pay_url = db.Column(db.String(520),default='#')

class Placard(db.Model):
    __tablename__ = 'placards'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(124),nullable=False)
    text = db.Column(db.String(1024))
    author = db.Column(db.String(64))
    date = db.Column(db.String(124),default=now())

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(124),nullable=False)
    text = db.Column(db.Text)
    user = db.Column(db.String(64))
    say_date = db.Column(db.String(124),default=now())
    look_date = db.Column(db.String(124),default='none')
    is_look = db.Column(db.Boolean,default=False)

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(124),nullable=False)
    vip_id = db.Column(db.Integer)
    card = db.Column(db.String(246),index=True)
    is_use = db.Column(db.Boolean,default=False)
    time = db.Column(db.String(124))
    use_date = db.Column(db.String(124))
    use_user = db.Column(db.String(64))
    make_date = db.Column(db.String(124),default=now())


