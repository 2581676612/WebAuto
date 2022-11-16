import pytest

from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    @pytest.mark.P0
    def test_fangluping_open(self):
        """拍摄项目设置-防录屏权限开启测试"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('拍摄设置')
        Chrome.Shoot.set_fangluping(True)
        Chrome.Shoot.open_camera_detail()
        Chrome.Shoot.check_fangluping(True)

    @pytest.mark.P0
    def test_fangluping_close(self):
        """拍摄项目设置-防录屏权限关闭测试"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('拍摄设置')
        Chrome.Shoot.set_fangluping(False)
        Chrome.Shoot.open_camera_detail()
        Chrome.Shoot.check_fangluping(False)

    @pytest.mark.P0
    def test_read_file_close(self):
        """拍摄项目设置-关闭成员查看文件权限"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('拍摄设置')
        Chrome.Shoot.set_role_read_permission(role='制作者', read=False)
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('成员管理')
        Chrome.Shoot.change_role(member=FireFox.Control.user_name, change_role='制作者')
        FireFox.Shoot.refresh()
        FireFox.Shoot.open_join_project()
        FireFox.Shoot.check_close_read_permission_by_room()
        FireFox.Shoot.open_camera_detail()
        FireFox.Shoot.check_close_read_permission_by_file()

    @staticmethod
    def teardown():
        Chrome.Shoot.back_to_shoot_index()
        FireFox.Shoot.back_to_shoot_index()
