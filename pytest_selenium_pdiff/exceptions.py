class MissingScreenshot(AssertionError):
    def __init__(self, screenshot_name, screenshot_path, *args, **kwargs):
        message = 'Cannot find the screenshot named ' \
                  '"{}" at {}, screenshot capture is disabled.'

        message = message.format(screenshot_name,
                                 screenshot_path
                                 )

        super(MissingScreenshot, self).__init__(message, *args, **kwargs)


class ScreenshotMismatch(AssertionError):
    def __init__(self, screenshot_name, expected_screenshot, captured_screenshot, pdiff_output, *args, **kwargs):
        message = 'Captured screenshot named "{}", does not match stored ' \
                  'screenshot "{}", perceptualdiff returned: "{}".  '

        message = message.format(
            screenshot_name,
            expected_screenshot,
            pdiff_output
        )

        self.screenshot_name = screenshot_name
        self.expected_screenshot = expected_screenshot
        self.captured_screenshot = captured_screenshot
        self.pdiff_output = pdiff_output

        super(ScreenshotMismatch, self).__init__(message, *args, **kwargs)


class ScreenshotMismatchWithDiff(AssertionError):
    def __init__(self, screenshot_name, expected_screenshot,
                 captured_screenshot, pdiff_comparison,
                 pdiff_output, *args, **kwargs):
        message = 'Captured screenshot named "{}", does not match stored screenshot "{}".  ' \
                  'Diff is available at: "{}", perceptualdiff returned: {}.'

        message = message.format(
            screenshot_name,
            expected_screenshot,
            pdiff_comparison,
            pdiff_output
        )

        self.screenshot_name = screenshot_name
        self.expected_screenshot = expected_screenshot
        self.captured_screenshot = captured_screenshot
        self.pdiff_comparison = pdiff_comparison
        self.pdiff_output = pdiff_output

        super(ScreenshotMismatchWithDiff, self).__init__(message, *args, **kwargs)
