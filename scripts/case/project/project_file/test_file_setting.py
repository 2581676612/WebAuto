from core.browser.chrome import Chrome
from core.base.base_case import BaseCaseFile


class TestCaseFileSetting(BaseCaseFile):
    def test_file_select_all(self):
        """选中文件测试"""
        Chrome.Project.select_all_file()
        Chrome.Project.close_choose_file()

    def test_file_unselect(self):
        """取消选中测试"""
        Chrome.Project.open_project()
        Chrome.Project.unselect_file()
        Chrome.Project.close_choose_file()

    def test_file_pre_view(self):
        """预览测试"""
        Chrome.Project.choose_test_file()
        Chrome.Project.click_space()
        Chrome.Project.check_pre_view()
        Chrome.Project.click_space()

    def test_file_create_dir(self):
        """用选中文件创建文件夹"""
        Chrome.Project.create_dir_by_file()

    def test_file_copy(self):
        """复制文件"""
        Chrome.Project.open_project()
        Chrome.Project.delete_project('测试-复制')
        Chrome.Project.create_project_quickly('测试-复制')
        Chrome.Project.open_project()
        Chrome.Project.copy_all_files('测试-复制')
        Chrome.Project.delete_project('测试-复制')

    def test_file_move(self):
        """移动文件"""
        Chrome.Project.open_project()
        Chrome.Project.delete_project('测试-移动')
        Chrome.Project.create_project_quickly('测试-移动')
        Chrome.Project.open_project()
        Chrome.Project.move_all_files('测试-移动')

    def test_file_download(self):
        """下载文件"""
        Chrome.Project.open_project('测试-移动')
        Chrome.Project.download_all_files()

    def test_all_delete(self):
        """删除全部文件"""
        Chrome.Project.delete_all_files()
        Chrome.Project.delete_project('测试-移动')

    @staticmethod
    def teardown_class():
        Chrome.Project.open_project()
        Chrome.Project.upload_file(select_all=True)
        Chrome.Project.wait_upload()