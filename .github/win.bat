::rem this really shouldn't be used locally
call %CONDA%/Scripts/activate.bat ./envs/_base

doit setup_py_ci nbtest robot || doit setup_py_ci nbtest robot || exit 1
