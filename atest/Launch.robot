*** Settings ***
Documentation     Work with the WXYZ Lab server
Library           OperatingSystem
Library           JupyterLibrary
Library           String
Library           Process

*** Keywords ***
Start New WXYZ Lab Server
    [Documentation]    Try to start the WXYZ Lab server
    ${proc} =    Start New Jupyter Server   jupyter-lab
    ...   env:JUPYTERLAB_DIR=%{PROJECT_DIR}${/}lab
    ...   stdout=${OUTPUT DIR}${/}server.log
    ...   stderr=STDOUT
    Wait For Jupyter Server To Be Ready
    [Return]   ${proc}
