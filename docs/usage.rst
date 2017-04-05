=====
Usage
=====

To use pytest-selenium-pdiff in a project::

    import pytest-selenium-pdiff

    def test_example(self, driver):
        do_something()
        screenshot_matches(driver, 'module/my screen shot', crop=(0,0,200,200), masks=[(20,30,50,70)]


Applying crop and masks are optional.  The image is cropped before it is masked.

The crop and mask coordinates should be in the following format::

 (left, upper, right, lower)

