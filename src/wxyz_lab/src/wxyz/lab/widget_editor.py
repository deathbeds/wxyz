""" Text editing widgets
"""
from .base import LabBase, T, W, module_name, module_version


@W.register
class EditorModeInfo(W.Widget):
    """CodeMirror modes known to the frontend"""

    _model_name = T.Unicode("EditorModeInfoModel").tag(sync=True)
    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)
    modes = T.Tuple().tag(sync=True)


@W.register
class EditorConfig(W.Widget):
    """JSON-compatible CodeMirror configuration options."""

    # pylint: disable=C0301
    _model_name = T.Unicode("EditorConfigModel").tag(sync=True)
    _model_module = T.Unicode(module_name).tag(sync=True)
    _model_module_version = T.Unicode(module_version).tag(sync=True)

    # the part between these comments will be rewritten
    # BEGIN SCHEMAGEN:TRAITS IEditorConfiguration @61e400d051e0be2c3d80ab6bbc304e616b0dce7729d13c64396b21352cf10855
    autofocus = T.Bool(
        help="""Can be used to make CodeMirror focus itself on initialization. Defaults to off. When fromTextArea is used, and no explicit value is given for this option, it will be set to true when either the source textarea is focused, or it has an autofocus attribute and no other element is focused.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    cursorBlinkRate = T.Union(
        [T.Float(), T.Int()],
        help="""Half - period in milliseconds used for cursor blinking. The default blink rate is 530ms.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    cursorHeight = T.Union(
        [T.Float(), T.Int()],
        help="""Determines the height of the cursor. Default is 1 , meaning it spans the whole height of the line. For some fonts (and by some tastes) a smaller height (for example 0.85), which causes the cursor to not reach all the way to the bottom of the line, looks better""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    dragDrop = T.Bool(
        help="""Controls whether drag-and - drop is enabled. On by default.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    electricChars = T.Bool(
        help="""Configures whether the editor should re-indent the current line when a character is typed that might change its proper indentation (only works if the mode supports indentation). Default is true.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    firstLineNumber = T.Union(
        [T.Float(), T.Int()],
        help="""At which number to start counting lines. Default is 1.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    fixedGutter = T.Bool(
        help="""Determines whether the gutter scrolls along with the content horizontally (false) or whether it stays fixed during horizontal scrolling (true, the default).""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    flattenSpans = T.Bool(
        help="""By default, CodeMirror will combine adjacent tokens into a single span if they have the same class. This will result in a simpler DOM tree, and thus perform better. With some kinds of styling(such as rounded corners), this will change the way the document looks. You can set this option to false to disable this behavior.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    foldGutter = T.Bool(
        help="""Provides an option foldGutter, which can be used to create a gutter with markers indicating the blocks that can be folded.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    gutters = T.Union(
        [T.Tuple(), T.Enum([None])],
        help="""Can be used to add extra gutters (beyond or instead of the line number gutter). Should be an array of CSS class names, each of which defines a width (and optionally a background), and which will be used to draw the background of the gutters. May include the CodeMirror-linenumbers class, in order to explicitly set the position of the line number gutter (it will default to be to the right of all other gutters). These class names are the keys passed to setGutterMarker.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    historyEventDelay = T.Union(
        [T.Float(), T.Int()],
        help="""The period of inactivity (in milliseconds) that will cause a new history event to be started when typing or deleting. Defaults to 500.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    indentUnit = T.Union(
        [T.Float(), T.Int()],
        help="""How many spaces a block (whatever that means in the edited language) should be indented. The default is 2.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    indentWithTabs = T.Bool(
        help="""Whether, when indenting, the first N*tabSize spaces should be replaced by N tabs. Default is false.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    keyMap = T.Unicode(
        help="""Configures the keymap to use. The default is "default", which is the only keymap defined in codemirror.js itself. Extra keymaps are found in the keymap directory. See the section on keymaps for more information.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    lineNumbers = T.Bool(
        help="""Whether to show line numbers to the left of the editor.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    lineWrapping = T.Bool(
        help="""Whether CodeMirror should scroll or wrap for long lines. Defaults to false (scroll).""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    maxHighlightLength = T.Union(
        [T.Float(), T.Int()],
        help="""When highlighting long lines, in order to stay responsive, the editor will give up and simply style the rest of the line as plain text when it reaches a certain position. The default is 10000. You can set this to Infinity to turn off this behavior.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    mode = T.Union(
        [T.Unicode(), T.Dict()],
        help="""string|object. The mode to use. When not given, this will default to the first mode that was loaded. It may be a string, which either simply names the mode or is a MIME type associated with the mode. Alternatively, it may be an object containing configuration options for the mode, with a name property that names the mode (for example {name: "javascript", json: true}).""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    placeholder = T.Unicode(
        help="""Optional value to be used in conjunction with CodeMirror’s placeholder add-on.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    pollInterval = T.Union(
        [T.Float(), T.Int()],
        help="""Indicates how quickly CodeMirror should poll its input textarea for changes(when focused). Most input is captured by events, but some things, like IME input on some browsers, don't generate events that allow CodeMirror to properly detect it. Thus, it polls. Default is 100 milliseconds.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    readOnly = T.Union(
        [T.Bool(), T.Enum("nocursor")],
        help="""boolean|string. This disables editing of the editor content by the user. If the special value "nocursor" is given (instead of simply true), focusing of the editor is also disallowed.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    rtlMoveVisually = T.Bool(
        help="""Determines whether horizontal cursor movement through right-to-left (Arabic, Hebrew) text is visual (pressing the left arrow moves the cursor left) or logical (pressing the left arrow moves to the next lower index in the string, which is visually right in right-to-left text). The default is false on Windows, and true on other platforms.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    scrollbarStyle = T.Unicode(
        help="""Chooses a scrollbar implementation. The default is "native", showing native scrollbars. The core library also provides the "null" style, which completely hides the scrollbars. Addons can implement additional scrollbar models.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    showCursorWhenSelecting = T.Bool(
        help="""Whether the cursor should be drawn when a selection is active. Defaults to false.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    smartIndent = T.Bool(
        help="""Whether to use the context-sensitive indentation that the mode provides (or just indent the same as the line before). Defaults to true.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    tabSize = T.Union(
        [T.Float(), T.Int()],
        help="""The width of a tab character. Defaults to 4.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    tabindex = T.Union(
        [T.Float(), T.Int()],
        help="""The tab index to assign to the editor. If not given, no tab index will be assigned.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    theme = T.Unicode(
        help="""The theme to style the editor with. You must make sure the CSS file defining the corresponding .cm-s-[name] styles is loaded. The default is "default".""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    undoDepth = T.Union(
        [T.Float(), T.Int()],
        help="""The maximum number of undo levels that the editor stores. Defaults to 40.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    viewportMargin = T.Union(
        [T.Float(), T.Int()],
        help="""Specifies the amount of lines that are rendered above and below the part of the document that's currently scrolled into view. This affects the amount of updates needed when scrolling, and the amount of work that such an update does. You should usually leave it at its default, 10. Can be set to Infinity to make sure the whole document is always rendered, and thus the browser's text search works on it. This will have bad effects on performance of big documents.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    workDelay = T.Union(
        [T.Float(), T.Int()],
        help="""See workTime.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    workTime = T.Union(
        [T.Float(), T.Int()],
        help="""Highlighting is done by a pseudo background - thread that will work for workTime milliseconds, and then use timeout to sleep for workDelay milliseconds. The defaults are 200 and 300, you can change these options to make the highlighting more or less aggressive.""",
        allow_none=True,
        default_value=None,
    ).tag(sync=True)
    # END SCHEMAGEN:TRAITS


@W.register
class Editor(LabBase, W.Textarea):
    """A basic editor"""

    # pylint: disable=no-member

    value = T.Any().tag(sync=True)

    _model_name = T.Unicode("EditorModel").tag(sync=True)
    _view_name = T.Unicode("EditorView").tag(sync=True)

    config = W.trait_types.InstanceDict(EditorConfig).tag(
        sync=True, **W.widget_serialization
    )

    scroll_y = T.Int(0).tag(sync=True)
    scroll_x = T.Int(0).tag(sync=True)
