__author__ = 'XeanYu'

import bcrypt

# 进行bcrypt加密
def passwd_bcrypt(password):

    passwd = bcrypt.hashpw(password.encode(),bcrypt.gensalt(10))

    return passwd.decode() # 该值存入数据库

# 检查密码是否正确
def check_passwd(password,hash):

# 该判断用来登录时核验账户密码是否正确
    if bcrypt.hashpw(password.encode(),hash) == hash:
        return True

    else:
        return False

