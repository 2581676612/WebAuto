import pytest
from core.base.parse import loop_count
from core.browser.chrome import Chrome


class BaseCase():
    pass


@pytest.mark.repeat(loop_count)
class BaseLoopCase():
    pass
