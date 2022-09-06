from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    @staticmethod
    def setup_class():
        Chrome.Project.open_project()

    def test_upload_img(self):
        """文件列表-上传文件"""
        Chrome.Project.upload_file(select_all=True)  # 选择test_file文件夹下的文件
        Chrome.Project.wait_upload()

    def test_upload_dir(self):
        """文件列表-上传文件夹"""
        Chrome.Project.upload_dir()
        Chrome.Project.wait_upload()

    @staticmethod
    def teardown_class():
        Chrome.Project.delete_dir('upload_file')
