__author__ = 'XeanYu'
from hashlib import md5
import random
def make_md5():
    md = md5()
    rand = str(random.random())
    for i in range(48):
        rand = rand + chr(random.randint(0,9999))

    md.update(rand.encode())
    return md.hexdigest()
