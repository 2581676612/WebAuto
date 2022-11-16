from core.browser.chrome import Chrome


class TestCase():
    def test_enter(self):
        """首页-进入项目首页"""
        Chrome.Project.enter_project_view()
