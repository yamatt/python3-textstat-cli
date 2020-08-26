import argparse

import textstat

from .cli import TextStatCli

def get_args():
    parser = argparse.ArgumentParser(description='Get stats about text files')
    parser.add_argument('--language', '-l',
        default="en_US",
        help='Language to use as defined by en_US'
    )
    parser.add_argument('path', help='Where to find these files to parse')

    args = parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    textstat_cli = TextStatCli.from_args(args)
    print(textstat_cli.to_json())
