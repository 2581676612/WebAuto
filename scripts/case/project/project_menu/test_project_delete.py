from core.browser.chrome import Chrome


class TestCase():
    def test_delete(self):
        """项目设置-删除项目"""
        Chrome.Project.delete_project()
