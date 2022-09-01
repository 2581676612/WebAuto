from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_rtmp_push(self):
        """机位配置-rtmp推流"""
        Chrome.Shoot.open_project()
        Chrome.Shoot.open_camera_setting('测试机位-自动化')
        Chrome.Shoot.push_by_rtmp()

    def test_srt_push(self):
        """机位配置-srt推流"""
        Chrome.Shoot.push_by_srt()
        Chrome.Shoot.close_camera_setting()
