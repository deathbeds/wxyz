::rem this really shouldn't be used locally
call %CONDA%/Scripts/activate.bat ./envs/_base

doit -n4 nbtest robot || doit nbtest robot || exit 1
