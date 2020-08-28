import unittest

from textstat_cli.__main__ import create_args


class TestGetArgs(unittest.TestCase):
    def test_use_json(self):
        args = create_args().parse_args("--json".split(" "))
        self.assertTrue(args.use_json_output)

    def test_not_use_json(self):
        args = create_args().parse_args("".split(" "))
        self.assertFalse(args.use_json_output)
