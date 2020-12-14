# wxyz.dvcs

> widgets for working with data in revision control

## Examples

### Simple git files

> A `Workspace` provides a `pathlib.Path`

```python
from pathlib import Path
from wxyz.dvcs import Git, Workspace

repo = Git(Path("repo"))
work = Workspace(Path("workspace"), repo=repo)
# or work = repo.workspace(Path("workspace"))

(work / "README.md").write_text("# My new workspace")

work.commit(message = "initial commit")
origin = repo.remote("origin", "http://git.example.com/example.git")
origin.push()
```

## A DataFrame that tracks edit history

```python
import pandas
from wxyz.dvcs import Fossil, Frame

repo = Fossil(Path("repo"))
frame = Frame()
frame.df = pandas.util.testing.makeDataFrame()
```

## A `rdflib.ConjunctiveGraph` with edit history

```python
import rdflib
from wxyz.dvcs import Graph

repo = Git(Path("repo"))
frame = Frame()
frame.df = pandas.util.testing.makeDataFrame()
```
