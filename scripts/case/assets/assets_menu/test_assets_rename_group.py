from core.browser.chrome import Chrome
from core.base import parse


class TestCase():
    def test_rename_group(self):
        """资产首页-重命名资产组"""
        Chrome.Assets.rename_assets_group(parse.project_name, '测试-修改')
        Chrome.Assets.rename_assets_group('测试-修改', parse.project_name)
