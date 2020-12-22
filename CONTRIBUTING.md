# Contributing to wxyz

Get [Miniforge][]. Create/activate a dev environment from a [lockfile][], list tasks.

    conda create --prefix envs/docs --file ci/locks/conda.docs.linux-64-3.8-2.2.lock
    source activate envs/docs
    doit list

[miniforge]: https://github.com/conda-forge/miniforge/releases
[lockfile]: ./ci/locks

## Use doit

Local development and continuous integration are both driven by [pydoit](https://pydoit.org/contents.html).

### View all doit commands

    doit list

### Run everything up to development

    doit

> This actually runs the `binder` task, which is used in `postBuild` for the
> interactive demo

### Do everything to prepare for a release

    doit release

### Live Development

To rebuild the labextension and your JupyterLab, use:

    doit watch

> When new files are created, it is usually necessary to re-start the watch command,
> stop it with <kbd>Ctrl+C</kbd>.

## Testing

### Notebooks

Tests are primarily captured as executable notebooks imported or linked to from
the [notebook index](src/py/wxyz_notebooks/src/wxyz/notebooks/index.ipynb).

Each notebook should:

- have a descriptive name
- demonstrate the value provided by the widgets in question as simply as possible
- provide a higher-level confection of `wxyz` widgets, usually a DockBox
- be imported into the index, unless it has very taxing, less-portable dependencies

### Robot Framework Testing

Where appropriate, individual components should be tested with Robot Framework
tests. Ideal tests include thoroughly excercising the demo notebooks as a user would.

    doit robot

## Code Style

Code style is enforced by a number of python, typescript and miscellaneous files
(e.g. YAML, JSON).

    doit lint*

## Updating lockfiles

The lockfiles in `ci/locks` are created in a separate environment from the main
development environment to avoid a `conda` dependency.

    conda create --prefix envs/lock --file ci/locks/conda.lock.linux-64-3.8-.lock
    source envs/lock/bin/activate
    doit lock
