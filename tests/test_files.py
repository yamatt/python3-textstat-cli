import unittest
from unittest.mock import Mock

from textstat_cli.cli import TextStat

class TestTextStatFile(unittest.TestCase):

    def test_getattr(self):
        class mock_textstatcli:
            class textstat:
                mock_attr = "test result"
        textstatfile = TextStatFile(None, mock_textstatcli)
        self.assertEqual(textstatfile.textstat, mock_textstatcli.textstat.mock_attr)
        self.assertRaises(AttributeError, textstatfile.fake_attribute)

    def test_to_dict(self):
        class mock_textstatcli:
            TESTS = [
                "mock1",
                "mock2"
            ]

            def mock1(self):
                return "mock1"

            def mock2(self):
                return "mock2"

        textstatfile = TextStatFile(None, mock_textstatcli)
        
