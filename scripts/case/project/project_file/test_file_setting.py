from code.web import Chrome
from code.base_case import BaseCaseFile


class TestCaseFileSetting(BaseCaseFile):
    def test_file_select_all(self):
        """选中文件测试"""
        Chrome.select_all_file()
        Chrome.close_choose_file()

    def test_file_unselect(self):
        """取消选中测试"""
        Chrome.open_project()
        Chrome.unselect_file()
        Chrome.close_choose_file()

    def test_file_pre_view(self):
        """预览测试"""
        Chrome.choose_test_file()
        Chrome.click_space()
        Chrome.check_pre_view()
        Chrome.click_space()

    def test_file_create_dir(self):
        """用选中文件创建文件夹"""
        Chrome.create_dir_by_file()

    def test_file_copy(self):
        """复制文件"""
        Chrome.open_project()
        Chrome.delete_project('测试-复制')
        Chrome.create_project_quickly('测试-复制')
        Chrome.open_project()
        Chrome.copy_all_files('测试-复制')
        Chrome.delete_project('测试-复制')

    def test_file_move(self):
        """移动文件"""
        Chrome.open_project()
        Chrome.delete_project('测试-移动')
        Chrome.create_project_quickly('测试-移动')
        Chrome.open_project()
        Chrome.move_all_files('测试-移动')

    def test_file_download(self):
        """下载文件"""
        Chrome.open_project('测试-移动')
        Chrome.download_all_files()

    def test_all_delete(self):
        """删除全部文件"""
        Chrome.delete_all_files()
        Chrome.delete_project('测试-移动')