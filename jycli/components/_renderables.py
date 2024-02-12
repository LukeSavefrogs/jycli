""" Base module for all renderable elements. """
import sys as _sys

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