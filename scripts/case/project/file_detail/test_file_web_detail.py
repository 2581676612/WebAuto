from core.browser.chrome import Chrome


class TestCase():
    def test_file_detail_view(self):
        """网页文件内页-进入文件详情页"""
        Chrome.Project.enter_file_detail_view(file_type='web')
        Chrome.Project.check_in_file_detail_view()

    def test_check_download_status(self):
        """网页文件内页-检测下载交付图标状态"""
        Chrome.Project.check_download_icon_status(is_gray=True)

    def test_check_cover_status(self):
        """网页文件内页-检测设置封面图标状态"""
        Chrome.Project.check_cover_icon_status(is_gray=True)

    def test_check_fangluping_status(self):
        """网页文件内页-检测设置防录屏图标状态"""
        Chrome.Project.check_fangluping_icon_status(is_gray=True)

    @staticmethod
    def teardown_class():
        Chrome.Project.back_to_project_index()