from __future__ import nested_scopes

from polyfills.stdlib.future_types.bool import *  # type: ignore # ==> Import the polyfills for boolean types
from jycli.console import Console
from jycli.components._renderables import Renderable
from jycli.style import parse as parse_style
from jycli.components import box


class Panel(Renderable):
    """A panel is a container for other widgets. It can have a title and a subtitle.

    Jython adaptation of https://rich.readthedocs.io/en/stable/reference/panel.html#rich.panel.Panel
    """
    def __init__(
        self,
        renderable,
        title=None,
        subtitle=None,
        expand=True,
        style="",
        border_style="",
        width=None, # type: int|None
        height=None, # type: int|None
        box=box.SQUARE,
    ):
        self.renderable = renderable
        self.title = title
        self.subtitle = subtitle
        self.expand = expand
        self.style = parse_style(style)
        self.border_style = parse_style(border_style)
        self.box = box

        self.width = None
        if width is not None and str(width).isdigit():
            self.width = int(width)
        
        self.height = None
        if height is not None and str(height).isdigit():
            self.height = int(height)

    def __console_print__(self, console):
        # type: (Console) -> str
        """Render the panel to a console."""
        console_width = self.width
        if console_width is None:
            console_width = console.width

        # Fallback to ASCII if the terminal is dumb
        if (not console.is_terminal() or console.is_dumb_terminal()) and not self.box.ascii:
            self.box = box.ASCII

        output = []
        padding_size = 2
        border_width = int(console_width - 2)

        # Title
        header_content = self.box.top * (console_width - 2) # Default to a line of dashes
        if self.title is not None:
            border_width = int(
                (
                    console_width
                    - len(self.title)      # Exclude the title
                    - (padding_size * 2)   #    "     "  padding
                    - 2                    #    "     "  border characters
                ) / 2
            )
            
            # If the title is an odd number of characters, add an 
            # extra border character to the left side
            extra_border_width = 0
            if len(self.title) % 2:
                extra_border_width = 1

            header_content = "".join([
                (self.box.top * (border_width + extra_border_width)),
                (" " * padding_size),
                (self.title),
                (" " * padding_size),
                (self.box.top * border_width),
            ])

        output.append(
            "%s%s%s%s%s"
            % (
                self.border_style,
                self.box.top_left,
                header_content,
                self.box.top_right,
                parse_style("reset"),
            )
        )
        
        # Body
        output.append(
            "\n".join(
                [
                    (
                        "%s%s%s %s %s%s%s"
                        % (
                            self.border_style,
                            self.box.mid_left,
                            parse_style("reset"),
                            _line.ljust(console_width - 4),
                            self.border_style,
                            self.box.mid_right,
                            parse_style("reset"),
                        )
                    )
                    for _line in self.renderable.splitlines()
                ]
            )
        )

        # Footer
        output.append(
            "%s%s%s%s%s"
            % (
                self.border_style,
                self.box.bottom_left,
                self.box.bottom * (console_width - 2),
                self.box.bottom_right,
                parse_style("reset"),
            )
        )

        return "\n".join(output)
    
    def __repr__(self):
        return "<%s width=%s>" % (self.__class__.__name__, self.width)


if __name__ == "__main__":  # pragma: no cover
    c = Console()

    # from .box import DOUBLE, ROUNDED
    # from .padding import Padding

    p0 = Panel(
        "Hello, World!",
    )
    p1 = Panel(
        "Hello, World!",
        title="Test panel",
        border_style="green",
        style="white on blue",
        box=box.DOUBLE,
        # padding=1,
    )
    p2 = Panel(
        "Hello, World!",
        title="TEST2",
        border_style="red",
        box=box.DOUBLE,
        # padding=1,
    )
    p3 = Panel(
        "Hello, World!",
        # title="TEST2",
        # style="white on blue",
        # box=DOUBLE,
        # padding=1,
        border_style="blue on yellow",
        width=50,
    )

    c.print()
    c.print(p0)

    c.print()
    c.print(p1)

    c.print()
    c.print(p2)

    c.print()
    c.print(p3)

    print(repr(p1), repr(p2), repr(p3))
