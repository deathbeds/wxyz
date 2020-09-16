""" Some more color traits and widgets
"""
# pylint: disable=R0903,R0901
import re

from wxyz.core.base import W

RE_RGB_EH = re.compile(r"rgba?\(\d+,\s*\d+,\s*\d+,\s*[10](\.\d+)?\)")


class AlphaColor(W.widgets.trait_types.Color):
    """A color with alpha"""

    def validate(self, obj, value):
        """expand the validation to work for rgba"""
        if RE_RGB_EH.match(value):
            return value
        return super().validate(obj, value)


class EmptyAlphaColor(W.widgets.trait_types.Color):
    """A color with alpha that might be the empty string"""

    def validate(self, obj, value):
        """expand the validation to work for rgba"""
        if value == "":
            return value
        return super().validate(obj, value)


class AlphaColorPicker(W.ColorPicker):
    """A color picker that should allow setting opacity"""

    value = AlphaColor("rgba(128, 128, 128, 0.5)").tag(sync=True)
