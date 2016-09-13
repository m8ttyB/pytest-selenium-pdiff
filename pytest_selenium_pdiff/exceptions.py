class MissingScreenshot(AssertionError):
    def __init__(self, screenshot_name, screenshot_path, *args, **kwargs):
        message = 'Cannot find the screenshot named ' \
                  '"{}" at {}, screenshot capture is disabled.'

        message = message.format(screenshot_name,
                                 screenshot_path
                                 )

        super(MissingScreenshot, self).__init__(message, *args, **kwargs)


class ScreenshotMismatch(AssertionError):
    def __init__(self, screenshot_name, expected_screenshot, captured_screenshot, command_output, *args, **kwargs):
        message = 'Captured screenshot named "{}", does not match stored ' \
                  'screenshot "{}", perceptualdiff returned: "{}".  '

        message = message.format(
            screenshot_name,
            expected_screenshot,
            command_output
        )

        self.screenshot_name = screenshot_name
        self.expected_screenshot = expected_screenshot
        self.captured_screenshot = captured_screenshot
        self.command_output = command_output

        super(ScreenshotMismatch, self).__init__(message, *args, **kwargs)


class ScreenshotMismatchWithDiff(AssertionError):
    def __init__(self, screenshot_name, expected_screenshot,
                 actual_screenshot, screenshot_comparison,
                 command_output, *args, **kwargs):
        message = 'Expected "{}" to match reference screenshot "{}", highlighted differences "{}".  Command output: {}'.format(
            actual_screenshot,
            expected_screenshot,
            screenshot_comparison,
            command_output
        )

        message = message.format(
            screenshot_name,
            expected_screenshot,
            screenshot_comparison,
            command_output
        )

        self.screenshot_name = screenshot_name
        self.expected_screenshot = expected_screenshot
        self.captured_screenshot = actual_screenshot
        self.screenshot_comparison = screenshot_comparison
        self.command_output = command_output

        super(ScreenshotMismatchWithDiff, self).__init__(message, *args, **kwargs)
