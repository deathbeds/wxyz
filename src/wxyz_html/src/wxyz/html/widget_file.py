""" File upload/download widgets
"""
# pylint: disable=no-member
import json

from .base import HTMLBase, T, W


@W.register
class File(HTMLBase):
    """A file. Might be uploaded from the browser.

    https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
    """

    _model_name = T.Unicode("FileModel").tag(sync=True)
    _view_name = T.Unicode("FileView").tag(sync=True)

    value = T.Bytes(help="The binary representation of the file").tag(
        sync=True, **W.trait_types.bytes_serialization
    )
    name = T.Unicode(help="The file's name").tag(sync=True)
    last_modified = T.Int(help="Timestamp of last file modification").tag(sync=True)
    size = T.Int(help="The size of the file in bytes").tag(sync=True)
    mime_type = T.Unicode(help="The file's MIME type.").tag(sync=True)

    def proxy(self, klass, **kwargs):
        """Generate a Proxy file object, given a File-compatible class"""
        traits = ["name", "mime_type", "size", "last_modified", "value"]
        for trait in traits:
            if trait not in kwargs:
                kwargs[trait] = getattr(self, trait)

        klass_file = klass(**kwargs)

        with klass_file.hold_trait_notifications():
            with self.hold_trait_notifications():
                for trait in traits:
                    T.link((self, trait), (klass_file, trait))

        return klass_file


@W.register
class TextFile(File):
    """A Text file"""

    _model_name = T.Unicode("TextFileModel").tag(sync=True)

    text = T.Unicode().tag(sync=True)
    encoding = T.Unicode("utf-8")

    def __init__(self, *args, **kwargs):
        if "encoding" not in kwargs:
            kwargs["encoding"] = "utf-8"
        if "text" in kwargs and "value" not in kwargs:
            kwargs["value"] = kwargs["text"].decode(kwargs["encoding"])
        elif "value" in kwargs and "json" not in kwargs:
            kwargs["text"] = kwargs["value"].decode(encoding=kwargs["encoding"])
        super().__init__(*args, **kwargs)

        with self.hold_trait_notifications():
            self.observe(self._on_bytes, "value")
            self.observe(self._on_text, "text")

    def _on_bytes(self, change):
        self.text = change.new.decode(encoding=self.encoding)

    def _on_text(self, change):
        value = change.new.encode(self.encoding)
        size = len(value)
        if value is not None and value != self.value:
            with self.hold_trait_notifications():
                self.value, self.size = value, size


@W.register
class JSONFile(File):
    """A JSON file"""

    _model_name = T.Unicode("JSONFileModel").tag(sync=True)

    json = T.Union(
        [T.Dict(), T.List(), T.Unicode(), T.Int(), T.Float(), T.Bool()], allow_none=True
    ).tag(sync=True)

    def __init__(self, *args, **kwargs):
        if "json" in kwargs and "value" not in kwargs:
            try:
                kwargs["value"] = json.dumps(
                    kwargs["json"], indent=2, sort_keys=True
                ).encode("utf-8")
            except json.JSONDecodeError:
                pass
        elif "value" in kwargs and "json" not in kwargs:
            try:
                kwargs["json"] = json.loads(kwargs["value"].decode(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        super().__init__(*args, **kwargs)

        with self.hold_trait_notifications():
            self.observe(self._on_bytes, "value")
            self.observe(self._on_json, "json")

    def _on_bytes(self, change):
        self.json = json.loads(change.new.decode(encoding="utf-8"))

    def _on_json(self, change):
        value = json.dumps(change.new, sort_keys=True, indent=2).encode("utf-8")
        size = len(value)
        if value is not None and value != self.value:
            with self.hold_trait_notifications():
                self.value, self.size = value, size


@W.register
class FileBox(HTMLBase, W.Box):
    """A box of files, which can be used to upload and download files"""

    _model_name = T.Unicode("FileBoxModel").tag(sync=True)
    _view_name = T.Unicode("FileBoxView").tag(sync=True)

    children = W.trait_types.TypedTuple(
        trait=T.Instance(File), help="List of file widgets"
    ).tag(sync=True, **W.widget_serialization)

    accept = W.trait_types.TypedTuple(
        trait=T.Unicode(), help="uploadable extensions and mimetypes (with wildcards)"
    ).tag(sync=True)

    multiple = T.Bool(False, help="if true, accept multiple files").tag(sync=True)
