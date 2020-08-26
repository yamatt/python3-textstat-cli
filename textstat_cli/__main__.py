import argparse
from json import dumps as json_dumps

import textstat

from .cli import TextStatCli

def get_args():
    parser = argparse.ArgumentParser(description='Get stats about text files')
    parser.add_argument('--language', '-l',
        default="en_US",
        help='Language to use as defined by en_US.'
    )
    parser.add_argument('--json', '-j', action='store_false',
        help='Use argument to have the results output as json.'
    )
    parser.add_argument('path', help='Where to find these files to parse.')

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    textstat_cli = TextStatCli.from_args(args)
    result = dict(textstat_cli)
    if args.json:
        print(json_dumps(result))
    else:
        for file_name in result:
            print(file_name)
            for test in result[file_name]:
                print("\t{test}: {score}".format(
                    test=test,
                    score=result[file_name][test]
                ))
