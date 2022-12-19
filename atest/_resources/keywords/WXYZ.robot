*** Settings ***
Resource    ../variables/WXYZ.robot


*** Keywords ***
Open WXYZ Notebook
    [Arguments]    ${notebook}    ${path}=${WXYZ_NOTEBOOKS}
    Set Tags    ipynb:notebook
    ${full path} =    Normalize Path    ${path}${/}${notebook}.ipynb
    File Should Exist    ${full path}
    Open File    ${full path}    ${MENU NOTEBOOK}
    Wait Until Page Contains Element    ${JLAB XP KERNEL IDLE}    timeout=30s
    Ensure Sidebar Is Closed
    Capture Page Screenshot    01-loaded.png
