from core.browser.chrome import Chrome
from core.base.parse import copy_camera


class TestCase():
    @staticmethod
    def setup_class():
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('创建机位')
        Chrome.Shoot.create_camera(copy_camera)
        Chrome.Shoot.open_camera_detail()

    def test_open_left_view(self):
        """机位详情页-打开左侧侧边栏"""
        Chrome.Shoot.open_left_view()

    def test_download(self):
        """机位详情页-批量操作-全选下载"""
        Chrome.Shoot.select_all_files()
        Chrome.Shoot.download_files()

    def test_copy_to_shoot(self):
        """机位详情页-批量操作-复制到拍摄"""
        Chrome.Shoot.select_all_files()
        Chrome.Shoot.copy_files_to_shoot()
        Chrome.Shoot.refresh()
        Chrome.Shoot.open_left_view()
        Chrome.Shoot.check_copy_to_shoot()

    def test_copy_to_media(self):
        """机位详情页-批量操作-复制到资源"""
        Chrome.Shoot.select_all_files()
        Chrome.Shoot.copy_to_media()

    def test_delete_files(self):
        """机位详情页-批量操作-删除"""
        Chrome.Shoot.select_camera(copy_camera)
        Chrome.Shoot.select_all_files()
        Chrome.Shoot.delete_files()
        Chrome.Shoot.check_delete(copy_camera)

    def test_hide_left_view(self):
        """机位详情页-隐藏左边侧边栏"""
        Chrome.Shoot.close_left_view()
        Chrome.Shoot.hide_left_view()

    def test_show_left_view(self):
        """机位详情页-显示左边侧边栏"""
        Chrome.Shoot.show_left_view()

    @staticmethod
    def teardown_class():
        Chrome.Shoot.back_to_shoot_index()