import unittest

from textstat.textstat import textstat

from textstat_cli.cli import TextStatCli


class TestTextStatCLI(unittest.TestCase):
    def test_textstat_singleton(self):
        test_textstatcli = TextStatCli(None)
        self.assertIsNone(test_textstatcli._textstat)
        result = test_textstatcli.textstat
        self.assertIsNotNone(test_textstatcli._textstat)
        self.assertEqual(id(result), id(test_textstatcli.textstat))

    def test_tests_exist(self):
        """Validates that the tests I manually pulled out of textstat exist in
        the original library.
        """
        for test_name in TextStatCli.TESTS:
            self.assertTrue(
                hasattr(textstat, test_name),
                "'{test_name}' was not found in textstat".format(test_name=test_name),
            )

    def test_from_args_cls(self):
        class MockArgs:
            path = "test path"
            language = "test language"

        test_textstatcli = TextStatCli.from_args(MockArgs)
        self.assertEqual(test_textstatcli.root_path, MockArgs.path)
        self.assertEqual(test_textstatcli.language, MockArgs.language)

    def test_file_walk(self):
        pass

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
