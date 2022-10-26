from core.browser.chrome import Chrome
from core.base import parse


class TestCase():
    def test_delete_group(self):
        """资产首页-删除资产组"""
        Chrome.Assets.delete_assets_group(parse.project_name)