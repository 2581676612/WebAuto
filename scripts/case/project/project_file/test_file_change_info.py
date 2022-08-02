from code.web import Chrome
from code.base_case import BaseCase


class TestCaseFileChangeInfo(BaseCase):
    def test_change_name(self):
        """修改文件名称"""
        Chrome.choose_test_file()
        Chrome.change_file_name_by_info()

    def test_change_graded(self):
        """修改文件评分"""
        Chrome.change_file_grade_by_info()

    def test_change_discription(self):
        """修改文件描述"""
        Chrome.change_file_discription_by_info()

    def test_change_tag(self):
        """修改文件标签"""
        Chrome.change_file_tag_by_info()

    def test_change_link(self):
        """修改文件链接"""
        Chrome.change_file_link_by_info()


