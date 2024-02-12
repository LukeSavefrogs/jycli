# Jython CLI Library

The JyCLI (_Jython CLI_) package has been developed to make it easier to create script to create CLI applications using Jython.

## `application.Application`

The `application.Application` class allows creating CLI applications in a standardized way.

### Features

- **Automatic exit status**: `1` if the return status is a falsy boolean (_both `bool` or just a falsy `int`_), `0` otherwise (_`None` is considered as success_);
- Automatic **divider** to separate the actual script execution from all the previous boilerplate (_by default a full-width line consisting of `-` characters with the application name at the center_); can be customized.
- Use **hooks** to customize the behavior of the application before it closes: `on_success` (_when it ends without errors_), `on_failure` (_when it fails because of an exception or falsy return code_) and `on_finish` (_always executed at the end before closing the application_).
- Define a custom `has_failed` method if you want to customize when a specific return code should make the application fail (_for example, you may want to restrict only to numeric return values_).
- Automatically disables colors when it detects the [`NO_COLOR` variable](https://no-color.org/) or if the console is not interactive.

### Example

Take the following simple application. If you execute this code you'll note that the **return code** of is set to `0` (_which means success in Bash_); if you change the `return` statement in the `MyApplication.main()` method to `return 1==0` (_basically `False`_) the RC of the application will be `1` (_which means that an error occurred in Bash_).

Another thing to take note is that **hooks** can access **local variables** defined in the `MyApplication.main()` using the `context.locals` dictionary.

```python
from jycli.application import Application, ApplicationContext

class MyApplication(Application):
    """ This is a simple example of a CLI application. """
    title = "My Application"

    divider = "------------------- %(title)s -------------------"

    def main(self):
        text = "Hello World!"
        print(text)
        
        _time.sleep(2)
        return 1==1
    
    def on_success(self, context):
        # type: (ApplicationContext) -> None
        print("Success! Text printed: %s" % context.locals.get("text", None))

    def on_failure(self, context):
        # type: (ApplicationContext) -> None
        print("Failure!")
    
    def on_finish(self, context):
        # type: (ApplicationContext) -> None
        print("\nFinish!")
        print("Context: %s" % context)

        print("\n---> Total execution time: %s seconds (%sh:%sm:%ss)" % (
            context.duration,
            int(context.duration / 3600),
            int(context.duration / 60 % 60),
            int(context.duration % 60)
        ))


app = MyApplication()
app.run()
```

This code will produce the following output:

```text
------------------- My Application -------------------
Hello World!
------------------- My Application -------------------
Success! Text printed: Hello World!

Finish!
Context: ApplicationContext(duration=2.0, locals={'self': <__main__.MyApplication instance at 1094034428>, 'text': 'Hello World!'}, start_time=1.702979951763E9, return_value=True, end_time=1.702979953763E9, application=<__main__.MyApplication instance at 1094034428>)

---> Total execution time: 2.0 seconds (0h:0m:2s)
```

## `table` module

The `table` module exposes the `Table` class that comes in handy when creating **tables** that should render nicely (_and responsively_) in the terminal. It also provides methods for exporting the table data in **CSV** (`.to_csv()`) and **HTML** (`.to_html()`) format.

### Features

- Support for multiple render targets: to **terminal** (`.render()`), to **CSV** (`.to_csv()`) and to **HTML** (`.to_html()`);
- Customize the **table width** when rendering to the terminal (_default is full terminal width_);
- **Wrap lines** if they are too long to render on a single line or if they contains a new line (`\n`).

### Example

```python
from jycli.table import Table

table = Table("My beautiful table", ["Column1", "Column2"])
table.add_row("Value1", "Value2")
table.add_row("Value3", "Value4")

print(table.render())
# Output:
#   ***********************************************************
#                        My beautiful table
#   ***********************************************************
#   Column1                     | Column2
#   --------------------------- | --------------------------
#   Value1                      | Value2
#   Value3                      | Value4


print(table.to_csv())
# Output:
#   Column1,Column2
#   Value1,Value2
#   Value3,Value4

print(table.to_html())
# Output:
#   <table>
#   <caption>My beautiful table</caption>
#   <thead>
#   <tr>
#   <th>Column1</th>
#   <th>Column2</th>
#   </tr>
#   </thead>
#   <tbody>
#   <tr>
#   <td>Value1</td>
#   <td>Value2</td>
#   </tr>
#   <tr>
#   <td>Value3</td>
#   <td>Value4</td>
#   </tr>
#   </tbody>
```

## `console` module

The `console` module as the name suggests allows interacting with the console terminal.

For example, you can get the terminal width and height:

```python
from jycli.console import Console

console = Console()
print("%dh x %dw" % (console.width, console.height))
```
