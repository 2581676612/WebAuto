import pytest
import core.base.parse as parse

from py._xmlgen import html
from core.browser.chrome import Chrome
from core.browser.firefox import FireFox
from core.base.logger import logger

_driver = None


def pytest_configure(config):
    # Environment配置
    # config._metadata.pop('JAVA_HOME')
    config._metadata.pop('Packages')
    # config._metadata.pop('Platform')
    config._metadata.pop('Plugins')
    # config._metadata.pop('Python')


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p(f'测试人员：{parse.test_people}')])


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    # if report.when == 'teardown':
    if report.when == 'call' or report.when == 'setup':
        xfail = hasattr(report, 'wasfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            chrome_name = report.nodeid.replace("::", "_") + ".png"
            chrome_img = _chrome_screenshot()
            if chrome_img:
                if chrome_name:
                    html = f'<div><img src="data:image/png;base64,{chrome_img}" alt="screenshot" style="width:800px;height:400px;"></div>'
                    extra.append(pytest_html.extras.html(html))
            else:
                logger.info('Chrome非运行状态，无需截图！')
            firefox_name = report.nodeid.replace("::", "_") + ".png"
            firefox_img = _firefox_screenshot()
            if firefox_img:
                if firefox_name:
                    f_html = f'<div><img src="data:image/png;base64,{firefox_img}" alt="screenshot" style="width:800px;height:400px;"></div>'
                    extra.append(pytest_html.extras.html(f_html))
            else:
                logger.info('Firefox非运行状态，无需截图！')
            report.extra = extra


def _chrome_screenshot():
    '''截图保存为base64'''
    if Chrome and Chrome.Control.driver_status:
        return Chrome.driver.get_screenshot_as_base64()
    else:
        return False


def _firefox_screenshot():
    '''截图保存为base64'''
    if FireFox and FireFox.Control.driver_status:
        return FireFox.driver.get_screenshot_as_base64()
    else:
        return False


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.pop()
