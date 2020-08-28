import unittest

from textstat import textstat

from textstat_cli.cli import TextStatCli


class TestTextStatCLI(unittest.TestCase):
    def test_textstat_singleton(self):
        test_textstat = TextStatCli(None)
        self.assertNone(test_textstat._textstat)
        result = test_textstat.textstat
        self.assertIsNotNone(test_textstat._textstat)
        self.assertEqual(id(result), id(test_textstat.textstat))

    def test_tests_exist(self):
        for test_name in TextStatCli.TESTS:
            self.assertTrue(hasattr(textstat, test))

    def test_from_args_cls(self):
        class MockArgs:
            path = "test path"
            language = "test language"

        result = TextStatCli.from_args(MockArgs)
        self.assertEqual(result.root_path, MockArgs.path)
        self.assertEqual(result.language, MockArgs.language)

    def test_file_walk(self):
        pass
