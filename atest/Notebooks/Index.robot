*** Settings ***
Documentation     Basic all-or-nothing run of index notebook
Suite Setup       Setup Suite For Screenshots    notebook-index
Resource          ../Keywords.robot

*** Variables ***
${SCREENS}        ${SCREENS ROOT}${/}notebook-index

*** Test Cases ***
Index
    Open WXYZ Notebook    index
    Restart and Run All
    Wait For All Cells To Run    60s
    Capture All Code Cells
    Page Should Not Contain Element    ${JLAB XP STDERR}
    Capture Page Screenshot    99-fin.png
    # Browser Log Should Not Contain    ${some file content}
    [Teardown]    Clean up after Working with file    index.ipynb
