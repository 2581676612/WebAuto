import pytest
from .parse import loop_count
from .web import Chrome


class BaseCase():
    pass


@pytest.mark.repeat(loop_count)
class BaseLoopCase():
    pass


class BaseCaseFile():
    pass
    # @staticmethod
    # def setup_class():
    #     Chrome.create_project_quickly()
    #     Chrome.open_project()
    #     Chrome.upload_file(select_all=True)
    #     Chrome.wait_upload()

    # @staticmethod
    # def teardown_class():
    #     Chrome.delete_project()