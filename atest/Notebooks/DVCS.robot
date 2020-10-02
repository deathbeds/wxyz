*** Settings ***
Documentation     Distributed Version Control
Suite Setup       Setup Suite For Screenshots    notebook-dvcs
Resource          ../Keywords.robot

*** Variables ***
${SCREENS}        ${SCREENS ROOT}${/}notebook-dvcs
${GIT I}          Git I
${XP COMMITTER}    xpath://*[contains(@class, "jp-wxyz-dvcs-tool-commit-box")]
${XP COMMIT BTN}    xpath://*[contains(@class, "jp-wxyz-dvcs-tool-commit-btn")]
${XP COMMIT MSG}    xpath://*[contains(@class, "jp-wxyz-dvcs-tool-commit-msg")]/input
${XP PG TEXTAREA}    xpath://*[contains(@class, "jp-wxyz-dvcs-playground-textarea")]/textarea
${XP PG BOX}      xpath://*[contains(@class, "jp-wxyz-dvcs-playground-box")]

*** Test Cases ***
Git I
    Set Screenshot Directory    ${SCREENS}${/}git-i
    Open WXYZ Notebook    ${GIT I}    ${WXYZ EXAMPLES}
    Restart and Run All
    Wait For All Cells To Run    60s
    Capture All Code Cells
    Page Should Not Contain Element    ${JLAB XP STDERR}
    Capture Element Screenshot    ${XP PG BOX}    10-before-initial-commit.png
    Commit
    Capture Element Screenshot    ${XP PG BOX}    20-after-initial-commit.png
    Input Text    ${XP PG TEXTAREA}    hello world
    Commit    another commit
    Capture Element Screenshot    ${XP PG BOX}    30-after-hello.png
    [Teardown]    Clean up after Working with file    ${GIT I}.ipynb

*** Keywords ***
Commit
    [Arguments]    ${msg}=${EMPTY}
    Input Text    ${XP COMMIT MSG}    ${msg}
    Wait Until Element Is Enabled    ${XP COMMIT BTN}
    Sleep    0.5s
    Click Element    ${XP COMMIT BTN}
    Wait Until Page Contains    No changes    timeout=10s
