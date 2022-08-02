from code.web import Chrome
from code.base_case import BaseCase


class TestCaseUpload(BaseCase):
    def test_upload_img(self):
        """上传文件测试"""
        Chrome.create_project_quickly()
        Chrome.open_project()
        Chrome.upload_file('img', 'img.jpg') # 选择test_file文件夹下的文件
        Chrome.wait_upload()

    def test_upload_dir(self):
        """上传文件夹测试"""
        Chrome.upload_dir('img')
        Chrome.wait_upload()
