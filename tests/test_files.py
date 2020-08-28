from io import StringIO
from tempfile import NamedTemporaryFile
import unittest
from unittest.mock import Mock

from textstat_cli.files import TextStatFile


class TestTextStatFile(unittest.TestCase):
    def test_getattr_calls_self(self):
        class TestTextStatFile(TextStatFile):
            test_value = "test value"

        test_textstatfile = TextStatFile(None, None)

        self.assertEqual(test_textstatfile.test_value, TestTextStatFile.test_value)

    def test_getattr_calls_textstat(self):
        class MockTextStatCLI:
            textstat = Mock()

        test_method_name = "test_method_name"

        test_textstatfile = TextStatFile(None, MockTextStatCLI)

        getattr(test_textstatfile, test_method_name)()

        getattr(MockTextStatCLI.textstat, test_method_name).assert_called()

    def test_text(self):
        test_file_contents = "test file contents"
        test_file = StringIO(test_file_contents)
        test_textstatfile = TextStatFile(test_file, None)

        self.assertIsNone(test_textstatfile._text)
        test_text_result = test_textstatfile.text
        self.assertEqual(test_textstatfile.text, test_file_contents)
        self.assertEqual(id(test_textstatfile.text), id(test_text_result))
        self.assertEqual(test_textstatfile._text, test_file_contents)

    def test_to_dict(self):
        test_method_name = "test1"
        test_method_result = "result1"

        class MockTextStatCLI:
            TESTS = [test_method_name]

            textstat = Mock(return_value=test_method_result)

        test_textstatfile = TextStatFile(None, MockTextStatCLI)

        result = dict(test_textstatfile)

        self.assertTrue(test_method_name in result)
        self.assertEqual(result[test_method_name], test_method_result)

    def test_from_path_cls(self):
        mock_textstatcli = Mock()
        temp_file = NamedTemporaryFile()

        test_textstatfile = TextStatFile.from_path(temp_file.name, mock_textstatcli)
        self.assertIsNotNone(test_textstatfile.f)
        self.assertEqual(test_textstatfile.cli, mock_textstatcli)
