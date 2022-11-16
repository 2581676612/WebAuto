import pytest

from core.browser.chrome import Chrome
from core.base.parse import camera


class TestCase():
    @staticmethod
    def setup_class():
        Chrome.Shoot.open_project()
        Chrome.Shoot.open_camera_detail(camera)

    @pytest.mark.P0
    def test_set_read_status(self):
        """机位详情页-设置审阅状态"""
        Chrome.Shoot.set_read_status(status='备选')
        Chrome.Shoot.check_read_status(status='备选')

    @pytest.mark.P0
    def test_rename(self):
        """机位详情页-文件重命名"""
        Chrome.Shoot.file_rename(new_name='rename')
        Chrome.Shoot.check_rename(new_name='rename')

    @pytest.mark.P0
    def test_set_grade(self):
        """机位详情页-文件设置评分"""
        Chrome.Shoot.change_file_grade_by_info()

    @pytest.mark.P0
    def test_discussion(self):
        """机位详情页-添加意见"""
        Chrome.Shoot.add_discussion()
        Chrome.Shoot.check_discussion()
        Chrome.Shoot.add_file_in_discussion()
        Chrome.Shoot.check_file_in_discussion()
        Chrome.Shoot.delete_discussion()

    @staticmethod
    def teardown_class():
        Chrome.Shoot.back_to_shoot_index()