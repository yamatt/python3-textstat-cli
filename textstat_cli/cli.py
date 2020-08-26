import os

from .textstat import TextStat
from .files import TextStatFile


class TextStatCli(object):
    TEXTSTAT = TextStat
    TEXTSTATFILE = TextStatFile

    ACCEPTABLE_FILE_EXTENSIONS = ["txt", "md"]

    # methods for analysing text available in textstat
    TESTS = [
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

    @classmethod
    def from_args(cls, args):
        return cls(
            root_path=args.path,
            language=args.language,
        )

    def __init__(self, root_path, language="en_US"):
        self.root_path = root_path
        self.language = language

        self._textstat = None
        self._files = None

    @property
    def textstat(self):
        if not self._textstat:
            self._textstat = TextStat(language=self.language)
        return self._textstat

    @property
    def files(self):
        if not self._files:
            for root_path, _, file_names, _ in os.fwalk(self.root_path):
                for file_name in file_names:
                    # get the file extension, or the thing after the last dot
                    # in the file name, to see if it's on the approved list
                    extension = file_name.split(".")[-1].lower()
                    if extension in self.ACCEPTABLE_FILE_EXTENSIONS:
                        self._files.append(
                            self.TEXTSTATFILE.from_path(
                                os.path.join(root_path, file_name),
                                self
                            )
                        )
        return self._files

    def __dict__(self):
        return dict([ (file.f.name, dict(file)) for file in self.files ]
