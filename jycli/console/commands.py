import os as _os

try:
    import java as _java  # pyright: ignore[reportMissingImports]

    subprocess = None
except ImportError:
    import subprocess  # Used while testing on Windows


def execute_command(command):
    # type: (list[str]) -> str
    """Execute a command and return the output.

    Args:
        command (list[str]): The command that will be executed.

    Returns:
        output (str): The output of the command.

    Example:
        >>> execute_command(["echo", "Hello World!"])
        'Hello World!'
    """
    if subprocess is not None:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=True,
        ).stdout

    output = []

    builder = _java.lang.ProcessBuilder([str(word) for word in command])
    builder.redirectErrorStream(1)
    process = builder.start()
    reader = _java.io.BufferedReader(
        _java.io.InputStreamReader(process.getInputStream())
    )

    line = reader.readLine()
    while line != None:
        output.append(line)
        line = reader.readLine()
    reader, process, builder = None, None, None

    return "\n".join(output)


class TerminalSize:
    """Represents the size of the terminal. Can be accessed both as a tuple and as attributes."""

    def __init__(self, columns, lines):
        # type: (int, int) -> None
        """Initialize the TerminalSize object.

        Args:
            columns (int): The number of columns in the terminal.
            lines (int): The number of lines in the terminal.
        """
        self.columns = int(columns)
        self.lines = int(lines)

    def __getitem__(self, index):
        # type: (int) -> int
        return (self.columns, self.lines).__getitem__(index)

    def __str__(self):
        return "%s(columns=%s, lines=%s)" % (
            self.__class__.__name__,
            self.columns,
            self.lines,
        )

    def __repr__(self):
        return self.__str__()


def get_terminal_size():
    # type: () -> TerminalSize
    """Get the size of the terminal.
    
    Source: https://stackoverflow.com/a/6550596/8965861

    Returns:
        size (tuple[int, int]): The size of the terminal.

    Example:
        >>> get_terminal_size()
        (80, 24)
    """

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct

            cr = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))  # type: ignore
        except:
            return
        return cr

    # Shortcircuit for Windows
    try:
        _size = _os.get_terminal_size()
        return TerminalSize(
            columns=_size.columns, 
            lines=_size.lines
        )
    except:
        pass

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = _os.open(_os.ctermid(), _os.O_RDONLY)  # type: ignore
            cr = ioctl_GWINSZ(fd)
            _os.close(fd)
        except:
            pass

    if not cr:
        try:
            cr = (int(_os.environ["LINES"]), int(_os.environ["COLUMNS"]))
        except:
            pass

    if not cr:
        cr = tuple([
            execute_command(["bash", "-c", "tput %s 2> /dev/tty" % _cmd]).strip()
            for _cmd in ["lines", "cols"]
        ])

    # If all else fails, assume a default terminal size
    if not cr or None in cr or "" in cr:
        # cr = (24, 80) # Standard VT100 terminal screen size
        cr = (24, 132)  # Custom wide terminal screen size (for better visualization)

    return TerminalSize(
        lines=int(cr[0]),
        columns=int(cr[1]),
    )
