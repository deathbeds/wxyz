*** Settings ***
Documentation     Distributed Version Control
Suite Setup       Setup Suite For Screenshots    notebook-dvcs
Resource          ../Keywords.robot

*** Variables ***
${SCREENS}        ${SCREENS ROOT}${/}notebook-dvcs
${GIT I}          Git I

*** Test Cases ***
Git I
    Set Screenshot Directory    ${SCREENS}${/}git-i
    Open WXYZ Notebook    ${GIT I}    ${WXYZ EXAMPLES}
    Restart and Run All
    Wait For All Cells To Run    60s
    Capture All Code Cells
    Page Should Not Contain Element    ${JLAB XP STDERR}
    Capture Page Screenshot    99-fin.png
    # Browser Log Should Not Contain    ${some file content}
    [Teardown]    Clean up after Working with file    ${GIT I}.ipynb
