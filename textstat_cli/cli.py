from json import dumps
import os

from .textstat import TextStat

METHODS = [
    "flesch_reading_ease",
    "smog_index",
    "flesch_kincaid_grade",
    "coleman_liau_index",
    "automated_readability_index",
    "automated_readability_index",
    "dale_chall_readability_score",
    "difficult_words",
    "linsear_write_formula",
    "gunning_fog",
    "text_standard",
    "fernandez_huerta",
    "szigriszt_pazos",
    "gutierrez_polini",
    "crawford"
]


ACCEPTABLE_FILE_EXTENSIONS = ["txt", "md"]


def walk_path(path, cli, TextStatFile=TextStatFile):
    files = []
    for root_path, _, file_names, _ in os.fwalk(path):
        for file_name in file_names:
            # get the file extension and see if it's on the approved list
            if file_name.split(".")[-1].lower() in ACCEPTABLE_FILE_EXTENSIONS:
                files.append(
                    TextStatFile.from_path(
                        os.path.join(root_path, file_name)
                    )
                )


class TextStatCli(object):
    TEXTSTAT = TextStat
    TEXTSTATFILE = TextStatFile

    @classmethod
    def from_args(cls, args):
        return cls(
            files=walk_path(args.path),
            language=args.language
        )

    def __init__(self, files, language="en_US"):
        self.files = files
        self.language = language

        self._textstat = None

    @property
    def textstat(self):
        if not self._textstat:
            self._textstat = TextStat(language=self.language)
        return self._textstat

    def to_json(self):
        return dumps([ dict(file) for file in self.files ])


class TextStatFile(object):
    OPEN_MODE = "r"

    @classmethod
    def from_path(cls, file_path, cli):
        return cls(
            open(file_path, cls.OPEN_MODE),
            cli
        )

    def __init__(self, f, cli):
        self.f = f
        self.cli = cli

        self._text = None

    @property
    def text(self):
        if not self._text:
            self._text = self.f.read()
        return self._text

    def reload_file(self):
        self._text = None

    def __getattr__(self, attr):
        try:
            return super(TextStatFile, self).__getattr__(attr)
        except AttributeError:
            return getattr(self.cli.textstat, attr)

    def __dict__(self):
        return dict((name, getattr(name, self)()) for name in METHODS)
