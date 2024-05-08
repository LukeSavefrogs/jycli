""" Complete ripoff of Rich's beautiful Box styles.

See https://github.com/Textualize/rich/blob/master/rich/box.py.
"""

from polyfills.stdlib.future_types.bool import *  # type: ignore # ==> Import the polyfills for boolean types


class Box:
    """Defines characters to render boxes.

    ┌─┬┐ top
    │ ││ head
    ├─┼┤ head_row
    │ ││ mid
    ├─┼┤ row
    ├─┼┤ foot_row
    │ ││ foot
    └─┴┘ bottom

    Args:
        box (str): Characters making up box.
        ascii (bool, optional): True if this box uses ascii characters only. Default is False.
    """

    def __init__(self, box, ascii=False):
        self._box = box
        self.ascii = ascii

        # top
        self.top_left, self.top, self.top_divider, self.top_right = box["top"]

        # head
        self.head_left, _, self.head_vertical, self.head_right = box["head"]

        # head_row
        (
            self.head_row_left,
            self.head_row_horizontal,
            self.head_row_cross,
            self.head_row_right,
        ) = list(box["head_row"])

        # mid
        self.mid_left, _, self.mid_vertical, self.mid_right = box["mid"]

        # row
        self.row_left, self.row_horizontal, self.row_cross, self.row_right = box["row"]

        # foot_row
        (
            self.foot_row_left,
            self.foot_row_horizontal,
            self.foot_row_cross,
            self.foot_row_right,
        ) = box["foot_row"]

        # foot
        self.foot_left, _, self.foot_vertical, self.foot_right = box["foot"]

        # bottom
        self.bottom_left, self.bottom, self.bottom_divider, self.bottom_right = box["bottom"]

    def __repr__(self):
        return "Box(...)"

    def __str__(self):
        return self._box


# fmt: off
ASCII = Box({
    "top":      ["+","-","-","+"],
    "head":     ["|"," ","|","|"],
    "head_row": ["|","-","+","|"],
    "mid":      ["|"," ","|","|"],
    "row":      ["|","-","+","|"],
    "foot_row": ["|","-","+","|"],
    "foot":     ["|"," ","|","|"],
    "bottom":   ["+","-","-","+"],
    },
    ascii=True,
)

ASCII2 = Box({
    "top":      ["+","-","+","+"],
    "head":     ["|"," ","|","|"],
    "head_row": ["+","-","+","+"],
    "mid":      ["|"," ","|","|"],
    "row":      ["+","-","+","+"],
    "foot_row": ["+","-","+","+"],
    "foot":     ["|"," ","|","|"],
    "bottom":   ["+","-","+","+"],
    },
    ascii=True,
)

ASCII_DOUBLE_HEAD = Box({
    "top":      ["+","-","+","+"],
    "head":     ["|"," ","|","|"],
    "head_row": ["+","=","+","+"],
    "mid":      ["|"," ","|","|"],
    "row":      ["+","-","+","+"],
    "foot_row": ["+","-","+","+"],
    "foot":     ["|"," ","|","|"],
    "bottom":   ["+","-","+","+"],
    },
    ascii=True,
)

SQUARE = Box({
    "top":      ["┌","─","┬","┐"],
    "head":     ["│"," ","│","│"],
    "head_row": ["├","─","┼","┤"],
    "mid":      ["│"," ","│","│"],
    "row":      ["├","─","┼","┤"],
    "foot_row": ["├","─","┼","┤"],
    "foot":     ["│"," ","│","│"],
    "bottom":   ["└","─","┴","┘"],
})

SQUARE_DOUBLE_HEAD = Box({
    "top":      ["┌","─","┬","┐"],
    "head":     ["│"," ","│","│"],
    "head_row": ["╞","═","╪","╡"],
    "mid":      ["│"," ","│","│"],
    "row":      ["├","─","┼","┤"],
    "foot_row": ["├","─","┼","┤"],
    "foot":     ["│"," ","│","│"],
    "bottom":   ["└","─","┴","┘"],
})

MINIMAL = Box({
    "top":      [" "," ","╷"," "],
    "head":     [" "," ","│"," "],
    "head_row": ["╶","─","┼","╴"],
    "mid":      [" "," ","│"," "],
    "row":      ["╶","─","┼","╴"],
    "foot_row": ["╶","─","┼","╴"],
    "foot":     [" "," ","│"," "],
    "bottom":   [" "," ","╵"," "],
})


MINIMAL_HEAVY_HEAD = Box({
    "top":      [" "," ","╷"," "],
    "head":     [" "," ","│"," "],
    "head_row": ["╺","━","┿","╸"],
    "mid":      [" "," ","│"," "],
    "row":      ["╶","─","┼","╴"],
    "foot_row": ["╶","─","┼","╴"],
    "foot":     [" "," ","│"," "],
    "bottom":   [" "," ","╵"," "],
})

MINIMAL_DOUBLE_HEAD = Box({
    "top":      [" "," ","╷"," "],
    "head":     [" "," ","│"," "],
    "head_row": [" ","═","╪"," "],
    "mid":      [" "," ","│"," "],
    "row":      [" ","─","┼"," "],
    "foot_row": [" ","─","┼"," "],
    "foot":     [" "," ","│"," "],
    "bottom":   [" "," ","╵"," "],
})


SIMPLE = Box({
    "top":      [" "," "," "," "],
    "head":     [" "," "," "," "],
    "head_row": [" ","─","─"," "],
    "mid":      [" "," "," "," "],
    "row":      [" "," "," "," "],
    "foot_row": [" ","─","─"," "],
    "foot":     [" "," "," "," "],
    "bottom":   [" "," "," "," "],
})

SIMPLE_HEAD = Box({
    "top":      [" "," "," "," "],
    "head":     [" "," "," "," "],
    "head_row": [" ","─","─"," "],
    "mid":      [" "," "," "," "],
    "row":      [" "," "," "," "],
    "foot_row": [" "," "," "," "],
    "foot":     [" "," "," "," "],
    "bottom":   [" "," "," "," "],
})


SIMPLE_HEAVY = Box({
    "top":      [" "," "," "," "],
    "head":     [" "," "," "," "],
    "head_row": [" ","━","━"," "],
    "mid":      [" "," "," "," "],
    "row":      [" "," "," "," "],
    "foot_row": [" ","━","━"," "],
    "foot":     [" "," "," "," "],
    "bottom":   [" "," "," "," "],
})


HORIZONTALS = Box({
    "top":      [" ","─","─"," "],
    "head":     [" "," "," "," "],
    "head_row": [" ","─","─"," "],
    "mid":      [" "," "," "," "],
    "row":      [" ","─","─"," "],
    "foot_row": [" ","─","─"," "],
    "foot":     [" "," "," "," "],
    "bottom":   [" ","─","─"," "],
})

ROUNDED = Box({
    "top":      ["╭","─","┬","╮"],
    "head":     ["│"," ","│","│"],
    "head_row": ["├","─","┼","┤"],
    "mid":      ["│"," ","│","│"],
    "row":      ["├","─","┼","┤"],
    "foot_row": ["├","─","┼","┤"],
    "foot":     ["│"," ","│","│"],
    "bottom":   ["╰","─","┴","╯"],
})

HEAVY = Box({
    "top":      ["┏","━","┳","┓"],
    "head":     ["┃"," ","┃","┃"],
    "head_row": ["┣","━","╋","┫"],
    "mid":      ["┃"," ","┃","┃"],
    "row":      ["┣","━","╋","┫"],
    "foot_row": ["┣","━","╋","┫"],
    "foot":     ["┃"," ","┃","┃"],
    "bottom":   ["┗","━","┻","┛"],
})

HEAVY_EDGE = Box({
    "top":      ["┏","━","┯","┓"],
    "head":     ["┃"," ","│","┃"],
    "head_row": ["┠","─","┼","┨"],
    "mid":      ["┃"," ","│","┃"],
    "row":      ["┠","─","┼","┨"],
    "foot_row": ["┠","─","┼","┨"],
    "foot":     ["┃"," ","│","┃"],
    "bottom":   ["┗","━","┷","┛"],
})

HEAVY_HEAD = Box({
    "top":      ["┏","━","┳","┓"],
    "head":     ["┃"," ","┃","┃"],
    "head_row": ["┡","━","╇","┩"],
    "mid":      ["│"," ","│","│"],
    "row":      ["├","─","┼","┤"],
    "foot_row": ["├","─","┼","┤"],
    "foot":     ["│"," ","│","│"],
    "bottom":   ["└","─","┴","┘"],
})

DOUBLE = Box({
    "top":      ["╔","═","╦","╗"],
    "head":     ["║"," ","║","║"],
    "head_row": ["╠","═","╬","╣"],
    "mid":      ["║"," ","║","║"],
    "row":      ["╠","═","╬","╣"],
    "foot_row": ["╠","═","╬","╣"],
    "foot":     ["║"," ","║","║"],
    "bottom":   ["╚","═","╩","╝"],
})

DOUBLE_EDGE = Box({
    "top":      ["╔","═","╤","╗"],
    "head":     ["║"," ","│","║"],
    "head_row": ["╟","─","┼","╢"],
    "mid":      ["║"," ","│","║"],
    "row":      ["╟","─","┼","╢"],
    "foot_row": ["╟","─","┼","╢"],
    "foot":     ["║"," ","│","║"],
    "bottom":   ["╚","═","╧","╝"],
})

MARKDOWN = Box({
    "top":      [" "," "," "," "],
    "head":     ["|"," ","|","|"],
    "head_row": ["|","-","|","|"],
    "mid":      ["|"," ","|","|"],
    "row":      ["|","-","|","|"],
    "foot_row": ["|","-","|","|"],
    "foot":     ["|"," ","|","|"],
    "bottom":   [" "," "," "," "],
    },
    ascii=True,
)
# fmt: on
