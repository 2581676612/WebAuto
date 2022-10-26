from core.browser.chrome import Chrome
from core.base import parse


class TestCase():
    def test_create_group(self):
        """资产首页-创建资产组"""
        Chrome.Assets.create_assets_group(parse.project_name)