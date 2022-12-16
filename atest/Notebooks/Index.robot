*** Settings ***
Documentation       Basic all-or-nothing run of index notebook

Resource            ../_resources/keywords/Browser.robot
Resource            ../_resources/keywords/Lab.robot
Resource            ../_resources/keywords/WXYZ.robot

Suite Setup         Setup Suite For Screenshots    notebook-index


*** Variables ***
${SCREENS}      ${SCREENS ROOT}${/}notebook-index


*** Test Cases ***
Index
    Open WXYZ Notebook    index
    Restart and Run All
    Wait For All Cells To Run    120s
    Capture All Code Cells
    Page Should Not Contain Element    ${JLAB XP STDERR}
    Capture Page Screenshot    99-fin.png
    # Browser Log Should Not Contain    ${some file content}
    [Teardown]    Clean up after Working with file    index.ipynb
