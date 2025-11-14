""" Base module for all renderable elements. """
import sys as _sys
from xml.sax.saxutils import escape

class Renderable:
    """ Base class for all renderable elements. """
    def __console_print__(self, console):
        raise NotImplementedError("The '%s' method must be defined when subclassing the 'Renderable' class." % _sys._getframe().f_code.co_name)
    
    def __str__(self):
        from jycli.console import Console
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
    
    def _csv_escape_string(self, string):
        # type: (str) -> str
        """ Escape the provided string and make it safe to be inserted as CSV. 
        
        Also, replace some special characters with spaces.
        
        Args:
            string(str): The string that needs to be processed.
        
        Returns:
            str: The escaped string
        """
        return (
            string.replace('"', '""')   # Escape double quotes (RFC4180 https://datatracker.ietf.org/doc/html/rfc4180#section-2)
        )