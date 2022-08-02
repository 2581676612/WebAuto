import time

from code.web import Chrome
from code.base_case import BaseLoopCase


class TestCase(BaseLoopCase):
    def test_create(self):
        """循环加入项目"""
        user = Chrome.create_user()
        Chrome.login_by_code(user, '888888')
        Chrome.accept_shoot_invite('http://shorturl.test.vtutor.com.cn/38iSa8')
        time.sleep(5)
        Chrome.login_out()