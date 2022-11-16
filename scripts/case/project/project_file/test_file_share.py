import time

from core.browser.chrome import Chrome


class TestCase():
    @staticmethod
    def setup_class():
        Chrome.Project.open_project()

    def test_share(self):
        """分享-链接"""
        Chrome.Project.select_all_file()
        share_link = Chrome.Project.share()
        Chrome.Control.open_another_page(share_link)
        Chrome.Control.switch_to_another_page()
        time.sleep(5)
        Chrome.Control.close_guide()

    def test_collect(self):
        """分享-收藏"""
        Chrome.Project.collect()

    def test_download_in_share_page(self):
        """分享-下载"""
        Chrome.Project.download_in_share_page()

    def test_move_in_share_page(self):
        """分享-转存"""
        Chrome.Project.move()

    def test_share_permission(self):
        """分享-分享设置"""
        Chrome.Control.switch_to_main_page()
        Chrome.Link.enter_link_view()
        Chrome.Link.open_project_share_settings()
        Chrome.Link.close_project_share_permission('允许评论', '允许下载和转存')
        Chrome.Link.close_share_setting_dialog()
        Chrome.Project.enter_project_view()
        Chrome.Control.switch_to_another_page()
        Chrome.Control.refresh()
        Chrome.Project.check_share_download_permission(download=False)
        Chrome.Project.check_share_move_permission(move=False)
        Chrome.Project.enter_share_file_detail()
        Chrome.Control.close_guide()
        Chrome.Project.check_share_comment_permission(comment=False)

    @staticmethod
    def teardown_class():
        Chrome.Control.close_another_page()
