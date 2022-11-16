from core.browser.chrome import Chrome


class TestCase():
    def test_import(self):
        """网页文件-导入"""
        Chrome.Project.open_project()
        Chrome.Project.import_url(url='https://www.baidu.com')

    def test_download_permission(self):
        """网页文件-下载权限"""
        Chrome.Control.refresh()
        Chrome.Project.open_project()
        Chrome.Project.check_web_file_download_button()
        Chrome.Project.cancel_choose_file()

    def test_download_web_and_other_file(self):
        """网页文件-下载（网页+非网页文件）"""
        Chrome.Project.check_download_web_and_other_file()
        Chrome.Project.cancel_choose_file()

