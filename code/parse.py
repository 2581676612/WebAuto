import configparser
import json
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.cfg'))

case = config.get('TestCase', 'case')
chrome_driver = config.get('ChromeDriver', 'file')
firefox_driver = config.get('FireFoxDriver', 'file')
web_type = config.get('Environment', 'web_type')
usr_1_name = config.get('UserInfo', 'usr_1_name')
usr_1 = config.get('UserInfo', 'usr_1')
pwd_1 = config.get('UserInfo', 'pwd_1')
usr_2_name = config.get('UserInfo', 'usr_2_name')
usr_2 = config.get('UserInfo', 'usr_2')
pwd_2 = config.get('UserInfo', 'pwd_2')
usr_3_name = config.get('UserInfo', 'usr_3_name')
usr_3 = config.get('UserInfo', 'usr_3')
pwd_3 = config.get('UserInfo', 'pwd_3')
project_name = config.get('project', 'name')
loop_count = config.get('Loop', 'count')
