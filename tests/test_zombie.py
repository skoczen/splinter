import unittest
from splinter.browser import Browser
from base import BaseBrowserTests
from fake_webapp import EXAMPLE_APP


class ZombieTest(BaseBrowserTests, unittest.TestCase):
# class ZombieTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('zombiejs')

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_foo(self):
        pass

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
