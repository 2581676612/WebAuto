import pytest

from core.browser.firefox import FireFox
from core.browser.chrome import Chrome
from core.base.parse import usr_2, pwd_2


class TestCase():
    def test_open_member_view_by_icon(self):
        """会议-点击头像打开成员管理页面"""
        Chrome.Shoot.open_member_view_by_icon()

    @pytest.mark.P0
    def test_create_meeting(self):
        """会议-创建会议"""
        Chrome.Shoot.create_meeting()

    @pytest.mark.P0
    def test_meeting_voice(self):
        """会议-麦克风静音"""
        Chrome.Shoot.click_voice_in_meeting_dialog_view()
        Chrome.Shoot.check_voice_status_in_meeting_dialog_view(silent=True)
        Chrome.Shoot.click_voice_in_meeting_dialog_view()
        Chrome.Shoot.check_voice_status_in_meeting_dialog_view(silent=False)
        Chrome.Shoot.close_meeting_dialog()
        Chrome.Shoot.click_voice_in_meeting_title()
        Chrome.Shoot.check_voice_status_in_meeting_title(silent=True)
        Chrome.Shoot.click_voice_in_meeting_title()
        Chrome.Shoot.check_voice_status_in_meeting_title(silent=False)

    @pytest.mark.P0
    def test_meeting_invite(self):
        """会议-邀请加入会议"""
        url = Chrome.Shoot.create_meeting_link()
        FireFox.Control.show_browser()
        # FireFox.Control.login_by_password(usr_2, pwd_2)
        FireFox.Shoot.join_meeting_by_link(url=url)
        Chrome.Shoot.check_join_meeting(FireFox.Control.user_name)

    @pytest.mark.P0
    def test_remove_member(self):
        """会议-移除会议成员"""
        if Chrome.Control.is_team():
            pytest.skip('团队版暂不支持邀请，无法测试移除')
        Chrome.Shoot.remove_meeting_member(FireFox.Control.user_name)

    @pytest.mark.P0
    def test_join_meeting(self):
        """会议-点击按钮加入会议"""
        if Chrome.Control.is_team():
            pytest.skip('团队版暂不支持邀请，无法验证')
        FireFox.Shoot.join_meeting_by_button()
        Chrome.Shoot.check_join_meeting(FireFox.Control.user_name)

    @pytest.mark.P0
    def test_meeting_host_translate(self):
        """会议-会议主持人移交"""
        if Chrome.Control.is_team():
            pytest.skip('团队版暂不支持邀请，无法验证')
        Chrome.Shoot.leave_meeting()
        FireFox.Shoot.check_host_translate()

    @pytest.mark.P0
    def test_meeting_close(self):
        """会议-全员结束会议"""
        if Chrome.Control.is_team():
            Chrome.Shoot.close_meeting()
        else:
            FireFox.Shoot.close_meeting()
            FireFox.Control.hide_browser()
