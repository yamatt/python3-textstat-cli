from io import StringIO
from tempfile import NamedTemporaryFile
import unittest
from unittest.mock import Mock

from textstat_cli.files import TextStatFile


class TestTextStatFile(unittest.TestCase):
    def test_text(self):
        test_file_contents = "test file contents"
        with StringIO(test_file_contents) as test_file:
            test_textstatfile = TextStatFile(test_file, None)

            self.assertIsNone(test_textstatfile._text)
            test_text_result = test_textstatfile.text
            self.assertEqual(test_textstatfile.text, test_file_contents)
            self.assertEqual(id(test_textstatfile.text), id(test_text_result))
            self.assertEqual(test_textstatfile._text, test_file_contents)

    def test_to_dictionary(self):
        test_method_friendly_name = "Test Method Name"
        test_method_name = "test1"
        test_method_result = "result1"

        class MockTextStatCLI:
            TESTS = {test_method_friendly_name: test_method_name}

            textstat = Mock(return_value=test_method_result)

        test_textstatfile = TextStatFile(None, MockTextStatCLI)

        result = test_textstatfile.to_dict()

        self.assertTrue(test_method_friendly_name in result.keys())
        getattr(MockTextStatCLI.textstat, test_method_name).assert_called()

    def test_from_path_cls(self):
        mock_textstatcli = Mock()
        with NamedTemporaryFile() as temp_file:
            test_textstatfile = TextStatFile.from_path(temp_file.name, mock_textstatcli)
            self.assertIsNotNone(test_textstatfile.f)
            self.assertEqual(test_textstatfile.cli, mock_textstatcli)
