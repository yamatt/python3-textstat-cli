import click

from .cli import Language, TextStatCli
from .renderers import render_human_output, render_json_output


@click.command()
@click.option("--language", "-l", default=Language.ENGLISH_US, help="Language to use as defined by en_US.", type=click.Choice(Language, case_sensitive=False)
)
@click.option("--json", "-j", is_flag=True, default=False, help="Use argument to have the results output as json."
)
@click.argument("paths", nargs=-1)
def main(language, json, paths):
    """
    Main entry point for this CLI.
    """
    textstat_cli = TextStatCli(paths=paths, language=language)
    if json:
        render_json_output(textstat_cli)
    else:
        render_human_output(textstat_cli)


if __name__ == "__main__":
    main()
