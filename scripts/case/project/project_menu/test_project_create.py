from core.browser.chrome import Chrome


class TestCase():
    def test_create(self):
        """项目设置-创建项目"""
        Chrome.Project.create_project()
