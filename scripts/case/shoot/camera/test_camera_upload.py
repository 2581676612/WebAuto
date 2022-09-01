from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_upload_img(self):
        """机位配置-上传文件测试"""
        Chrome.Shoot.upload_file(camera="测试机位-自动化", select_all=True)  # 选择test_file文件夹下的文件
        Chrome.Shoot.wait_upload()

    def test_upload_dir(self):
        """机位配置-上传文件夹测试"""
        Chrome.Shoot.upload_dir(camera="测试机位-自动化")
        Chrome.Shoot.wait_upload()
