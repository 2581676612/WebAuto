from core.browser.chrome import Chrome
from core.browser.firefox import FireFox
from core.base.base_case import BaseCase
from core.base.parse import usr_2_name


class TestCase(BaseCase):
    def test_fangluping_open(self):
        """项目设置-防录屏权限开启"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('项目设置')
        Chrome.Project.set_fangluping(True)
        Chrome.Project.check_fangluping(True)

    def test_fangluping_close(self):
        """项目设置-防录屏权限关闭"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('项目设置')
        Chrome.Project.set_fangluping(False)
        Chrome.Project.check_fangluping(False)

    def test_role_permission(self):
        """项目设置-身份权限测试"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('项目设置')
        Chrome.Project.close_project_permission('自定义信息权限', '邀请加入', '下载文件', '分享文件', '复制文件',
                                                '删除/恢复文件', role='成员')
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('成员管理')
        Chrome.Project.change_role(usr_2_name, '成员')
        FireFox.Project.open_project()
        FireFox.Project.choose_test_file()
        FireFox.Project.check_change_info_permission_close()
        FireFox.Project.check_invite_permission_close()
        FireFox.Project.check_download_permission_close()
        FireFox.Project.check_share_permission_close()
        FireFox.Project.check_copy_permission_close()
        FireFox.Project.check_delete_permission_close()

    @staticmethod
    def teardown_class():
        FireFox.Project.enter_project_view()