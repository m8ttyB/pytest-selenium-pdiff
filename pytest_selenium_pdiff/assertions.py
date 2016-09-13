import os
import shutil

from sh import perceptualdiff

from . import exceptions
from .pytest_selenium_pdiff import settings
from .utils import ensure_path_exists


def screenshot_matches(driver, screenshot_name, pixel_threshold=1):
    storage_path = settings['SCREENSHOTS_PATH']
    artifacts_path = settings['PDIFF_PATH']

    expected_screenshot = os.path.join(storage_path, screenshot_name + '.png')
    pdiff_comparison = os.path.join(artifacts_path, screenshot_name + '.diff.png')
    captured_screenshot = os.path.join(artifacts_path, screenshot_name + '.captured.png')

    ensure_path_exists(os.path.dirname(expected_screenshot))
    ensure_path_exists(os.path.dirname(pdiff_comparison))

    have_stored_screenshot = os.path.exists(expected_screenshot)

    if not have_stored_screenshot and not settings['ALLOW_SCREENSHOT_CAPTURE']:
        raise exceptions.MissingScreenshot(screenshot_name, expected_screenshot)

    driver.get_screenshot_as_file(captured_screenshot)

    if have_stored_screenshot:
        result = perceptualdiff(
            '-output', pdiff_comparison,
            '-threshold', pixel_threshold,
            expected_screenshot,
            captured_screenshot,
            _ok_code=[0, 1]
        )

        if result.exit_code == 1:
            error_message = str(result).strip()

            if os.path.exists(pdiff_comparison):
                raise exceptions.ScreenshotMismatchWithDiff(screenshot_name,
                                                            expected_screenshot,
                                                            captured_screenshot,
                                                            pdiff_comparison,
                                                            error_message)
            else:
                raise exceptions.ScreenshotMismatch(screenshot_name,
                                                    expected_screenshot,
                                                    captured_screenshot,
                                                    error_message)
    elif settings['ALLOW_SCREENSHOT_CAPTURE']:
        shutil.move(captured_screenshot, expected_screenshot)

    return True
