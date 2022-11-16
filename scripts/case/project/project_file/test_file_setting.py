from core.browser.chrome import Chrome


class TestCase():
    @staticmethod
    def setup_class():
        Chrome.Project.open_project()

    def test_top(self):
        """文件设置-置顶"""
        Chrome.Project.set_top()

    def test_read_status(self):
        """文件设置-审阅状态"""
        Chrome.Project.set_read_status(status='待审核')
        Chrome.Project.check_read_status(status='待审核')

    def test_file_select_all(self):
        """文件列表-全选文件"""
        Chrome.Project.select_all_file()
        Chrome.Project.close_choose_file()

    def test_file_unselect(self):
        """文件列表-取消全选"""
        Chrome.Project.open_project()
        Chrome.Project.unselect_file()
        Chrome.Project.close_choose_file()

    def test_file_pre_view(self):
        """文件列表-预览"""
        Chrome.Project.choose_test_file()
        Chrome.Project.click_space()
        Chrome.Project.check_pre_view()
        Chrome.Project.click_space()

    def test_file_create_dir(self):
        """文件列表-用选中文件创建文件夹"""
        Chrome.Project.create_dir_by_file()

    def test_file_copy(self):
        """文件列表-复制文件"""
        Chrome.Project.open_project()
        Chrome.Project.delete_project('测试-复制')
        Chrome.Project.create_project_quickly('测试-复制')
        Chrome.Project.open_project()
        Chrome.Project.copy_all_files('测试-复制')
        Chrome.Project.delete_project('测试-复制')

    def test_file_move(self):
        """文件列表-移动文件"""
        Chrome.Project.open_project()
        Chrome.Project.delete_project('测试-移动')
        Chrome.Project.create_project_quickly('测试-移动')
        Chrome.Project.open_project()
        Chrome.Project.move_all_files('测试-移动')

    def test_file_download(self):
        """文件列表-下载文件"""
        Chrome.Project.open_project('测试-移动')
        Chrome.Project.download_all_files(vip=Chrome.Control.vip)

    def test_all_delete(self):
        """文件列表-删除全部文件"""
        Chrome.Project.delete_all_files()
        Chrome.Project.delete_project('测试-移动')

    @staticmethod
    def teardown_class():
        Chrome.Project.open_project()
        Chrome.Project.upload_file(select_all=True)
        Chrome.Project.wait_upload()