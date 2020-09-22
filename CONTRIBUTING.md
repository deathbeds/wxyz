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

### Run everything

```bash
doit
```

### Live Development

Watch typescript sources:

```bash
doit watch
```

Watch Lab:

```bash
doit lab
```
