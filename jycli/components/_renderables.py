""" Base module for all renderable elements. """
import sys as _sys
from xml.sax.saxutils import escape

from jycli.console import Console

class Renderable:
    """ Base class for all renderable elements. """
    def __console_print__(self, console):
        # type: (Console) -> str
        raise NotImplementedError("The '%s' method must be defined when subclassing the 'Renderable' class." % _sys._getframe().f_code.co_name)
    
    def __str__(self):
        return self.__console_print__(
            console=Console(),
        )
    
    def _html_escape_string(self, string):
        # type: (str) -> str
        """ Escape the provided string and make it safe to be inserted as HTML. 
        
        Also, replace some special characters with the corresponding HTML element.
        
        Args:
            string(str): The string that needs to be processed.

        Returns:
            str: The escaped string
        """
        return (
            escape(string)              # Escape HTML entities
                .replace("\r", "")      # Remove carriage returns
                .replace("\n", "<br>")
        )