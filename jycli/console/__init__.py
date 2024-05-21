""" Provides a wrapper around the console and allows interacting with it. """

import sys as _sys
import os as _os

# Add the parent directory to the path so we can import the styling module.
# _sys.path.append("./")

import jycli.console.commands as commands

from jycli.console.styling import ANSIColors
from jycli.style import Style, parse as parse_style # pyright: ignore[reportUnusedImport]

from polyfills.stdlib.functions import enumerate
from polyfills.stdlib.future_types.bool import *  # type: ignore # ==> Import the polyfills for boolean types

try:
    import java.lang.System as JavaSystem # pyright: ignore[reportMissingImports]
except ImportError:
    JavaSystem = None

try:
    apply # pyright: ignore[reportUndefinedVariable]
except NameError:
    def apply(func, args, kwargs):
        return eval("func(*args, **kwargs)")

class Console:
    """ Represents the console. 
    
    Exposes methods useful to interact directly with the console.
    """
    def __init__(self, file=_sys.stdout, force_terminal=None, width=None, height=None):
        """ Initialize the console.
        
        Args:
            file (typing.TextIO): The file to write to. Defaults to `sys.stdout`.
            force_terminal (typing.Optional[bool]): Force the console to be a terminal.
            width (int, optional): The width of the terminal. Leave as default to auto-detect width.
            height (int, optional): The height of the terminal. Leave as default to auto-detect height.
        """
        self.file = file
        self._force_terminal = force_terminal

        self._width = None
        if width is not None and str(width).isdigit():
            self._width = int(width)
        
        self._height = None
        if height is not None and str(height).isdigit():
            self._height = int(height)

    def _tput_exec(self, command):
        # type: (str) -> str
        """ Execute a `tput` command via the shell.
        
        Args:
            command (str): The `tput` command to execute.
        """
        return commands.execute_command(["bash", "-c", "tput %s" % command])
    
    def get_terminal_size(self):
        # type: () -> commands.TerminalSize
        """ Get the size of the terminal.

        Returns:
            size (commands.TerminalSize): The size of the terminal. (width, height)

        Example:
            >>> get_terminal_size()
            (80, 24)
        """
        size = commands.get_terminal_size()
        
        if self._width is not None:
            size.columns = self._width
        
        if self._height is not None:
            size.lines = self._height
        
        return size
    
    def clear(self):
        """ Clear the screen.
        
        This is a wrapper around `tput clear`.
        """
        print(self._tput_exec("clear"))

    def move_cursor(self, x, y):
        # type: (int, int) -> None
        """ Move the cursor to the specified position.
        
        This is a wrapper around `tput cup`.

        Args:
            x (int): The x position to move the cursor to.
            y (int): The y position to move the cursor to.
        """
        print(self._tput_exec("cup %s %s" % (x, y)))
    
    def is_terminal(self):
        """Check if the console is writing to a terminal.

        Returns:
            bool: True if the console writing to a device capable of
            understanding terminal codes, otherwise False.
        """
        if self._force_terminal is not None:
            return self._force_terminal

        # If FORCE_COLOR env var has any value at all, we assume a terminal.
        force_color = _os.environ.get("FORCE_COLOR")
        if force_color is not None:
            self._force_terminal = True
            return True

        if JavaSystem is not None and JavaSystem.console() is not None:
            return True

        isatty = getattr(self.file, "isatty", None)
        if isatty is None:
            return False
        
        try:
            return isatty()
        except ValueError:
            # in some situation (at the end of a pytest run for example) isatty() can raise
            # ValueError: I/O operation on closed file
            # return False because we aren't in a terminal anymore
            return False

    def is_dumb_terminal(self):
        """Detect dumb terminal.

        Returns:
            bool: True if writing to a dumb terminal, otherwise False.
        """
        _term = _os.environ.get("TERM", "")
        is_dumb = _term.lower() in ("dumb", "unknown")
        return self.is_terminal() and is_dumb
    
    def out(self, *args, **kwargs):
        """ Output to the terminal. 
        
        This is a low-level way of writing to the terminal which unlike print() 
        won’t pretty print, wrap text, or apply markup, but will optionally 
        apply a basic style.

        Args:
            *args: The objects to be printed
            file (typing.TextIO): The file to write to. Defaults to `sys.stdout`.
            sep (str, optional): Separator between objects. Defaults to " ".
            end (str, optional): End of the print. Defaults to "\n".
        """
        file = kwargs.get("file", None)
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        style = kwargs.get("style", None)
        
        if file is None:
            file = self.file

        if style is None:
            style = Style()
        elif not isinstance(style, Style):
            style = parse_style(style)
        style_reset = style.get_reset_style()

        file.write(''.join([
            style.__console_print__(self),
            sep.join([str(arg) for arg in args]),
            style_reset.__console_print__(self),
            end,
        ]))
        
    def print(self, *args, **kwargs):
        """ Print the console to the specified file.

        Args:
            *args: The objects to be printed
            file (typing.TextIO): The file to write to. Defaults to `sys.stdout`.
            sep (str, optional): Separator between objects. Defaults to " ".
            end (str, optional): End of the print. Defaults to "\n".
        """
        renderables = list(args)
        for index, arg in enumerate(renderables):
            if hasattr(arg, "__console_print__") and callable(getattr(arg, "__console_print__")):
                renderables[index] = str(arg.__console_print__(self))

        # Old way of unpacking sequences
        apply(self.out, renderables, kwargs) # pyright: ignore[reportUndefinedVariable]
    
    def __getattr__(self, name):
        """`__getattr__` gets called every time an undefined attribute is accessed.

        We use this to implement dynamic properties.

        Args:
            name (str): The name of the attribute to get.
        """
        if name in ['columns', 'width']:
            return self.get_terminal_size().columns
        elif name in ['lines', 'height']:
            return self.get_terminal_size().lines
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

if __name__ == "__main__":
    console = Console()
    console.clear()
    console.move_cursor(0, 0)
    console.print("Hello, World!")
    console.print("Hello, World!", style="bold red")
    console.print("Terminal size: %s" % console.get_terminal_size())