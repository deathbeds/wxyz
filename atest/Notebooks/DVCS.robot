*** Settings ***
Documentation       Distributed Version Control

Resource            ../_resources/keywords/Browser.robot
Resource            ../_resources/keywords/Lab.robot
Resource            ../_resources/keywords/WXYZ.robot

Suite Setup         Setup Suite For Screenshots    notebook-dvcs


*** Variables ***
${SCREENS}                  ${SCREENS ROOT}${/}notebook-dvcs
${GIT I}                    Git I
${XP COMMITTER}             xpath://*[contains(@class, "jp-wxyz-dvcs-tool-commit-box")]
${XP COMMIT BTN}            xpath://*[contains(@class, "jp-wxyz-dvcs-tool-commit-btn")]
${XP COMMIT MSG}            xpath://*[contains(@class, "jp-wxyz-dvcs-tool-commit-msg")]/input
${XP PG TEXTAREA}           xpath://*[contains(@class, "jp-wxyz-dvcs-playground-textarea")]/textarea
${XP PG BOX}                xpath://*[contains(@class, "jp-wxyz-dvcs-playground-box")]
${CSS SLIDER}               css:.ui-slider-handle
${CSS ENABLE TIMETRAVEL}    css:input[title="Time Travel"]


*** Test Cases ***
Git I
    Set Screenshot Directory    ${SCREENS}${/}git-i
    Open WXYZ Notebook    ${GIT I}    ${WXYZ EXAMPLES}
    Restart and Run All
    Wait For All Cells To Run    60s
    Capture All Code Cells
    Page Should Not Contain Element    ${JLAB XP STDERR}
    Capture Element Screenshot    ${XP PG BOX}    10-before-initial-commit.png
    Input Text    ${XP PG TEXTAREA}    hello world
    Commit
    Capture Element Screenshot    ${XP PG BOX}    20-after-initial-commit.png
    FOR    ${i}    IN RANGE    ${5}
        Input Text    ${XP PG TEXTAREA}    this is commit #${i}
        Commit    another commit ${i}
        Capture Element Screenshot    ${XP PG BOX}    3${i}-commit.png
    END
    ${canary} =    Set Variable    that's all folks
    Input Text    ${XP PG TEXTAREA}    ${canary}
    Click Element    ${CSS ENABLE TIMETRAVEL}
    Capture Element Screenshot    ${XP PG BOX}    40-before-time-travel.png
    Wait Until Keyword Succeeds    5x    0.5s    Drag And Drop By Offset    ${CSS SLIDER}    -500    0
    Wait Until Keyword Succeeds    5x    0.5s    Git Box Should Not Be    ${canary}
    Capture Element Screenshot    ${XP PG BOX}    50-after-time-travel.png
    [Teardown]    Clean up after Working with file    ${GIT I}.ipynb


*** Keywords ***
Commit
    [Arguments]    ${msg}=${EMPTY}
    Input Text    ${XP COMMIT MSG}    ${msg}
    Wait Until Element Is Enabled    ${XP COMMIT BTN}
    Sleep    0.5s
    Click Element    ${XP COMMIT BTN}
    Wait Until Page Contains    No changes    timeout=10s

Git Box Should Not Be
    [Arguments]    ${canary}
    ${val} =    Get Element Attribute    ${XP PG TEXTAREA}    value
    Should Not Be Equal    ${val}    ${canary}
