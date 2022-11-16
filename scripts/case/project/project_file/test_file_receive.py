from core.browser.chrome import Chrome


class TestCase():
    def test_receive_file(self):
        """文件列表-收集文件"""
        Chrome.Project.open_project()
        receive_link = Chrome.Project.create_receive_link()
        Chrome.Control.open_another_page(receive_link)
        Chrome.Control.switch_to_another_page()
        Chrome.Control.wait(5)
        Chrome.Project.upload_file_by_receive_link(file='img.jpg')
        Chrome.Control.switch_to_main_page()
        Chrome.Project.check_receive()

    @staticmethod
    def teardown_class():
        Chrome.Control.close_another_page()
        Chrome.Project.enter_project_view()