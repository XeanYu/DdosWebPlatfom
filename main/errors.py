
__author__ = 'XeanYu'

"""
此模块是错误路由模块
"""


from flask import render_template
from . import main

# .(点) ==> __init__

@main.errorhandler(404)
def notfound(e):
    return '<h1>No Found</h1>'

