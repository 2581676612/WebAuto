from core.browser.chrome import Chrome
from core.base.base_case import BaseCaseFile


class TestCaseFileImgDetail(BaseCaseFile):
    def test_file_detail_view(self):
        """进入文件详情页"""
        Chrome.Project.enter_file_detail_view(file_type='img')
        Chrome.Project.check_in_file_detail_view()

    def test_file_change(self):
        """切换文件"""
        Chrome.Project.change_file_in_detail_view()

    def test_img_fill(self):
        """图片上下/左右撑满"""
        Chrome.Project.set_img_fill_height()
        Chrome.Project.set_img_fill_width()

    def test_img_change_size(self):
        """图片放大/缩小"""
        Chrome.Project.set_img_smaller()
        Chrome.Project.set_img_larger()

    def test_img_control_map(self):
        """打开/关闭画面小地图"""
        Chrome.Project.control_img_small_map(show=True)
        Chrome.Project.control_img_small_map(show=False)

    def test_img_keyboard_guide(self):
        """键盘快捷键"""
        Chrome.Project.open_keyboard_guide()
        Chrome.Project.close_keyboard_guide()

    def test_img_max_screen(self):
        """文件全屏显示"""
        Chrome.Project.file_max_view()
        Chrome.Project.file_quit_max_view()

    @staticmethod
    def teardown_class():
        Chrome.Project.back_to_project_index()
