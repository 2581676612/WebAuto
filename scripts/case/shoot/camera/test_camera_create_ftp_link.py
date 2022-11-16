import pytest

from core.browser.chrome import Chrome


class TestCase():
    @pytest.mark.P0
    def test_upload_by_ftp(self):
        """机位配置-FTP上传"""
        Chrome.Shoot.open_project()
        Chrome.Shoot.open_camera_setting('测试机位-自动化')
        Chrome.Shoot.create_ftp_link()
