import re as _re
import unittest as _unittest

STYLES = {
    "effects": {
        "reset": "0",
        "bold": "1",
        "dim": "2",
        "italic": "3",
        "underline": "4",
        "blinking": "5",
        "reverse": "7",
        "invisible": "8",
        "strikethrough": "9",

        # Common aliases
        "dimmed": "2",
        "underlined": "4",
        "invert": "7",
        "inverted": "7",
        "hidden": "8",
    },
    "foreground": {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "reset": "39",
        
        # Bright colors
        "black:bright": "90",
        "red:bright": "91",
        "green:bright": "92",
        "yellow:bright": "93",
        "blue:bright": "94",
        "magenta:bright": "95",
        "cyan:bright": "96",
        "white:bright": "97",
        "reset:bright": "99",
    },
    "background": {
        "black": "40",
        "red": "41",
        "green": "42",
        "yellow": "43",
        "blue": "44",
        "magenta": "45",
        "cyan": "46",
        "white": "47",
        "reset": "49",

        # Bright colors
        "black:bright": "100",
        "red:bright": "101",
        "green:bright": "102",
        "yellow:bright": "103",
        "blue:bright": "104",
        "magenta:bright": "105",
        "cyan:bright": "106",
        "white:bright": "107",
        "reset:bright": "109",
    },
}


class Style:
    def __init__(self, effect=None, foreground=None, background=None):
        # type: (str|int|None, str|int|None, str|int|None) -> None
        self.effect = effect
        self.foreground = foreground
        self.background = background

        if effect is not None and type(effect) == type(""):
            self.effect = STYLES["effects"].get(str(effect), None)
            if self.effect is None:
                raise ValueError("Invalid effect: %s" % effect)
            
        if foreground is not None and type(foreground) == type(""):
            self.foreground = STYLES["foreground"].get(str(foreground), None)
            if self.foreground is None:
                raise ValueError("Invalid foreground color: %s" % foreground)

        if background is not None and type(background) == type(""):
            self.background = STYLES["background"].get(str(background), None)
            if self.background is None:
                raise ValueError("Invalid background color: %s" % background)

    def __add__(self, other):
        if type(other) == type(""):
            return str(self) + other
        
        if type(other) != type(self):
            raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (
                self.__class__.__name__, 
                type(other),
            ))
    
        final_style = Style()
        for attr in ["foreground", "background", "effect"]:
            if getattr(other, attr) is not None:
                setattr(final_style, attr, getattr(other, attr))
            elif getattr(self, attr) is not None:
                setattr(final_style, attr, getattr(self, attr))

        return final_style
    
    def __radd__(self, other):
        if type(other) == type(""):
            return other + str(self)
        
        # Only if the method is not implemented on the left operand,
        # Python attempts to call `__radd__` on the right operand
        raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (
            type(other),
            self.__class__.__name__, 
        ))
    
    def __sub__(self, other):
        raise NotImplementedError("Subtraction is not supported for %s objects." % self.__class__.__name__)

    def __str__(self):
        if (
            self.effect is None
            and self.foreground is None
            and self.background is None
        ):
            return ""
        
        return "\033[%sm" % ';'.join([
            _style
            for _style in (self.effect, self.foreground, self.background)
            if _style is not None
        ])
    
    def __repr__(self):
        _effect, _foreground, _background = (None,) * 3
        _repr_attrs = []

        if self.effect is not None:
            _effect = ''.join([ key for key in STYLES["effects"].keys() if STYLES["effects"][key] == self.effect ])
            _repr_attrs.append("effect=%s" % _effect)
        if self.foreground is not None:
            _foreground = ''.join([ key for key in STYLES["foreground"].keys() if STYLES["foreground"][key] == self.foreground ])
            _repr_attrs.append("foreground=%s" % _foreground)
        if self.background is not None:
            _background = ''.join([ key for key in STYLES["background"].keys() if STYLES["background"][key] == self.background ])
            _repr_attrs.append("background=%s" % _background)
        
        return "Style(%s)" % (', '.join(_repr_attrs))
    
    def __eq__(self, other):
        if type(other) != type(self):
            return 1 == 0
        
        for attr in ["effect", "foreground", "background"]:
            if getattr(self, attr) != getattr(other, attr):
                return 1 == 0
        
        return 1 == 1
        
    def escaped_str(self):
        # type: () -> str
        """ Get the ANSI escape code for the style. """
        return str(self).replace("\033", "\\033")

def parse(text):
    # type: (str) -> Style
    """ Parse a string for ANSI escape codes. 
    
    Example:
        ```
        >>> parse("bold")
        "\033[1m"
        >>> parse("yellow")
        "\033[33m"
        >>> parse("on red")
        "\033[41m"
        >>> parse("green on red")
        "\033[32;41m"
        >>> parse("bold white on red")
        "\033[1;37;41m"
        ```
    """
    text = text.strip()
    style_regex = "^((%s) ?){0,2}(on (%s))?$" % (
        "|".join(list(STYLES["effects"].keys()) + list(STYLES["foreground"].keys())),
        "|".join(STYLES["background"].keys()),
    )

    if not _re.match(style_regex, text):
        raise ValueError("Invalid color format: %s" % text)
    
    # Split the text into tokens.
    tokens = [s.strip() for s in text.split("on")]
    if len(tokens) > 2:
        raise ValueError("Invalid color format: %s" % text)
    
    elif len(tokens) == 1:
        tokens.append("") # Only the foreground color is set.
    
    # Split the foreground color into multiple tokens.
    fg_tokens = [s.strip() for s in tokens[0].split(" ")]
    if len(fg_tokens) > 2:
        raise ValueError("Invalid color format: %s" % text)
    
    # Parse the foreground color.
    fg_style = Style()
    if len(fg_tokens) == 1 and fg_tokens[0].strip() != "":
        # If there is only one token, it is either a foreground color or an effect.
        # We need then to look up the token in the effects and foreground colors.
        _effect = STYLES["effects"].get(fg_tokens[0], None)
        _foreground = STYLES["foreground"].get(fg_tokens[0], None)

        if _effect is not None:
            fg_style = Style(effect=fg_tokens[0])
        elif _foreground is not None:
            fg_style = Style(foreground=fg_tokens[0])
        else:
            raise ValueError("Invalid effect or foreground color: %s" % fg_tokens[0])
    elif len(fg_tokens) == 2:
        fg_style = Style(
            effect=fg_tokens[0],
            foreground=fg_tokens[1],
        )

    # Parse the background color.
    bg_style = Style()
    if tokens[1] != "":
        bg_style = Style(background=tokens[1])

    return fg_style + bg_style


class ParserTestCase(_unittest.TestCase):
    def test_style_name(self):
        # Invalid color errors.
        self.assertRaises(ValueError, parse, "CustomColor")
        self.assertRaises(ValueError, parse, "CustomColor on CustomColor")
        self.assertRaises(ValueError, parse, "CustomColor on red")
        
    def test_style_format(self):
        # Invalid formats.
        self.assertRaises(ValueError, parse, "string on string on string")
        self.assertRaises(ValueError, parse, "string string string on string")
        self.assertRaises(ValueError, parse, "string string string")
        self.assertRaises(ValueError, parse, "on string string")

        # Valid formats.
        parse("bold")
        parse("italic red")
        parse("on blue")
        
        parse("yellow on green")
        parse("blinking white on black")

    def test_parse(self):
        self.assertEqual(
            parse("red"),
            Style(foreground="red"),
        )
        self.assertEqual(
            parse("bold red"),
            Style(effect="bold", foreground="red"),
        )
        self.assertEqual(
            parse("on yellow"),
            Style(background="yellow"),
        )
        self.assertEqual(
            parse("green on red"),
            Style(foreground="green", background="red"),
        )
        self.assertEqual(
            parse("italic green on red"),
            Style(effect="italic", foreground="green", background="red"),
        )

    def test_escaped_string(self):
        self.assertEqual(
            parse("bold").escaped_str(),
            r"\033[1m",
        )
        self.assertEqual(
            parse("yellow").escaped_str(),
            r"\033[33m",
        )
        self.assertEqual(
            parse("on red").escaped_str(),
            r"\033[41m",
        )
        self.assertEqual(
            parse("green on red").escaped_str(),
            r"\033[32;41m",
        )
        self.assertEqual(
            parse("bold white on red").escaped_str(),
            r"\033[1;37;41m",
        )


if __name__ == "__main__":
    _unittest.main()