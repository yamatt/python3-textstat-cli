import os
import unittest
from unittest.mock import Mock
import tempfile

from textstat_cli.textstat import TextStat

from textstat_cli.cli import TextStatCli


class TestTextStatCLI(unittest.TestCase):
    def test_textstat_singleton(self):
        test_textstatcli = TextStatCli(None)
        self.assertIsNone(test_textstatcli._textstat)
        result = test_textstatcli.textstat
        self.assertIsNotNone(test_textstatcli._textstat)
        self.assertEqual(id(result), id(test_textstatcli.textstat))
        self.assertIsInstance(result, TextStatCli.TEXTSTAT)

    def test_tests_exist(self):
        """Validates that the tests I manually pulled out of textstat exist in
        the original library.
        """
        for test_name in TextStatCli.TESTS:
            self.assertTrue(
                hasattr(TextStat, test_name),
                "'{test_name}' was not found in textstat".format(test_name=test_name),
            )

    def test_from_args_cls(self):
        class MockArgs:
            path = ["test path"]
            language = "test language"

        test_textstatcli = TextStatCli.from_args(MockArgs)
        self.assertEqual(test_textstatcli.paths, MockArgs.path)
        self.assertEqual(test_textstatcli.language, MockArgs.language)

    def test_file_walk_single_file(self):
        single_file = "samples/lorium.txt"
        test_textstatcli = TextStatCli([single_file])
        self.assertEqual(test_textstatcli.files[0].f.name, single_file)

    def test_extension_check(self):
        test_textstatcli = TextStatCli(None)
        self.assertTrue(test_textstatcli._extension_ok("file.md"))
        self.assertTrue(test_textstatcli._extension_ok("/long/path/to/file.md"))
        self.assertFalse(test_textstatcli._extension_ok("file"))
        self.assertFalse(test_textstatcli._extension_ok("/long/path/to/file"))
        self.assertFalse(test_textstatcli._extension_ok("file.odt"))
        self.assertFalse(test_textstatcli._extension_ok("/long/path/to/file.odt"))

    def test_add_files(self):
        test_textstatcli = TextStatCli(None)
        self.assertTrue(len(test_textstatcli._files) == 0)
        with tempfile.NamedTemporaryFile() as temp_file:
            test_textstatcli._add_file(temp_file.name)
            self.assertTrue(len(test_textstatcli._files) == 1)
            self.assertIsInstance(
                test_textstatcli._files[0], test_textstatcli.TEXTSTATFILE
            )
            self.assertEqual(test_textstatcli._files[0].f.name, temp_file.name)

    def test_to_dictionary(self):
        class MockFile:
            MOCK_FILE_DICT = {"foo": "bar"}

            class f:
                # mock file object
                name = "test name"

            @staticmethod
            def to_dict():
                return MockFile.MOCK_FILE_DICT

        test_textstatcli = TextStatCli(None)
        test_textstatcli._files = [MockFile]

        self.assertEqual(
            test_textstatcli.to_dict(), {MockFile.f.name: MockFile.MOCK_FILE_DICT}
        )


class TestTextStatCLIWalk(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_claim_file = Mock()

        self.test_textstatcli = TextStatCli([self.temp_dir.name])
        self.test_textstatcli._claim_file = self.mock_claim_file

    def create_file(self, path):
        file_path = os.path.join(self.temp_dir.name, path)
        f = open(file_path, "w")
        f.close()
        return file_path

    def test_no_files(self):
        self.test_textstatcli._paths_walk()
        self.mock_claim_file.assert_not_called()

    def test_single_file(self):
        file_path = self.create_file("file.txt")
        self.test_textstatcli._paths_walk()
        self.mock_claim_file.assert_called()
        self.assertTrue(self.mock_claim_file.call_count == 1)

    def test_acceptable_file(self):
        self.create_file("file.txt")
        self.test_textstatcli._paths_walk()
        self.mock_claim_file.assert_called()
        self.assertTrue(self.mock_claim_file.call_count == 1)

    def test_sub_directory(self):
        temp_sub_dir_name = "subdir"
        temp_sub_dir_path = os.path.join(self.temp_dir.name, temp_sub_dir_name)
        temp_sub_file_path = os.path.join(temp_sub_dir_path, "file.txt")

        os.mkdir(temp_sub_dir_path)

        f = open(temp_sub_file_path, "w")
        f.close()

        self.test_textstatcli._paths_walk()
        self.mock_claim_file.assert_called()
        self.assertTrue(self.mock_claim_file.call_count == 1)

    def test_mutliple_files(self):
        self.create_file("file1.txt")
        self.create_file("file2.txt")

        self.test_textstatcli._paths_walk()
        self.mock_claim_file.assert_called()
        self.assertTrue(self.mock_claim_file.call_count == 2)
