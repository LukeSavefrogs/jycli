from __future__ import nested_scopes

import sys as _sys
import math as _math

from polyfills.stdlib.future_types.bool import *  # type: ignore # ==> Import the polyfills for boolean types
from jycli.console import Console
from jycli._renderables import Renderable
from jycli.style import parse as parse_style

if _sys.version_info[0] < 3:
  text_type = unicode # type: ignore
  binary_type = str
  def b(x):
    return x
  def u(x):
    return unicode(x, "utf-8")
else:
  text_type = str
  binary_type = bytes # type: ignore
  import codecs
  def b(x):
    return codecs.latin_1_encode(x)[0]
  def u(x):
    return x


class Rule(Renderable):
    """ A horizontal rule is a line that separates content. It can have a title.

    Jython adaptation of https://rich.readthedocs.io/en/stable/reference/rule.html#rich.rule.Rule
    """
    def __init__(
        self,
        title=None,
        characters="─",
        style="",
        width=None, # type: int|None
    ):
        self._console = Console()
        self.title = title
        self.characters = characters
        self.style = parse_style(style)

        self.width = None
        if width is not None and str(width).isdigit():
            self.width = int(width)

    def __console_print__(self, console):
        # type: (Console) -> str
        """Render the Rule component to a console."""
        console_width = self.width
        if console_width is None:
            console_width = console.width

        output = []
        padding_size = 2
        border_width = int(_math.floor(int(console_width) / len(u(self.characters))))

        # Title
        header_content = (self.characters * border_width)
        if self.title is not None:
            border_width = int(
                (
                    _math.floor(int(console_width) / len(u(self.characters)))
                    - len(self.title)      # Exclude the title
                    - (padding_size * 2)   #    "     "  padding
                ) / 2              
            )
            
            header_content = "%s%s%s%s%s" % (
                (self.characters * border_width),
                (" " * padding_size),
                self.title,
                (" " * padding_size),
                (self.characters * border_width),
            )

            # if len(self.title) % 2:
            #    header_content += self.characters[0]
                
    
        # Header
        output.append("%s%s%s" % (
            self.style,
            header_content,
            parse_style("reset"),
        ))

        return "\n".join(output)

    def to_html(self):
        """ Render the rule to HTML. 
        
        TODO: Add color support
        
        Source: https://stackoverflow.com/a/12522330/8965861
        """
        html = """
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <td><hr /></td>
            </table>
        """

        if self.title is not None:
            html = """
                <table width="100%%" border="0" cellspacing="0" cellpadding="0">
                    <td><hr /></td>
                    <td width="1px" style="padding: 0 10px; white-space: nowrap;">%s</td>
                    <td><hr /></td>
                </table>
            """ % self.title

        return html

    def __str__(self):
        return self._render()
        

if __name__ == "__main__":  # pragma: no cover
    c = Console()
    c.print(Rule(
        title="Horizontal rule",
        # characters="-~=",
        # width=141,
        style="red on white",
    ))

    c.print(Rule(
        # title="Horizontal rule",
        # characters="-~=",
        # width=141,
        # style="green",
    ).to_html())