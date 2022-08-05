from core.browser.chrome import Chrome
from core.base.base_case import BaseCaseFile


class TestCaseFileImgDetail(BaseCaseFile):
    def test_video_detail_view(self):
        """进入视频文件详情页"""
        Chrome.Project.enter_file_detail_view(file_type='video')
        Chrome.Project.check_in_file_detail_view()

    def test_video_player_status(self):
        """播放器状态测试"""
        Chrome.Project.video_player_start()
        Chrome.Project.check_player_status(play=True)
        Chrome.Project.video_player_stop()
        Chrome.Project.check_player_status(play=False)

    def test_video_player_time_control(self):
        """播放器快进/快退"""
        Chrome.Project.control_player_forward()
        Chrome.Project.control_player_back()

    def test_video_player_time_code_change(self):
        """播放器时间码格式切换"""
        Chrome.Project.change_video_time_code_to_code()
        Chrome.Project.change_video_time_code_to_fps()

    def test_video_player_fps_change(self):
        """播放器上一帧/下一帧"""
        Chrome.Project.control_fps_forward()
        Chrome.Project.control_fps_back()
        Chrome.Project.change_video_time_code_to_normal()

    def test_video_player_sound_control(self):
        """播放器静音/取消静音"""
        Chrome.Project.video_sound_close()
        Chrome.Project.video_sound_open()

    def test_img_max_screen(self):
        """视频文件全屏显示"""
        Chrome.Project.file_max_view()
        Chrome.Project.file_quit_max_view()

    @staticmethod
    def teardown_class():
        Chrome.Project.back_to_project_index()