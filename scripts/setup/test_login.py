from core.browser.chrome import Chrome
from core.browser.firefox import FireFox
from core.base.parse import usr_2, pwd_2
import pytest


class TestCase():
    @pytest.mark.P0
    def test_login(self):
        """登录"""
        Chrome.Control.show_browser()
        Chrome.Control.login_by_password()
        if FireFox:
            FireFox.Control.login_by_password(usr_2, pwd_2)


if __name__ == '__main__':
    pytest.main(['-sv', __file__, '--html=D:\\auto_demo\\report\\test.html'])
