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
    Wait Until Page Contains Element    ${JLAB XP KERNEL IDLE}    timeout=30s
    Capture Page Screenshot    01-loaded.png

Restart and Run All
    Lab Command    Clear All Outputs
    Lab Command    Restart Kernel and Run All Cells
    Accept Default Dialog Option
    Wait Until Element Contains    ${JLAB XP LAST CODE PROMPT}    [*]:

Capture All Code Cells
    [Arguments]    ${prefix}=${EMPTY}    ${timeout}=30s
    ${cells} =    Get WebElements    ${JLAB XP CODE CELLS}
    Lab Command    Expand All Code
    FOR    ${idx}    ${cell}    IN ENUMERATE    @{cells}
        ${sel} =    Set Variable    ${JLAB XP CODE CELLS}\[${idx.__add__(1)}]
        Run Keyword and Ignore Error    Wait Until Element does not contain    ${sel}    [*]:    timeout=${timeout}
        Capture Element Screenshot    ${sel}    ${prefix}cell-${idx.__repr__().zfill(3)}.png
    END
