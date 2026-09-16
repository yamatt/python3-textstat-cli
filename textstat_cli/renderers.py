from json import dumps as json_dumps


def render_human_output(textstat_cli):
    """
    Print results of the tests to the terminal
    """
    result = textstat_cli.to_dict()

    for file_name in result:
        print(file_name)
        for test in result[file_name]:
            print(f"\t{test}: {result[file_name][test]}")


def render_json_output(textstat_cli):
    """
    Print results of the tests as JSON
    """
    result = textstat_cli.to_dict()
    print(json_dumps(result))
