import os

from .textstat import TextStat
from .files import TextStatFile


class TextStatCli(object):
    """
    Wrapper for textstat
    """

    TEXTSTAT = TextStat
    TEXTSTATFILE = TextStatFile

    ACCEPTABLE_FILE_EXTENSIONS = ["txt", "md"]

    # methods in textstat for analysing text
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
    ]

    @classmethod
    def from_args(cls, args):
        """Initialises this class based on the results of argparse Namespace
        defined in __main__.create_args().

        :param args: :class:`argparse.Namespace` like object to populate this
            class
        """
        return cls(root_path=args.path, language=args.language)

    def __init__(self, root_path, language="en_US"):
        """
        :param root_path: The base path as a string to look for files to run the
            tests against.
        :param language: :class:`textstat.textstat` defined language string
        """
        self.root_path = root_path
        self.language = language

        self._textstat = None
        self._files = []

    @property
    def textstat(self):
        """Textstat singleton that is used throughought this library."""
        if not self._textstat:
            self._textstat = self.TEXTSTAT(language=self.language)
        return self._textstat

    @property
    def files(self):
        """A list of all the files to scan, based upon initial root path.
        Only lists files that have the right file extension.
        Wraps those files in to the TextStatFile object.
        """
        if not self._files:
            for root_path, _, file_names, _ in os.fwalk(self.root_path):
                for file_name in file_names:
                    # get the file extension, or the thing after the last dot
                    # in the file name, to see if it's on the approved list
                    extension = file_name.rsplit(".", maxsplit=1)[-1].lower()
                    if extension in self.ACCEPTABLE_FILE_EXTENSIONS:
                        self._files.append(
                            self.TEXTSTATFILE.from_path(
                                os.path.join(root_path, file_name), self
                            )
                        )
        return self._files

    def to_dict(self):
        """Get all the results as a python dictionary object. Useful for converting
        to JSON.
        """
        return dict([ (file.f.name, dict(file)) for file in self.files ])
