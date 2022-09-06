from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_change_name(self):
        """自定义信息-修改文件名称"""
        Chrome.Project.choose_test_file()
        Chrome.Project.change_file_name_by_info()

    def test_change_graded(self):
        """自定义信息-修改文件评分"""
        Chrome.Project.change_file_grade_by_info()

    def test_change_description(self):
        """自定义信息-修改文件描述"""
        Chrome.Project.change_file_description_by_info()

    def test_change_tag(self):
        """自定义信息-修改文件标签"""
        Chrome.Project.change_file_tag_by_info()

    def test_change_link(self):
        """自定义信息-修改文件链接"""
        Chrome.Project.change_file_link_by_info()


