import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.cfg'))


# 解析配置文件参数
case = config.get('TestCase', 'case')
chrome_driver = config.get('ChromeDriver', 'file')
firefox_run = config.get('FireFoxDriver', 'run')
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
project_name = config.get('Project', 'name')
test_people = config.get('Report', 'test_people')
loop_count = config.get('Loop', 'count')


# 自定义参数
file_type_dict = {'img': ['bmp', 'tiff', 'gif', 'png', 'jpeg', 'jpg'],
                  'video': ['avi', 'wmv', 'mpg', 'mpeg', 'mov', 'rm', 'ram', 'swf', 'flv', 'mp4']}
main_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))