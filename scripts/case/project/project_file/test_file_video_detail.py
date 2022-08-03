from code.web import Chrome
from code.base_case import BaseCaseFile


class TestCaseFileImgDetail(BaseCaseFile):
    def test_video_detail_view(self):
        """进入视频文件详情页"""
        Chrome.enter_file_detail_view(file_type='video')
        Chrome.check_in_file_detail_view()

    def test_video_player_status(self):
        """播放器状态测试"""
        Chrome.video_player_start()
        Chrome.check_player_status(play=True)
        Chrome.video_player_stop()
        Chrome.check_player_status(play=False)

    def test_video_player_time_control(self):
        """播放器快进/快退"""
        Chrome.control_player_forward()
        Chrome.control_player_back()

    def test_video_player_time_code_change(self):
        """播放器时间码格式切换"""
        Chrome.change_video_time_code_to_code()
        Chrome.change_video_time_code_to_fps()

    def test_video_player_fps_change(self):
        """播放器上一帧/下一帧"""
        Chrome.control_fps_forward()
        Chrome.control_fps_back()
        Chrome.change_video_time_code_to_normal()

    def test_video_player_sound_control(self):
        """播放器静音/取消静音"""
        Chrome.video_sound_close()
        Chrome.video_sound_open()

    def test_img_max_screen(self):
        """视频文件全屏显示"""
        Chrome.file_max_view()
        Chrome.file_quit_max_view()
