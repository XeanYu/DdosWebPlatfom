#!/usr/bin/env python
__author__ = 'XeanYu'
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from ddos import app
from exts import db

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    from configparser import ConfigParser
    manager.run()