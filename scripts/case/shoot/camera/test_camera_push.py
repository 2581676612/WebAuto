import time

import pytest

from core.browser.chrome import Chrome
from core.app.obs import OBS


class TestCase():
    @pytest.mark.P0
    def test_rtmp_push(self):
        """机位配置-rtmp推流"""
        Chrome.Shoot.open_project()
        Chrome.Shoot.open_camera_setting('测试机位-自动化')
        Chrome.Shoot.push_by_rtmp()

    @pytest.mark.P0
    def test_srt_push(self):
        """机位配置-srt推流"""
        Chrome.Shoot.push_by_srt()
        Chrome.Shoot.close_camera_setting()
        Chrome.Shoot.open_camera_detail()
        OBS.start()
        OBS.open_settings()
        OBS.open_push_settings()
        OBS.set_push_server()
        OBS.submit()
        OBS.start_push()
        Chrome.Control.show_browser()
        Chrome.Shoot.check_live()
        Chrome.Control.wait(5)
        Chrome.Shoot.start_record()
        Chrome.Control.wait(5)
        Chrome.Shoot.stop_record()

    @staticmethod
    def teardown_class():
        OBS.start()
        OBS.stop_push()
        OBS.quit()
        Chrome.Shoot.back_to_shoot_index()
