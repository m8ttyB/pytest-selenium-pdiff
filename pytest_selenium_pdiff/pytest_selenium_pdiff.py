import base64
import os

import pytest

from . import exceptions

settings = {
    'SCREENSHOTS_PATH': None,
    'PDIFF_PATH': None,
    'ALLOW_SCREENSHOT_CAPTURE': False
}

SCREENSHOT_EXCEPTION_TYPES = (
    exceptions.ScreenshotMismatchWithDiff,
    exceptions.ScreenshotMismatch
)


def pytest_addoption(parser):
    group = parser.getgroup('selenium-pdiff', 'selenium-pdiff')
    group._addoption('--allow-screenshot-capture',
                     help='Allow capturing of missing screenshots.',
                     metavar='bool')
    group._addoption('--screenshots-path',
                     help='Path for captured screenshots.',
                     metavar='str')
    group._addoption('--pdiff-path',
                     metavar='path',
                     help='path to pdiff output')

    selenium_exclude_debug = os.environ.get('SELENIUM_EXCLUDE_DEBUG', '')
    if 'screenshot' not in selenium_exclude_debug:
        selenium_exclude_debug += ' screenshot'

    os.environ['SELENIUM_EXCLUDE_DEBUG'] = selenium_exclude_debug


def pytest_configure(config):
    settings['SCREENSHOTS_PATH'] = config.getoption('screenshots_path')
    settings['PDIFF_PATH'] = config.getoption('pdiff_path')
    settings['ALLOW_SCREENSHOT_CAPTURE'] = config.getoption('allow_screenshot_capture')

    if 'ALLOW_SCREENSHOT_CAPTURE' in os.environ:
        settings['ALLOW_SCREENSHOT_CAPTURE'] = True


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.extra = getattr(report, 'extra', [])

    xfail = hasattr(report, 'wasxfail')
    failure = (report.skipped and xfail) or (report.failed and not xfail)

    if failure and call.excinfo:
        exception = call.excinfo.value

        if isinstance(exception, SCREENSHOT_EXCEPTION_TYPES):
            report.extra.append(pytest_html.extras.image(
                get_image_as_base64(exception.expected_screenshot),
                'PDIFF: Expected'
            ))

            if isinstance(exception, exceptions.ScreenshotMismatchWithDiff):
                report.extra.append(pytest_html.extras.image(
                    get_image_as_base64(exception.pdiff_comparison),
                    'PDIFF: Comparison'
                ))

            report.extra.append(pytest_html.extras.image(
                get_image_as_base64(exception.captured_screenshot),
                'PDIFF: Actual'
            ))


def get_image_as_base64(filename):
    with open(filename, 'rb') as fp:
        content = fp.read()
        b64_image = base64.b64encode(content).decode('ascii')
    return b64_image
