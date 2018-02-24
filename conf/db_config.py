#!/usr/bin/env python
__author__ = 'XeanYu'
import os

SECRET_KEY = 'asdfawegr1a1sdfa1sd6'

DB_USER = 'root' # DB login user
DB_PASS = 'xeanyu' # DB login password
DB_NAME = 'ddos' # use DB name
DB_PORT = '3306'  # DB connect port
DB_HOST = '127.0.0.1' # BD connect host

BASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(DB_USER,DB_PASS,DB_HOST,DB_PORT,DB_NAME)
SQLALCHEMY_DATABASE_URI = BASE_URI


SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False