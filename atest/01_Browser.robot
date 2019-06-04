*** Settings ***
Library   JupyterLibrary
Resource  ./Browser.robot
Test Setup        Open WXYZ Lab    browser=${BROWSER}
Test Teardown     Run Keywords    Execute JupyterLab Command    Save Notebook
...               AND    Wait Until Keyword Succeeds    2 x    1 s    Execute JupyterLab Command    Reset Application State
...               AND    Run keyword And Ignore Error    Handle Alert    timeout=1 s
...               AND    Close Browser

*** Test Cases ***
Launcher
    Set Screenshot Directory   ${OUTPUT DIR}${/}launcher
    Wait Until Page Contains   Launcher
    Capture Page Screenshot  00_launcher.png
