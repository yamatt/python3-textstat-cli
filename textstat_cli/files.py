

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
        return dict((name, getattr(name, self)()) for name in self.cli.TESTS)
