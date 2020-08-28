class TextStatFile(object):
    """
    An object that represents files on your system to run the tests against.
    """

    OPEN_MODE = "r"

    @classmethod
    def from_path(cls, file_path, cli):
        """
        Initialise this class when you don't have a file object, but do have
        the file path.
        """
        return cls(open(file_path, cls.OPEN_MODE), cli)

    def __init__(self, f, cli):
        """
        """
        self.f = f
        self.cli = cli

        self._text = None

    @property
    def text(self):
        """
        Get the contents of the file (memory inefficent)
        """
        if not self._text:
            self._text = self.f.read()
        return self._text

    def __getattr__(self, attr):
        """
        There are a lot of methods in textstat and they're likely to change.
        This is the lazy (i.e.: DRY) way of accessing those methods
        """
        if hasattr(self, attr):
            return getattr(self, attr)
        return getattr(self.cli.textstat, attr)

    def __dict__(self):
        """
        For all of the tests/methods available in textstat, run through them
        all and produce the results as a dictionary.
        """
        return dict((name, getattr(name, self)()) for name in self.cli.TESTS)
