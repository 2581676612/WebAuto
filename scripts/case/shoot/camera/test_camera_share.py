from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    def test_share_can_read(self):
        """分享-分享者有查看文件权限"""
        share_url = Chrome.Shoot.create_share_link()
        FireFox.Shoot.open_page(share_url)
        FireFox.Shoot.check_open_share_link(read=True)
        FireFox.Shoot.enter_shoot_page()

    def test_share_can_not_read(self):
        """分享-分享者无查看文件权限"""
        FireFox.Shoot.open_join_project()
        FireFox.Shoot.show_browser()
        share_url = FireFox.Shoot.create_share_link()
        FireFox.Shoot.hide_browser()
        Chrome.Shoot.open_page(share_url)
        Chrome.Shoot.check_open_share_link(read=False)
        Chrome.Shoot.enter_shoot_page()
