""" Contains the Table class. """
import sys as _sys

from polyfills.stdlib.functions import sum
from polyfills.itertools import batched
from jycli.components import box
from jycli.console import Console
from jycli.components._renderables import Renderable

__all__ = ["Table"]


# On Jython 2.1, the `len()` function over a unicode string returns a wrong value:
# wsadmin>len("│") # expect: 1
# 3
# 
# This is solved by explicitly converting the string from UTF8 to unicode and then getting the length:
# wsadmin>len(unicode("│", "utf-8")) # expect: 1
# 1
#
# Source: https://stackoverflow.com/a/16476580/8965861
if _sys.version_info[0] < 3:
  text_type = unicode
  binary_type = str
  def b(x):
    return x
  def u(x):
    return unicode(x, "utf-8")
else:
  text_type = str
  binary_type = bytes
  import codecs
  def b(x):
    return codecs.latin_1_encode(x)[0]
  def u(x):
    return x


class Table(Renderable):
    """ A table that can be rendered in the console or as HTML. """
    def __init__(self, name, columns, box=box.SQUARE):
        """ Creates a new table.

        Args:
            name (str): The name of the table. Will be displayed before printing the table.
            columns (list[str]): The column names of the table. Must match the number of columns each row contains.

        Examples:
            ```pycon
            >>> table = Table("MyTable", ["Column1", "Column2"])
            >>> table
            MyTable (0 rows)
            ```
        """
        self.name = name
        self.columns = columns
        self.rows = []
        self.box = box

    def add_row(self, *args):
        """ Adds a row to the table.
        
        Args:
            *args (any): The values to add to the table.

        Raises:
            Exception: If the number of arguments does not match the number of columns defined.

        Examples:
            ```pycon
            >>> table = Table("MyTable", ["Column1", "Column2"])
            >>> table.add_row("Value1", "Value2")
            >>> table.add_row("Value3", "Value4")
            >>> table
            MyTable (2 rows)
            ```
        """
        if len(args) != len(self.columns):
            raise Exception("Invalid number of arguments (expected %d, found %d)" % (len(self.columns), len(args)))
        
        self.rows.append([ str(_val) for _val in args])

    def __console_print__(self, console):
        # type: (Console) -> str
        """Render the component to a console."""
        max_width = console.width

        # Fallback to ASCII if the terminal is dumb
        if (not console.is_terminal() or console.is_dumb_terminal()) and not self.box.ascii:
            self.box = box.ASCII

        # TODO: Remove variable duplication or use a custom parameter "adapt/equal size"
        if max_width is None:
            max_width = console.width

            # Calculate the maximum length for each column
            max_lengths = [ len(column) for column in self.columns ]
            for row in self.rows:
                for index in range(len(row)):
                    max_lengths[index] = max(max_lengths[index], len(str(row[index])))
        else:
            max_lengths = [ int(max_width / len(self.columns)) for _ in self.columns ]

        # ALWAYS recalculate each column's max length
        difference = (
            sum(max_lengths)
            + (len(u(" │ ")) * (len(self.columns) - 1))
            + (len(u("│ ")) + len(u(" │")))
            - max_width
        ) # type: ignore

        if difference > 0:
            # Try to reduce the length of the columns with the biggest length
            for _ in range(difference): # type: ignore
                max_lengths[max_lengths.index(max(max_lengths))] -= 1
        
        elif difference < 0:
            # Try to increase the length of the columns with the smallest length
            for _ in range(abs(difference)): # type: ignore
                max_lengths[max_lengths.index(min(max_lengths))] += 1

        
        # Render the table
        table = []

        # Table name
        table.append("" * max_width)
        table.append(self.name.center(max_width))
        table.append("%s%s%s" % (
            self.box.top_left,
            self.box.top_divider.join([
                self.box.top * (max_lengths[index] + 2)
                for index in range(len(self.columns))
            ]),
            self.box.top_right,
        ))

        # Header
        chunked_header = [
            [
                # 3. Align all lines to the left
                _chunked_string.ljust(max_lengths[index])
                
                # 2. Join the chunks with '\n', then split them again, so that 
                #    each chunk (as well as strings containing `\n`) is now a line.
                for _chunked_string in '\n'.join(
                    # 1. Split the row into chunks of the maximum length
                    batched(self.columns[index], max_lengths[index])
                ).splitlines()
            ]
            
            for index in range(len(self.columns))
        ]


        # Find the longest chunk (more lines in a single column) in the header
        header_longest_chunk = max([len(_chunked_string) for _chunked_string in chunked_header])

        # Fill the header with empty strings to match the longest chunk
        for index in range(len(chunked_header)):
            if len(chunked_header[index]) < header_longest_chunk:
                chunked_header[index].extend([" " * max_lengths[index]] * (header_longest_chunk - len(chunked_header[index])))
        
        table.append('\n'.join([
            "%s %s %s" % (
                self.box.head_left,
                (" " + self.box.head_vertical + " ").join(_row), # TODO: Do not hardcode spaces, check size
                self.box.head_right,
            )
            for _row in zip(*chunked_header)
        ]))

        # Header separator
        table.append("%s%s%s" % (
            self.box.head_row_left,
            self.box.head_row_cross.join([
                self.box.head_row_horizontal * (max_lengths[index] + 2)
                for index in range(len(self.columns))
            ]),
            self.box.head_row_right,
        ))

        # Rows
        for _row_index in range(len(self.rows)):
            row = self.rows[_row_index]

            chunked_row = [
                [
                    # 3. Align all lines to the left
                    _chunked_string.ljust(max_lengths[index])
                    
                    # 2. Join the chunks with '\n', then split them again, so that 
                    #    each chunk (as well as strings containing `\n`) is now a line.
                    for _chunked_string in '\n'.join(
                        # 1. Split the row into chunks of the maximum length
                        batched(row[index], max_lengths[index])
                    ).splitlines()
                ]
                
                for index in range(len(row))
            ]

            row_longest_chunk = max([len(_chunked_string) for _chunked_string in chunked_row])
            for index in range(len(chunked_row)):
                if len(chunked_row[index]) < row_longest_chunk:
                    chunked_row[index].extend([" " * max_lengths[index]] * (row_longest_chunk - len(chunked_row[index])))
            
            table.append('\n'.join([
                "%s %s %s" % (
                    self.box.mid_left,
                    (" " + self.box.mid_vertical + " ").join(_row),
                    self.box.mid_right,
                )
                for _row in zip(*chunked_row)
            ]))
            
            # Row separator (except for the last row)
            if _row_index < len(self.rows) - 1:
                table.append("%s %s %s" % (
                    self.box.row_left,
                    (" " + self.box.row_cross + " ").join([
                        self.box.row_horizontal * max_lengths[index]
                        for index in range(len(self.columns))
                    ]),
                    self.box.row_right,
                ))

        table.append("%s%s%s" % (
            self.box.bottom_left,
            self.box.bottom_divider.join([
                self.box.bottom * (max_lengths[index] + 2)
                for index in range(len(self.columns))
            ]),
            self.box.bottom_right,
        ))
        return "\n".join(table)
    
    def render(self, max_width=None):
        """ Renders the table as a string.

        Args:
            max_width (int, optional): The maximum width of the table. If `None`, it defaults to the terminal width.

        Returns:
            table (str): The string representation of the table.

        Examples:
            ```pycon
            >>> table = Table("MyTable", ["Column1", "Column2"])
            >>> table.add_row("Value1", "Value2")
            >>> table.add_row("Value3", "Value4")
            >>> print(table.render())
            ****************************************************************************************************
            *                                          MyTable                                                 *
            ****************************************************************************************************
            * Column1 | Column2                                                                                *
            * ------------------------------------------------------------------------------------------------ *
            * Value1  | Value2                                                                                 *
            * Value3  | Value4                                                                                 *
            ****************************************************************************************************
            ```
        """
        return self.__console_print__(console=Console(width=max_width))

    def to_html(self):
        """ Renders the table as HTML.
        
        Returns:
            html (str): The HTML representation of the table.
            
        Examples:
            ```pycon
            >>> table = Table("MyTable", ["Column1", "Column2"])
            >>> table.add_row("Value1", "Value2")
            >>> table.add_row("Value3", "Value4")
            >>> print(table.to_html())
            <table>
            <caption>MyTable</caption>
            <thead>
            <tr><th>Column1</th><th>Column2</th></tr>
            </thead>
            <tbody>
            <tr><td>Value1</td><td>Value2</td></tr>
            <tr><td>Value3</td><td>Value4</td></tr>
            </tbody>
            </table>
            ```
        """
        html = ['<table cellpadding="0" cellspacing="0" align="center" border="1">']

        # Table name
        html.append("<caption>%s</caption>" % self._html_escape_string(self.name))
        
        # Header
        html.append("<thead>")
        html.append("<tr>")
        for column in self.columns:
            html.append("<th>%s</th>" % self._html_escape_string(column))
        html.append("</tr>")
        html.append("</thead>")

        # Rows
        html.append("<tbody>")
        for row in self.rows:
            html.append("<tr>")
            for column in row:
                html.append("<td>%s</td>" % self._html_escape_string(column))
            html.append("</tr>")
        html.append("</tbody>")

        html.append("</table>")

        return "\n".join(html)
    
    def to_csv(self, delimiter=",", quotechar='"', lineterminator="\n"):
        """ Renders the table as CSV.
        
        TODO: Test this method.
        TODO: Add support for escaping the delimiter, quotechar and lineterminator characters.
        TODO: Improve quoting of values (currently only quotes values if they contain the delimiter, quotechar or lineterminator characters).

        Args:
            delimiter (str, optional): The delimiter to use between columns. Defaults to `","`.
            quotechar (str, optional): The quote character to use. Defaults to `"\""`.
            lineterminator (str, optional): The line terminator to use. Defaults to `"\n"`.

        Returns:
            csv (str): The CSV representation of the table.

        Examples:
            ```pycon
            >>> table = Table("MyTable", ["Column1", "Column2"])
            >>> table.add_row("Value1", "Value2")
            >>> table.add_row("Value3", "Value4")
            >>> print(table.to_csv())
            Column1,Column2
            Value1,Value2
            Value3,Value4
            ```
        """
        csv = []

        # Header
        csv.append(delimiter.join([
            str(
                (
                    str(_col).find(delimiter) != -1
                    or str(_col).find(quotechar) != -1
                    or str(_col).find(lineterminator) != -1
                )
                    and "%s%s%s" % (quotechar, str(_col))
                    or _col
            ) for _col in self.columns
        ]))

        # Rows
        for row in self.rows:
            csv.append(delimiter.join([
                str(
                    (
                        str(_column).find(delimiter) != -1
                        or str(_column).find(quotechar) != -1
                        or str(_column).find(lineterminator) != -1
                    )
                        and "%s%s%s" % (quotechar, str(_column))
                        or _column
                )
                for _column in row
            ]))
        
        return lineterminator.join(csv)

    def __str__(self):
        return "%s (%d rows)" % (self.name, len(self.rows))

    def __repr__(self):
        return "%s (%d rows)" % (self.name, len(self.rows))


if __name__ == "__main__":
    table = Table("MyTable", ["Column1\ntest", "Column2asdasdasdaasdasdasdasdsdasd", "Column3"], box=box.ASCII2)
    table.add_row("Value1aaaaaaaaaaaaaaaaaaaaaaaaaaaa", "Value2", "Value3")
    table.add_row("Value4", "Value5", "Value6")
    table.add_row("Value7", "Value8\nNew line", "Value9")
    print(table.render())
