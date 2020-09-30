*** Settings ***
Documentation     Basic all-or-nothing run of notebooks
Suite Setup       Setup Suite For Screenshots    notebooks
Resource          Keywords.robot

*** Variables ***
${SCREENS}        ${SCREENS ROOT}${/}notebooks

*** Test Cases ***
Index
    Open WXYZ Notebook    index
    Restart and Run All
    Wait For All Cells To Run    60s
    Capture All Code Cells
    Page Should Not Contain Element    ${JLAB XP STDERR}
    Capture Page Screenshot    99-fin.png
    [Teardown]    Clean up after Working with file    index.ipynb

*** Keywords ***
Open WXYZ Notebook
    [Arguments]    ${notebook}    ${path}=${WXYZ_NOTEBOOKS}
    Set Screenshot Directory    ${SCREENS}${/}00-index
    ${full path} =    Normalize Path    ${path}${/}${notebook}.ipynb
    File Should Exist    ${full path}
    Open File    ${full path}    ${MENU NOTEBOOK}
    Sleep    5s
    Capture Page Screenshot    01-loaded.png

Restart and Run All
    Lab Command    Restart Kernel and Run All Cells
    Accept Default Dialog Option

Capture All Code Cells
    [Arguments]    ${prefix}=${EMPTY}
    ${cells} =    Get WebElements    ${JLAB XP CODE CELLS}
    FOR    ${idx}    ${cell}    IN ENUMERATE    @{cells}
        Capture Element Screenshot    ${JLAB XP CODE CELLS}\[${idx.__add__(1)}]    ${prefix}cell-${idx}.png
    END