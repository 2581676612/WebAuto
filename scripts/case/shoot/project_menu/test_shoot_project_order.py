import pytest

from core.browser.chrome import Chrome


class TestCase():
    def test_hide_project_list(self):
        """拍摄项目-隐藏项目列表"""
        Chrome.Shoot.hide_my_project_list()

    def test_show_project_list(self):
        """拍摄项目-显示项目列表"""
        Chrome.Shoot.show_my_project_list()

    def test_order_project(self):
        """项目排序-按创建时间由旧到新"""
        Chrome.Shoot.order_my_project_by_time_old_2_new()

    def test_order_project_1(self):
        """项目排序-按文件名正序"""
        Chrome.Shoot.order_my_project_by_name()

    def test_order_project_2(self):
        """项目排序-按文件名倒序"""
        Chrome.Shoot.order_my_project_by_name_reverse()

    @staticmethod
    def teardown_class():
        Chrome.Control.refresh()