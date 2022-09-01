from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_create_ftp_link(self):
        """机位配置-生成FTP链接"""
        Chrome.Shoot.open_project()
        Chrome.Shoot.open_camera_setting('测试机位-自动化')
        Chrome.Shoot.create_ftp_link()
        Chrome.Shoot.close_camera_setting()
