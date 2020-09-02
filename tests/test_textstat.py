import unittest

from textstat_cli.textstat import TextStat


class TestTextStat(unittest.TestCase):
    def test_default_initialization(self):
        test_textstat = TextStat()
        self.assertEqual(test_textstat._textstatistics__lang, "en_US")

    def test_setting_language_at_initialization(self):
        TEST_VALUE = "A test value"
        test_textstat = TextStat(language=TEST_VALUE)
        self.assertEqual(test_textstat._textstatistics__lang, TEST_VALUE)
