# Contributing to wxyz

## Setup

- Get [Miniforge](https://github.com/conda-forge/miniforge/releases)
- Create a dev environment from a [lockfile](./ci/locks):

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

> This actually runs the `binder` task, which is used in `postBuild` for the
> interactive demo

### Do everything to prepare for a release

```bash
doit release
```

### Live Development

To rebuild the labextension and your JupyterLab, use:

```bash
doit watch
```

> When new files are created, it is usually necessary to re-start the watch command,
> stop it with <kbd>Ctrl+C</kbd>.

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

## Updating lockfiles

The lockfiles in `ci/locks` are created in a separate environment from the main
development environment to avoid a `conda` dependency.

```bash
conda create --prefix envs/lock --file ci/locks/conda.lock.linux-64-3.8-.lock
source envs/lock/bin/activate
doit lock
```
