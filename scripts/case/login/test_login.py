import time
from core.browser.chrome import Chrome
from core.base.base_case import BaseCase
import pytest


class TestCase(BaseCase):
    def test_login(self):
        """登录测试"""
        Chrome.Project.login_by_password()


if __name__ == '__main__':
    pytest.main(['-sv', __file__, '--html=D:\\auto_demo\\report\\test.html'])
