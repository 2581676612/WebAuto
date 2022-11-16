import pytest

from core.browser.chrome import Chrome


class TestCase():
    @staticmethod
    def setup_class():
        Chrome.Shoot.open_project()
        Chrome.Shoot.open_camera_detail('测试机位-自动化')
        Chrome.Shoot.select_video_play()
        Chrome.Shoot.wait(3)

    @pytest.mark.P0
    def test_video_player_status(self):
        """播放器-播放状态测试"""
        Chrome.Shoot.video_player_start()
        Chrome.Shoot.check_player_status(play=True)
        Chrome.Shoot.video_player_stop()
        Chrome.Shoot.check_player_status(play=False)

    @pytest.mark.P0
    def test_video_player_time_control(self):
        """播放器-快进/快退"""
        Chrome.Shoot.control_player_forward()
        Chrome.Shoot.control_player_back()

    @pytest.mark.P0
    def test_video_player_time_code_change(self):
        """播放器-时间码格式切换"""
        Chrome.Shoot.change_video_time_code_to_code()
        Chrome.Shoot.change_video_time_code_to_fps()

    @pytest.mark.P0
    def test_video_player_fps_change(self):
        """播放器-上一帧/下一帧"""
        Chrome.Shoot.control_fps_forward()
        Chrome.Shoot.control_fps_back()
        Chrome.Shoot.change_video_time_code_to_normal()

    @pytest.mark.P0
    def test_video_player_sound_control(self):
        """播放器-静音/取消静音"""
        Chrome.Shoot.video_sound_close()
        Chrome.Shoot.video_sound_open()

    @pytest.mark.P0
    def test_video_quality_change(self):
        """播放器-画质切换"""
        Chrome.Shoot.change_video_views_quality()

    @pytest.mark.P0
    def test_video_speed_change(self):
        """播放器-倍数切换"""
        Chrome.Shoot.refresh()
        Chrome.Shoot.select_video_play()
        Chrome.Shoot.change_video_player_speed()

    @pytest.mark.P0
    def test_img_max_screen(self):
        """播放器-全屏显示"""
        Chrome.Shoot.file_max_view()
        Chrome.Shoot.file_quit_max_view()

    @pytest.mark.P0
    def test_many_screen(self):
        """播放器-多屏验证"""
        Chrome.Shoot.check_many_player()

    @staticmethod
    def teardown_class():
        Chrome.Shoot.back_to_shoot_index()