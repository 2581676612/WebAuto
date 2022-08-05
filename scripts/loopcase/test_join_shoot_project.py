import time

from core.browser.chrome import Chrome
from core.base.base_case import BaseLoopCase


class TestCase(BaseLoopCase):
    def test_create(self):
        """循环加入项目"""
        user = Chrome.Project.create_user()
        Chrome.Project.login_by_code(user, '888888')
        Chrome.Project.accept_shoot_invite('http://shorturl.test.vtutor.com.cn/38iSa8')
        time.sleep(5)
        Chrome.Project.login_out()