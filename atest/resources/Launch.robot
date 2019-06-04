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
    Wait Until Keyword Succeeds    5x    5s  WXYZ Server Is Running
    [Return]   ${proc}

WXYZ Server Is Running
    ${log} =  Get File   ${OUTPUT DIR}${/}server.log
    Should Contain    ${log}    is running
