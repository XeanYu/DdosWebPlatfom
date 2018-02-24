#!/usr/bin/env python
__author__ = 'XeanYu'

# 创建蓝本
from flask import Blueprint
main = Blueprint('main',__name__)

# 在末尾导入views,errors，因为errors和views也需要导入main，避免了循环导入依赖

from . import views,errors

# .(点) 就是当前包