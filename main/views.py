__author__ = 'XeanYu'

"""
this modle is main.views

"""

from flask import render_template,session,url_for,request,jsonify,redirect,abort
from flask_login import login_required,login_user,logout_user
from . import main
from random import randint # make random_code
from exts import db
from models import Users,Login_logs,Site,Vip,Placard,Message,Card
from func.password import * # use bcrypt make password
from func.date import now
from func.agent import *
from func.randmd5 import make_md5
from conf.admin import Admin
from conf import SEO


# index view route
@main.route('/')
def index():

    seo = Site.query.filter_by(id=1).first()

    if seo:
        return render_template('index.html',seo=seo)
    else:
        return redirect(url_for('main.init'))

# sgin_up view route
@main.route('/registered/',methods=['GET','POST']) # allow GET and POST request
def sgin_up():
    """
    此路由用来注册用户
    :return:
    """
    if request.method == 'GET': # GET
        global up_random_code
        up_random_code = randint(10000, 99999)  # 生成5位纯数字验证码
        return render_template('sgin_up.html',num_code=up_random_code)

    else: # POST
        username = request.form.get('username').strip() # 获取用户名
        email = request.form.get('email').strip() # 获取邮箱
        password = request.form.get('password').strip() # 获取密码
        code = request.form.get('code').strip() # 获取私密代码
        random_code_form = request.form.get('random_code').strip() # 获取随机码

        if all([username,email,password,code,random_code_form]):

            # 判断验证码是否正确
            if str(random_code_form) == str(up_random_code):

                add_db = Users.query.filter_by(username=username).first()
                if not add_db: # 判断数据是否存在当前用户，如果不存在，则添加到数据库

                    password = passwd_bcrypt(password)
                    add_db = Users(username=username,mail=email,password=password,code=code,sgin_up_date = now())
                    db.session.add(add_db)
                    db.session.commit() # 提交值数据库(Fluash())
                    return jsonify(msg='redirect')

                else:
                    return jsonify(msg='用户已存在')

            else:
                return jsonify(msg='输入的随机码不正确')

        else:
            return jsonify(msg='输入的信息不完整')

# sgin_in  view route
@main.route('/login/',methods=['GET','POST'])
def sgin_in():
    """
    此路由用来用户登录
    :return:
    """
    # if user not login ==> GO TO login
    if request.method == 'GET':
        global lg_random_code
        lg_random_code = randint(10000,99999)
        return render_template('sgin_in.html',num_code=lg_random_code) # return template and export make_random_code

    if request.method == 'POST':

        """
        strip() => cut space
        """
        username = request.form.get('username').strip() # get user's username
        password = request.form.get('password').strip() # get user's password
        random_code_form = request.form.get('random_code').strip() # get user's input random code

        # get user's msg
        user_ip = str(request.remote_addr) # get user's IP
        user_agent = str(request.user_agent) # get user's User-Agent
        browser = str(request.user_agent.browser) # get user's browser
        os = str(request.user_agent.platform)  # get user's os

        if all([username,password,random_code_form]): # judgmeng user's input not is None
            if str(lg_random_code) == str(random_code_form): # judgment random_code == user input random_code

                # search user for Users'Table
                login = Users.query.filter_by(username=username).first()
                if login: # find user

                    if str(login.login_static) == '0': # 是否可以登录
                         if check_passwd(password,login.password.encode()): # judgment password equal

                            # add user login log
                            logadd = Login_logs(
                                username=username,
                                browser=browser,
                                device=is_device(user_agent),
                                os=os,
                                ip=user_ip,
                                platform=user_msg(user_agent)
                            ) #


                            db.session.add(logadd) # add 'logadd' object to 'db.session'
                            db.session.commit() # commit session to DB's Login_logs
                            login_user(login)
                            session['username'] = login.username
                            # 判断是否是管理员
                            if username in Admin.username:
                                session['Admin'] = True

                            else:
                                session['Admin'] = False

                            return jsonify(msg='login') # return views to Ajax ==> Login success

                         else: # password error
                            return jsonify(msg='密码错误!')
                    else:
                        return jsonify(msg='您被禁止登录!')

                else:   # don's search username
                    return jsonify(msg='没有此用户,请注册!')

            else:   # random error
                return jsonify(msg='随机码输入错误')

        else:  # fill message have None
            return jsonify(msg='请输入完整信息')

    # if user login

# password lost page  view route
@main.route('/getpass/',methods=['GET','POST'])
def getpass():

    """
    change password page
    :return:
    """
    if request.method == 'GET':
        return render_template('getpass.html')

    else:
        username = request.form.get('user').strip()
        code = request.form.get('code').strip()
        newpass = request.form.get('newpass').strip()

            # use all() function => True
        if all([username,code,newpass]):

            # find username for DB
            user = Users.query.filter_by(username=username).first()
            if user:
                if str(code) == str(user.code):
                    user.password = str(passwd_bcrypt(newpass))
                    db.session.add(user)
                    db.session.commit()
                    return jsonify(msg='change')

                else:
                    return jsonify(msg='私密代码不正确!')

            else:
                return jsonify(msg='没有此用户')

        else:
            return jsonify(msg='请填写好信息')

# 面板
@main.route('/user/',methods=['GET','POST'])
@login_required
def console():

    user_num = Users.query.count()
    placards = Placard.query.all()
    placards.reverse()

    index_msg = {
        'user_num':user_num,
        'ddos_num': 2123,
        'server_num': 1110,
                 }
    return render_template('user.html',template='u_index.html',admin=session['Admin'],index_msg = index_msg,ggs=placards)

# 个人资料
@main.route('/user/self/',methods=['GET','POST'])
@login_required
def self():

    myself = Users.query.filter_by(username=session['username']).first()
    if request.method == 'GET':

        page = request.args.get('page',1,type=int)
        pagination = Login_logs.query.filter_by(username=session['username']).paginate(page, per_page=8, error_out=False)
        items = pagination.items


        a = {'name':'ZZ'}
        return render_template('user.html',template='u_self.html',myself=myself,vip=a,logs=pagination,login_log=items,admin=session['Admin'])

    else:

        email = request.form.get('email').strip() # get form's input of name is email

        if email:
            myself.mail = email
            db.session.add(myself)
            db.session.commit()
            return jsonify({'msg':'change'})

        else:
            return jsonify({'msg':'不可以有空字段'})


# 系统设置
@main.route('/user/set/',methods=['GET','POST'])
@login_required
def os_set():

    # 判断是否是平台管理员
    if session['Admin']:

        # 判断使用了什么方法
        if request.method == 'GET':
            seo = Site.query.filter_by(id=1).first()
            return render_template('user.html',template='os_set.html',admin=True,seo=seo)

        # POST (ajax)请求
        else:
            # 获取数据
            name = request.form.get('name').strip()
            title = request.form.get('title').strip()
            keywords = request.form.get('keywords').strip()
            description = request.form.get('description').strip()

            if all([title,keywords,description,name]): # 判断有没有空字段
                chseo = Site.query.filter_by(id=1).first()

                chseo.name = name
                chseo.title = title # 修改标题
                chseo.keywords = keywords # 
                chseo.description = description


                db.session.add(chseo)
                db.session.commit()
                return jsonify({'msg':'change'})

            else:
                return jsonify({'msg':'请填写完整信息!'})

    # 不是管理员则跳转至面板首页
    else:
        return redirect(url_for('main.console'))

# VIP
###################
@main.route('/user/vip_set/',methods=['GET','POST'])
@login_required
def vip_set():
    if session['Admin']:

        vips = Vip.query.all()
        if request.method == 'GET':
            return render_template('user.html',template='os_vip.html',vips=vips,admin=True)

        else:
            name = request.form.get('name')
            attack_num = request.form.get('attack_num')
            max_use_time = request.form.get('use_time')
            pay_url = request.form.get('pay_url')
            yuan = request.form.get('yuan')

            if all([name,attack_num,max_use_time,pay_url]):
                vip = Vip.query.filter_by(name=name).first()

                if vip:
                    vip.name = name
                    vip.attack_num = attack_num
                    vip.max_use_time = max_use_time
                    vip.pay_url = pay_url
                    vip.yuan = yuan
                    db.session.add(vip)
                    db.session.commit()
                    return jsonify(msg='old')

                else:
                    vip = Vip(name=name,attack_num=attack_num,max_use_time=max_use_time,pay_url=pay_url,yuan=yuan)
                    db.session.add(vip)
                    db.session.commit()
                    return jsonify(msg='new')
            else:
                return jsonify(msg='0')

    else:
        return redirect(url_for('main.console'))

@main.route('/user/vip_del/',methods=['GET','POST'])
@login_required
def vip_del():
    if session['Admin']:

        if request.method == 'GET':
            return redirect(url_for('main.console'))

        else:
            vip = request.form.get('name')
            print(vip)

            if vip:
                delte = Vip.query.filter_by(name=str(vip)).first()
                db.session.delete(delte)
                db.session.commit()
                return jsonify(msg='del')

            else:
                return jsonify(msg='Error')

    else:
        return redirect(url_for('main.console'))
######################

# 公告
###########################
@main.route('/user/placard/',methods=['GET','POST'])
@login_required
def placard():
    if session['Admin']:
        if request.method == 'GET':
            placards = Placard.query.all()
            return render_template('user.html',template='os_placard.html',admin=True,placards=placards)

        else:

            title = request.form.get('title')
            text = request.form.get('text')
            author = session['username']
            date = now()

            find = Placard.query.filter_by(title=title).first()

            if not find:
                add_dict = {
                    'msg': 'add',
                    'title': title,
                    'context': text,
                    'author': author,
                    'date':date
                }
                add = Placard(title=title,text=text,author=author,date=date)
                db.session.add(add)
                db.session.commit()
                return jsonify(add_dict)

            else:
                return jsonify({'msg':'e1'})
    else:
        return redirect(url_for('main.console'))

@main.route('/user/del_placard/',methods=['POST','GET'])
@login_required
def placard_del():
    if session['Admin']:
        if request.method == 'GET':
            return redirect(url_for('main.console'))

        else:
            title = request.form.get('title')

            if title:
                delete = Placard.query.filter_by(title=title).first()
                db.session.delete(delete)
                db.session.commit()
                return jsonify({'msg':'del'})

            else:
                return jsonify({'msg':'0'})
    else:
        return redirect(url_for('main.console'))
#########################


@main.route('/user/users/',methods=['GET','POST'])
@login_required
def users():
    if session['Admin']:
        pass
    else:
        return redirect(url_for('main.console'))

# 留言板
######################
@main.route('/user/say/',methods=['GET','POST'])
@login_required
def say():
    if request.method == 'GET':
        said = Message.query.filter_by(user=session['username']).all()
        return render_template('user.html',admin=session['Admin'],template='u_say.html',saids=said)
    else:

        title = request.form.get('title')
        text = request.form.get('text')

        if all([title,text]):
            add = Message(title=title,text=text,user=session['username'])
            db.session.add(add)
            db.session.commit()
            return jsonify({'msg':'addsay'})

        else:
            return jsonify({'msg':'e1'})

@main.route('/user/say_del/',methods=['POST','GET'])
@login_required
def say_del():

    if request.method == 'GET':
        return abort(404)
    else:
        id = request.form.get('id')
        if id:
            delete = Message.query.filter_by(id=id).first()
            if delete:
                db.session.delete(delete)
                db.session.commit()
                return jsonify({'msg':'saydel'})
            else:
                return jsonify({'msg':'e2'})

        else:
            return jsonify({'msg':'e1'})

@main.route('/user/os_say/',methods=['GET','POST'])
@login_required
def os_say():
    if session['Admin']:

        if request.method == 'GET':
            say = Message.query.all()
            say.reverse()
            return render_template('user.html',template='os_say.html',admin=True,says=say)

        else:
            id = request.form.get('id')
            say = Message.query.filter_by(id=id).first()
            if say:
                say.is_look = True
                say.look_date = now()
                db.session.add(say)
                db.session.commit()
                return jsonify({'msg':'look','date': now()})

            else:
                return jsonify({'msg':'e1'})

    else:
        return jsonify({'msg': '您不是管理员,无权操作留言'})
#####################

## 卡密生成
@main.route('/user/make_card/',methods=['GET','POST'])
@login_required
def make_card():
    if session['Admin']:
        if request.method == 'GET':
            page = request.args.get('page',1,type=int)
            vips = Vip.query.all()
            card = Card.query.paginate(page, per_page=8, error_out=False)

            return render_template('user.html',template='make_card.html',admin=True,cards=card.items,look=card,vips=vips)
        else:
            card_num = request.form.get('cards')
            time = request.form.get('time')
            vip = request.form.get('vip')

            if all([card_num,time,vip]):
                name = Vip.query.filter_by(id=int(vip)).first()
                name = name.name
                for add in range(int(card_num)):
                    md5 = make_md5()

                    find = Card.query.filter_by(card=md5).first()
                    if find:
                        md5 = make_md5()
                    add_card = Card(name=name,vip_id=vip,time=time,card=md5)
                    db.session.add(add_card)
                    db.session.commit()
                return jsonify({'msg':'make'})
            else:
                return jsonify({'msg':'e1'})
    else:
        return redirect(url_for('main.console'))
# 注销
@main.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.sgin_in'))


# 网站初始化
@main.route('/init/')
def init():

    init = Site.query.filter_by(id=1).first()
    if init:
        return redirect(url_for('main.index'))

    else:
        site = Site(name=SEO.name,title=SEO.title, keywords=SEO.keywords, description=SEO.description)
        db.session.add(site)
        db.session.commit()
        return redirect(url_for('main.index'))
