""" The `application` module contains the `Application` class, which is the
base class for all CLI applications.

Usage:
    >>> class MyApplication(Application):
    ...     def main(self):
    ...         print("Hello World!")
    ...         return True
    ...
    ...     def on_success(self, context):
    ...         print("Success!")
    ...
    ...     def on_failure(self, context):
    ...         print("Failure!")
    ... 
    >>> app = MyApplication()
    >>> app.run()
    --------------------------------------------------------------------------------
    
    Hello World!
    
    --------------------------------------------------------------------------------
    Success!
"""
# TODO: Aggiungere possibilità di logging direttamente dall'applicazione con scelta se usare il modulo logging o lo script logger di opac
# TODO: Aggiungere scelta inoltre se copiare il file di log alla fine della procedura o scriverci nel frattempo
from __future__ import nested_scopes
import sys as _sys
import time as _time
import traceback
from jycli.components.rule import Rule

from polyfills.stdlib.future_types.bool import * # type: ignore # ==> Import the polyfills for boolean types

from jycli.console import Console
from jycli.components.panel import Panel

__all__ = ["Application", "ApplicationContext"]

def is_boolean(value):
    """ Return whether the given value is a boolean or not.
    
    Args:
        value (Any): The value to check.
    
    Returns:
        bool: `True` if the given value is a boolean, `False` otherwise.
    """
    return (type(value) != type("") and str(value) in ["True", "False"]) or type(value) == type(1 == 1) or type(value) == type(1)

class Application:
    """ The `Application` class is the base class for all CLI applications. 
    
    Usage:
        >>> class MyApplication(Application):
        ...     def main(self):
        ...         print("Hello World!")
        ...         return True
        ...
        ...     def on_success(self, context):
        ...         # type: (ApplicationContext) -> None
        ...         print("Success!")
        ...
        ...     def on_failure(self, context):
        ...         # type: (ApplicationContext) -> None
        ...         print("Failure!")
        ... 
        >>> app = MyApplication()
        >>> app.run()
        --------------------------------------------------------------------------------
        
        Hello World!
        
        --------------------------------------------------------------------------------
        Success!
    """
    
    title = None # type: str|None
    """ The title of the CLI application. """

    max_width = None # type: int|None
    """ The maximum width of the console output. """

    console = None # type: Console|None
    """ The console used by the application. """

    divider = None # type: str|None
    """ String printed before and after the application execution. """

    _locals = {} # type: dict
    """ Will contain the local variables of the `Application.main()` method. 
    
    This attribute is set by the `Application.run()` method AFTER the execution
    of the `Application.main()` method and is only meant to be used INTERNALLY.
    """

    _raised = False
    """ Indicates whether an exception was raised during the execution of the
    `Application.main()` method.

    This attribute is set by the `Application.run()` method AFTER the execution
    of the `Application.main()` method and is only meant to be used INTERNALLY.
    """

    return_value = None # type: int|bool|None
    """ The return value of the `Application.main()` method. """

    def __init__(self, *args, **kwargs):
        """ Create a new `Application` instance. """
        title = kwargs.get("title", None)
        divider = kwargs.get("divider", None)
        max_width = kwargs.get("max_width", None)
        console = kwargs.get("console", None)

        if self.max_width is None and max_width is not None:
            self.max_width = max_width

        if self.console is None:
            if console is not None:
                if not isinstance(console, Console):
                    raise TypeError("The 'console' argument MUST be an instance of 'Console' (got '%s' with type '%s')." % (console, type(console)))
                self.console = console
            else:
                self.console = Console(width=self.max_width)

        # TODO: `Console._width` is a private attribute, create a public way to set it.
        if self.max_width is not None and self.console._width != self.max_width:
            self.console._width = self.max_width

        if self.title is None:
            if title is None:
                self.title = self.__class__.__name__
            else:
                self.title = title

        if self.divider is None:
            if divider is None:
                self.divider = Rule(
                    title="     %s     " % self.title,
                    style="cyan",
                    width=self.console.width,
                )
            else:
                self.divider = divider % {
                    "title": self.title,
                }
        else:
            self.divider = self.divider % {
                "title": self.title,
            }

    def main(self):
        # type: () -> bool|int
        """ The main method of the application.

        Please note that this method SHOULD return a boolean or an integer.
        Otherwise, the application will assume that it succeeded (eg. if 
        returns `None` or a string) and will print an `ApplicationWarning` message.

        This method MUST be overwritten when subclassing the `Application` class.
        
        Returns:
            success (bool|int): `True` if the application was successful, `False` 
                otherwise.
        """
        raise NotImplementedError(
            "This method MUST be overwritten when subclassing the `Application` class"
        )

    def on_finish(self, context):
        # type: (ApplicationContext) -> None
        """ Hook method that will be run when the `Application.main()` function
        ends with or without exceptions.

        This hook will be the last to be executed.

        This method MAY be overwritten when subclassing the `Application` class.

        Args:
            context(ApplicationContext): The context of the application.
        """
    
    def on_success(self, context):
        # type: (ApplicationContext) -> None
        """ Hook method that will be run when the `Application.main()` function
        ends without exceptions and with a truthy return value (or `None`).
        
        This method MAY be overwritten when subclassing the `Application` class.
        
        Args:
            context(ApplicationContext): The context of the application.
        """
    
    def on_failure(self, context):
        # type: (ApplicationContext) -> None
        """ Hook method that will be run when the `Application.main()` function
        ends with exceptions or with a falsy return value (`None` is not 
        considered as indicating a failure here).
        
        This method MAY be overwritten when subclassing the `Application` class.
        
        Args:
            context(ApplicationContext): The context of the application.
        """
    
    def _run_hook(self, hook, context):
        """ Run a hook method without blocking the execution of the application
        if the hook fails.

        This method is used internally by the `Application` class, and MUST
        NOT be overwritten when subclassing the `Application` class.

        Args:
            hook (callable): The hook method to run.
            context (ApplicationContext): The context of the application.

        Returns:
            Any: The return value of the hook method.
        """
        try:
            return hook(context)
        except:
            self.console.print("HookWarning: Error while executing the '%s' hook: %s" % (hook, _sys.exc_info()[1]))
            traceback.print_exc()
        
        return None

    def has_failed(self):
        """ Indicates whether the application has failed or not.

        This method MAY be overwritten when subclassing the `Application` 
        class to provide custom logic.

        Note that even if this method returns `True`, the final status
        will not be a success if the method `Application.main()` 
        raised an exception.

        Returns:
            bool: `True` if the application has failed, `False` otherwise.
        """
        # If the return value is not a boolean, we assume that the application
        # succeeded (since it correctly returned without an exception).
        if self.return_value is None or not is_boolean(self.return_value):
            return False
        
        return not self.return_value
    
    def run(self):
        # type: () -> None
        """ Run the CLI application, then execute the defined hooks.
        
        DO NOT overwrite this method when subclassing the `Application` class.

        This method will execute the following hooks:
            1. `Application.on_success()` / `Application.on_failure()`
            2. `Application.on_finish()` (last to be executed)
        """
        def _tracer(frame, event, arg):
            """ Tracer function used to get the local variables of the `Application.main()` method.
            
            See the following docs for more information:
            - https://docs.python.org/release/2.1/lib/module-sys.html (sys.setprofile() documentation)
            - https://docs.python.org/release/2.1/lib/profile-instant.html (Pyton profiler documentation)
            """
            if event == 'return':
                # Note that we use the 'update()' method instead of
                # assigning directly because it returned an object of type
                # `org.python.core.PyStringMap` instead of `org.python.core.PyDictionary`.
                self._locals = {}
                self._locals.update(frame.f_locals.copy())


        # Start the timer
        self._start_time = _time.time()

        self.console.print("\n\n", self.divider, "\n\n", sep="")
        _sys.setprofile(_tracer)    # The tracer is activated on next call, return or exception
        try:
            try:
                self.return_value = self.main()
            except SystemExit:
                # ? Should a SystemExit be re-raised or should redirect 
                # ? the exception to the correct handler?
                raise
            except:
                full_traceback = "".join(traceback.format_exception(*_sys.exc_info()))
                try:
                    exception_panel = Panel(
                        full_traceback,
                        title="Application Error",
                        border_style="red",
                    )
                    self.console.print(exception_panel)
                except:
                    # Fallback to the default traceback
                    self.console.print(full_traceback)

                self._raised = True
        finally:
            _sys.setprofile(None)   # Make sure to always remove the tracer
        self.console.print("\n\n", self.divider, "\n\n", sep="")

        # Stop the timer
        self._end_time = _time.time()
        self._execution_time = self._end_time - self._start_time

        if not self._raised and not is_boolean(self.return_value):
            self.console.print("ApplicationWarning: The return value of the 'Application.main()' method SHOULD be a boolean or an integer (got '%s' with type '%s')." % (self.return_value, type(self.return_value)))        

        if type(self._locals) != type({}):
            raise Exception("The '_locals' attribute MUST be a dictionary (got '%s' with type '%s')." % (self._locals, type(self._locals)))

        application_context = ApplicationContext(
            application=self,
            local_vars=self._locals, # pyright: ignore[reportGeneralTypeIssues]
            return_value=self.return_value,
            start_time=self._start_time,
            end_time=self._end_time,
        )


        if self._raised or self.has_failed():
            self._run_hook(self.on_failure, application_context)
        else:
            self._run_hook(self.on_success, application_context)

        self._run_hook(self.on_finish, application_context)

        # Exit the application with the return value of the main method
        # ONLY if failed.
        if self._raised or self.has_failed():
            _sys.exit(1)


class ApplicationContext:
    """ The `ApplicationContext` class holds information about the 
    execution of the `Application.main()`.
    
    It is used to provide this information to the hooks.
    
    Attributes:
        locals (dict): A dictionary containing the local variables of the `Application.main()` method.
        return_value (int|bool): The return value of the `Application.main()` method.
        duration (float): The duration of the `Application.main()` method.
        start_time (float): The start time of the `Application.main()` method.
        end_time (float): The end time of the `Application.main()` method.
    """
    application = None # type: Application|None
    """ The original application instance. 

    This can be used for example to access the `Application.title` or
    other attributes of the application. 
    """
    
    # We ignore the type here to be able to initialize the attribute
    # with a `None` value.
    locals = None # type: dict # type: ignore
    """ The local variables of the `Application.main()` method. """
    
    return_value = None # type: int|bool|None
    """ The return value of the `Application.main()` method. """

    duration = -1 # type: float
    """ The duration time (expressed in seconds) of the `Application.main()` method. """

    start_time = -1 # type: float
    """ The start time (timestamp) of the `Application.main()` method. """

    end_time = -1 # type: float
    """ The end time (timestamp) of the `Application.main()` method. """

    def __init__(self, application, local_vars, return_value, start_time, end_time):
        # type: (Application, dict, int|bool|None, float, float) -> None
        """ Create a new `ApplicationContext` instance.
        
        Args:
            application (Application): The original application instance.
            local_vars (dict): A dictionary containing the local variables of the `Application.main()` method.
            return_value (int|bool): The return value of the `Application.main()` method.
            start_time (float): The start time of the `Application.main()` method.
            end_time (float): The end time of the `Application.main()` method.
        """
        if type(local_vars) != type({}):
            raise TypeError("The 'local_vars' argument MUST be a dictionary (got '%s' with type '%s')." % (local_vars, type(local_vars)))
        
        self.application = application
        self.locals = local_vars
        self.return_value = return_value

        self.duration = end_time - start_time
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        # type: () -> str
        """ Return a string representation of the `ApplicationContext` instance. """
        return "%s(%s)" % (
            self.__class__.__name__,
            ", ".join([
                "%s=%s" % (key, value)
                for key, value in vars(self).items()
                if not key.startswith("_")
            ]),
        )



if __name__ == "__main__":
    class MyApplication(Application):
        """ This is a simple example of a CLI application. """
        
        title = "My Application"

        def main(self):
            text = "Hello World!"
            print(text)
            
            _time.sleep(2)
            return True
        
        def on_success(self, context):
            # type: (ApplicationContext) -> None
            print("Success! Text printed: %s" % context.locals.get("text", None))


        def on_failure(self, context):
            # type: (ApplicationContext) -> None
            print("Failure!")
        
        def on_finish(self, context):
            # type: (ApplicationContext) -> None
            print("Finish!")
            print("Context: %s" % context)

            print("\n\n---> Total execution time: %s seconds (%sh:%sm:%ss)\n\n" % (
                context.duration,
                int(context.duration / 3600),
                int(context.duration / 60 % 60),
                int(context.duration % 60)
            ))
    
    app = MyApplication()
    app.run()