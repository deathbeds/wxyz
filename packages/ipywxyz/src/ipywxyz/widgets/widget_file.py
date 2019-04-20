from ._base import Base, T, W


@W.register
class File(Base):
    """ A file. Might be uploaded from the browser.

        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
    """

    _model_name = T.Unicode("FileModel").tag(sync=True)
    _view_name = T.Unicode("FileView").tag(sync=True)

    value = T.Bytes(help="The binary representation of the file").tag(
        sync=True, **W.trait_types.bytes_serialization
    )
    name = T.Unicode(help="The file's name").tag(sync=True)
    last_modified = T.Int(help="Timestamp of last file modification")
    size = T.Int(help="The size of the file in bytes")
    mime_type = T.Unicode(help="The file's MIME type.").tag(sync=True)


@W.register
class FileBox(Base, W.Box):
    """ A box of files, which can be used to upload and download files
    """

    _model_name = T.Unicode("FileBoxModel").tag(sync=True)
    _view_name = T.Unicode("FileBoxView").tag(sync=True)

    children = W.trait_types.TypedTuple(
        trait=T.Instance(File), help="List of file widgets"
    ).tag(sync=True, **W.widget_serialization)

    accept = W.trait_types.TypedTuple(
        trait=T.Unicode(), help="uploadable extensions and mimetypes (with wildcards)"
    ).tag(sync=True)

    multiple = T.Bool(False, help="if true, accept multiple files").tag(sync=True)
