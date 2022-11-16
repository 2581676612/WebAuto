from core.browser.chrome import Chrome


class TestCase():
    def test_add_version(self):
        """版本管理-添加版本"""
        Chrome.Project.open_project()
        Chrome.Project.add_version(file_type='video', file_name='video.mp4')

    def test_compare_version(self):
        """版本管理-对比"""
        Chrome.Project.enter_file_detail_view(file_type='video')
        Chrome.Project.compare_version()

    def test_share_one_version(self):
        """版本管理-分享单版本"""
        Chrome.Project.check_share_version_status()
        share_link = Chrome.Project.share(version='V1', detail_view=True)
        Chrome.Control.open_another_page(share_link)
        Chrome.Control.switch_to_another_page()
        Chrome.Control.wait(5)
        Chrome.Control.close_guide()
        Chrome.Project.check_many_version(many=False)
        Chrome.Control.close_another_page()

    def test_share_all_version(self):
        """版本管理-分享全部版本"""
        share_link = Chrome.Project.share(version='ALL', detail_view=True)
        Chrome.Control.open_another_page(share_link)
        Chrome.Control.switch_to_another_page()
        Chrome.Control.wait(5)
        Chrome.Control.close_guide()
        Chrome.Project.check_many_version(many=True)
        Chrome.Control.close_another_page()

    def test_remove_version(self):
        """版本管理-删除版本"""
        Chrome.Project.remove_version()

    @staticmethod
    def teardown_class():
        Chrome.Project.enter_project_view()