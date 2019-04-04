from collections import defaultdict

import ipywidgets as W

# some reasonable default styles (e.g. Grid, Dock)
BLOCK_LAYOUT = dict(
    layout=dict(
        height="50vh"
    )
)

_HANDLERS = dict(
    type_by_name=defaultdict(list),
    type=defaultdict(list)
)

def for_type_by_name(package=None, klazz=None, factory=None):
    if package is None and klazz is None:
        return _HANDLERS["type_by_name"]
    if factory is None:
        return _HANDLERS["type_by_name"][(package, klazz)]
    _HANDLERS["type_by_name"][(package, klazz)].append(factory)


def for_type(klazz=None, factory=None):
    if klazz is None:
        return _HANDLERS["type"]
    if factory is None:
        return _HANDLERS["type"][klazz]
    _HANDLERS["type"][klazz].append(factory)
