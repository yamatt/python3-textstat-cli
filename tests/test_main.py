import unittest

from textstat_cli.__main__ import create_args


class TestGetArgs(unittest.TestCase):
    def test_use_json(self):
        args = create_args().parse_args("--json .".split(" "))
        self.assertTrue(args.use_json_output)
        args = create_args().parse_args("-j .".split(" "))
        self.assertTrue(args.use_json_output)

    def test_not_use_json(self):
        args = create_args().parse_args(".".split(" "))
        self.assertFalse(args.use_json_output)

    def test_path(self):
        TEST_PATH = "./test_path"
        args = create_args().parse_args("./testpath".split(" "))
        self.assertEqual(args.path, TEST_PATH)

    def test_language(self):
        TEST_LANGUAGE = "test_language"
        TEST_ARG = "--language {test_language} .".format(
            test_language=test_language
        )
        args = create_args().parse_args(TEST_ARG.split(" "))
        self.assertEqual(args.language, TEST_LANGUAGE)
