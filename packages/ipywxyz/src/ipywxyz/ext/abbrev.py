import functools
import inspect

import IPython.core.formatters
import ipywidgets as W
from ..widgets.abbrev import for_type_by_name, for_type

WI = W.interactive


class WidgetAbbrev(IPython.core.formatters.BaseFormatter):
    _return_type = object

    def __call__(self, obj, *whatever):
        value = super().__call__(obj)

        if isinstance(value, str):
            value = inspect.unwrap(WI.widget_from_abbrev)(obj)

        return value

def load_ipython_extension(shell):
    """ Add handlers for common types for `ipywidgets.interact` compatible
        with WXYZ widgets
    """

    unload_ipython_extension(shell)

    WI.widget_from_abbrev = functools.wraps(WI.widget_from_abbrev)(WidgetAbbrev())

    for pkg_klazz, factories in for_type_by_name().items():
        print(pkg_klazz, factories)
        for factory in factories:
            WI.widget_from_abbrev.for_type_by_name(*pkg_klazz, factory)

    for klazz, factories in for_type().items():
        print(klazz, factories)
        for factory in factories:
            WI.widget_from_abbrev.for_type(klazz, factory)


def unload_ipython_extension(shell):
    WI.widget_from_abbrev = inspect.unwrap(WI.widget_from_abbrev)

__test__ = {
"test": """>>> load_ipython_extension(get_ipython())
>>> import pandas, ipywidgets
>>> ipywidgets.interactive.widget_from_abbrev(pandas.util.testing.makeTimeDataFrame())
DataGrid(layout=Layout(height='50vh'))

>>> ipywidgets.interactive.widget_from_abbrev((0, 10))
IntSlider(value=5, max=10)

>>> ipywidgets.interactive.widget_from_abbrev("Editor")
Editor(value='Editor', layout=Layout(height='50vh'))
"""}
