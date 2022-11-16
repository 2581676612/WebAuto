import pytest

from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    @pytest.mark.P0
    def test_share_can_read(self):
        """分享-分享者有查看文件权限"""
        share_url = Chrome.Shoot.create_share_link()
        FireFox.Shoot.open_page(share_url)
        FireFox.Shoot.wait(5)
        FireFox.Shoot.check_open_share_link(read=True)
        FireFox.Shoot.check_download_permission_in_share(download=False)

        Chrome.Shoot.open_share_list()
        Chrome.Shoot.open_share_setting()
        Chrome.Shoot.allow_download_in_share()
        Chrome.Shoot.save_share_setting()
        FireFox.Shoot.refresh()
        FireFox.Shoot.check_download_permission_in_share(download=True)

        Chrome.Shoot.open_share_setting()
        Chrome.Shoot.open_password_in_share()
        Chrome.Shoot.save_share_setting()
        password = Chrome.Shoot.get_share_password()
        FireFox.Shoot.refresh()
        FireFox.Shoot.check_password_in_share(password)

        Chrome.Shoot.delete_share_link()
        FireFox.Shoot.refresh()
        FireFox.Shoot.check_share_delete()

    @pytest.mark.P0
    def test_share_can_not_read(self):
        """分享-分享者无查看文件权限"""
        if Chrome.Control.is_team():
            pytest.skip('团队版暂不支持邀请，无法配置权限')
        FireFox.Shoot.open_join_project()
        FireFox.Shoot.show_browser()
        share_url = FireFox.Shoot.create_share_link()
        FireFox.Shoot.hide_browser()
        Chrome.Shoot.open_page(share_url)
        Chrome.Shoot.wait(5)
        Chrome.Shoot.check_open_share_link(read=False)

    @staticmethod
    def teardown():
        Chrome.Shoot.enter_shoot_page()
        FireFox.Shoot.enter_shoot_page()