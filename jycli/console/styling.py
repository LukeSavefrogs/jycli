import os as _os
import sys as _sys

class _ANSIColors:
    """ ANSI escape sequences for colors. """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"

    RESET_FG = "\033[39m"
    RESET_BG = "\033[49m"
    
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINKING = "\033[5m"
    REVERSE = "\033[7m"
    INVISIBLE = "\033[8m"
    STRIKETHROUGH = "\033[9m"

    def __init__(self):
        # type: () -> None
        """ Initialize ANSI escape codes. """
        # Copy attributes for all ANSI escape codes into the child class.
        for key, value in vars(self.__class__).items():
            if key.startswith("_") or callable(value):
                continue

            setattr(self, key, value)

        # Disable colors if the NO_COLOR environment variable is set (https://no-color.org/).
        no_color_var = _os.environ.get('NO_COLOR', None)
        if no_color_var is not None and no_color_var != "":
            self.disable()

        # Disable colors if the output is not a TTY (https://stackoverflow.com/a/64523765/8965861).
        if not hasattr(_sys, 'ps1'):
            self.disable()
    
    def enable(self):
        # type: () -> None
        """ Enable ANSI escape codes. """
        for key in vars(self).keys():
            if callable(getattr(self.__class__, key)):
                continue
            setattr(self, key, getattr(self.__class__, key))
    
    def disable(self):
        # type: () -> None
        """ Disable ANSI escape codes. """
        for key in vars(self).keys():
            if callable(getattr(self.__class__, key)):
                continue
            setattr(self, key, "")
    
    def get(self, color_name):
        # type: (str) -> str
        """ Get the ANSI escape code for a color. """
        return getattr(self, color_name.upper(), "")

ANSIColors = _ANSIColors()
""" ANSI escape sequences for colors. """
