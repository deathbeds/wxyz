# Contributing to wxyz

## Setup

- Get [Miniconda for Python 3](https://repo.anaconda.com/miniconda/)
- Create a dev environment from a [lockfile](./ci/locks)

  ```bash
  conda create --prefix envs/dev --file ci/locks/conda.test.linux-64-3.8-2.2.lock
  ```

- Activate the environment

  ```bash
  source activate envs/dev
  ```

## Use doit

Local development and continuous integration are both driven by [pydoit](https://pydoit.org/contents.html).

### View all doit commands

```bash
doit list
```

### Run everything up to development

```bash
doit
```

> this actually runs the `binder` task

### Live Development

Watch typescript sources:

```bash
doit watch
```

Watch Lab:

```bash
doit lab
```

## Testing

### Notebooks

Tests are primarily captured as executable notebooks imported or linked to from
the [notebook index](src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb).

Each notebook should:

- have a descriptive name
- demonstrate the value provided by the widget in question as simply as possible
- provide a higher-level confection of wxyz widgets, usually a DockBox
- be imported into the notebook, unless it has very taxing, less-portable dependencies

### Robot Framework Testing

Where appropriate, individual components should be tested with Robot Framework
tests. Ideal tests include thoroughly excercising the demo notebooks.

```bash
doit robot
```

## Code Style

Code style is enforced by a number of python, typescript and miscellaneous files
(e.g. YAML, JSON).

```bash
doit lint*
```
