__author__ = 'XeanYu'
from configparser import ConfigParser

conf = ConfigParser()

conf['SEO'] = {
    'title': 'XeanYu',
    'keywords': 'XeanYu,',
    'description': 'XeanYu'
}

conf['WEB'] = {
    'web_name': 'XeanYu',
    'message': 'XeanYu',
    'buy_url': 'XeanYu'

}

with open('conf/web.conf','w') as file:
    conf.write(file)