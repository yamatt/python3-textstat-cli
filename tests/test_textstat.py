import unittest
from unittest.mock import Mock

from textstat_cli.textstat import TextStat


class TestTextStat(unittest.TestCase):
    def setUp(self):
        self.sample_text = open("samples/lorium.txt").read()
        self.sample_text_wc = 460

    def test_default_initialization(self):
        test_textstat = TextStat()
        self.assertEqual(test_textstat._textstatistics__lang, "en_US")

    def test_setting_language_at_initialization(self):
        TEST_VALUE = "A test value"
        test_textstat = TextStat(language=TEST_VALUE)
        self.assertEqual(test_textstat._textstatistics__lang, TEST_VALUE)

    def test_reading_speed(self):
        test_textstat = TextStat()
        self.assertEqual(test_textstat.reading_speed(self.sample_text, 100), 4.6)

    def check_reading_speed(self, wpm):
        test_textstat = TextStat()
        test_textstat.reading_speed = Mock()

        function_name = "time_to_read_{wpm}wpm".format(wpm=wpm)

        getattr(test_textstat, function_name)(self.sample_text)

        test_textstat.reading_speed.assert_called()
        self.assertEqual(test_textstat.reading_speed.call_args.args[1], wpm)

    def test_reading_speeds(self):
        for wpm in [100, 130, 160]:
            self.check_reading_speed(wpm)
