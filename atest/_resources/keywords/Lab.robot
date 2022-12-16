*** Settings ***
Library     OperatingSystem
Library     SeleniumLibrary
Resource    Browser.robot
Resource    ../variables/Lab.robot
Resource    ../variables/Browser.robot


*** Keywords ***
Open JupyterLab
    Set Environment Variable    MOZ_HEADLESS    ${HEADLESS}
    ${firefox} =    Get Firefox Binary
    ${geckodriver} =    Which    geckodriver
    ${service args} =    Create List    --log    info
    Set Global Variable    ${NEXT BROWSER}    ${NEXT BROWSER.__add__(1)}
    Create WebDriver    Firefox
    ...    executable_path=${geckodriver}
    ...    firefox_binary=${firefox}
    ...    service_log_path=${OUTPUT DIR}${/}geckodriver-${PABOT ID}-${NEXT BROWSER}.log
    ...    service_args=${service args}
    Wait Until Keyword Succeeds    3x    5s    Wait For Splash

Wait For Splash
    Go To    ${URL}lab?reset&token=${TOKEN}
    Set Window Size    1920    1080
    Wait Until Page Contains Element    ${SPLASH}    timeout=30s
    Wait Until Page Does Not Contain Element    ${SPLASH}    timeout=10s
    Execute Javascript    window.onbeforeunload \= function (){}

Try to Close All Tabs
    Wait Until Keyword Succeeds    5x    50ms    Close All Tabs

Close All Tabs
    Accept Default Dialog Option
    Lab Command    Close All Tabs
    Accept Default Dialog Option

Wait For All Cells To Run
    [Arguments]    ${timeout}=10s
    Wait Until Element Does Not Contain    ${JLAB XP LAST CODE PROMPT}    [*]:    timeout=${timeout}
    Wait Until Element is Visible    ${JLAB XP KERNEL IDLE}    timeout=${timeout}

Click JupyterLab Menu
    [Documentation]    Click a top-level JupyterLab menu bar item with by ``label``,
    ...    e.g. File, Help, etc.
    [Arguments]    ${label}
    ${xpath} =    Set Variable    ${JLAB XP TOP}${JLAB XP MENU LABEL}\[text() = '${label}']
    Wait Until Page Contains Element    ${xpath}
    Mouse Over    ${xpath}
    Click Element    ${xpath}

Click JupyterLab Menu Item
    [Documentation]    Click a currently-visible JupyterLab menu item by ``label``.
    [Arguments]    ${label}
    ${item} =    Set Variable    ${JLAB XP MENU ITEM LABEL}\[text() = '${label}']
    Wait Until Page Contains Element    ${item}
    Mouse Over    ${item}
    Click Element    ${item}

Open With JupyterLab Menu
    [Documentation]    Click into a ``menu``, then a series of ``submenus``
    [Arguments]    ${menu}    @{submenus}
    Click JupyterLab Menu    ${menu}
    FOR    ${submenu}    IN    @{submenus}
        Click JupyterLab Menu Item    ${submenu}
    END

Ensure File Browser is Open
    ${sel} =    Set Variable    css:.lm-TabBar-tab[data-id="filebrowser"]:not(.lm-mod-current)
    ${els} =    Get WebElements    ${sel}
    IF    ${els.__len__()}    Click Element    ${sel}

Ensure Sidebar Is Closed
    [Arguments]    ${side}=left
    ${els} =    Get WebElements    css:#jp-${side}-stack
    IF    ${els.__len__()}
        Click Element    css:.jp-mod-${side} .lm-TabBar-tab.lm-mod-current
    END

Open Context Menu for File
    [Arguments]    ${file}
    Ensure File Browser is Open
    Click Element    css:button[title="Refresh File List"]
    ${selector} =    Set Variable    xpath://span[@class='jp-DirListing-itemText']/span\[text() = '${file}']
    Wait Until Page Contains Element    ${selector}
    Open Context Menu    ${selector}

Rename Jupyter File
    [Arguments]    ${old}    ${new}
    Open Context Menu for File    ${old}
    Mouse Over    ${MENU RENAME}
    Click Element    ${MENU RENAME}
    Press Keys    None    CTRL+a
    Press Keys    None    ${new}
    Press Keys    None    RETURN

Input Into Dialog
    [Arguments]    ${text}
    Wait For Dialog
    Click Element    ${DIALOG INPUT}
    Input Text    ${DIALOG INPUT}    ${text}
    Click Element    ${DIALOG ACCEPT}

Open ${file} in ${editor}
    Open Context Menu for File    ${file}
    Mouse Over    ${MENU OPEN WITH}
    Wait Until Page Contains Element    ${editor}
    Mouse Over    ${editor}
    Click Element    ${editor}

Clean Up After Working With File
    [Arguments]    ${file}
    Remove File    ${OUTPUT DIR}${/}home${/}${file}
    Reset Application State

Wait For Dialog
    Wait Until Page Contains Element    ${DIALOG WINDOW}    timeout=180s

Gently Reset Workspace
    Try to Close All Tabs

Enter Cell Editor
    [Arguments]    ${cell_nr}    ${line}=1
    Click Element    css:.jp-Cell:nth-child(${cell_nr}) .CodeMirror-line:nth-child(${line})
    Wait Until Page Contains Element    css:.jp-Cell:nth-child(${cell_nr}) .CodeMirror-focused

Place Cursor In Cell Editor At
    [Arguments]    ${cell_nr}    ${line}    ${character}
    Enter Cell Editor    ${cell_nr}    ${line}
    Execute JavaScript
    ...    return document.querySelector('.jp-Cell:nth-child(${cell_nr}) .CodeMirror').CodeMirror.setCursor({line: ${line} - 1, ch: ${character}})

Enter File Editor
    Click Element    css:.jp-FileEditor .CodeMirror
    Wait Until Page Contains Element    css:.jp-FileEditor .CodeMirror-focused

Place Cursor In File Editor At
    [Arguments]    ${line}    ${character}
    Enter File Editor
    Execute JavaScript
    ...    return document.querySelector('.jp-FileEditor .CodeMirror').CodeMirror.setCursor({line: ${line} - 1, ch: ${character}})

Open Context Menu Over
    [Arguments]    ${sel}
    Wait Until Keyword Succeeds    10 x    0.1 s    Mouse Over    ${sel}
    Wait Until Keyword Succeeds    10 x    0.1 s    Open Context Menu    ${sel}

Open File
    [Arguments]    ${file}    ${editor}=${MENU EDITOR}
    ${parent}    ${name} =    Split Path    ${file}
    Copy File    ${file}    ${OUTPUT DIR}${/}home${/}${name}
    Open ${name} in ${editor}
    Capture Page Screenshot    00-opened.png

Open in Advanced Settings
    [Arguments]    ${plugin id}
    Lab Command    Advanced Settings Editor
    ${sel} =    Set Variable    css:[data-id="${plugin id}"]
    Wait Until Page Contains Element    ${sel}
    Click Element    ${sel}
    Wait Until Page Contains    System Defaults

Set Editor Content
    [Arguments]    ${text}    ${css}=${EMPTY}
    Execute JavaScript    return document.querySelector('${css} .CodeMirror').CodeMirror.setValue(`${text}`)

Get Editor Content
    [Arguments]    ${css}=${EMPTY}
    ${content} =    Execute JavaScript    return document.querySelector('${css} .CodeMirror').CodeMirror.getValue()
    RETURN    ${content}

Clean Up After Working with File and Settings
    [Arguments]    ${file}
    Clean Up After Working With File    ${file}
    Reset Plugin Settings

Close JupyterLab
    Close All Browsers

Open Command Palette
    Press Keys    id:main    ${ACCEL}+SHIFT+c
    Wait Until Page Contains Element    ${CMD PALETTE INPUT}
    Wait Until Keyword Succeeds    5x    0.5s    Click Element    ${CMD PALETTE INPUT}

Enter Command Name
    [Arguments]    ${cmd}
    Open Command Palette
    Input Text    ${CMD PALETTE INPUT}    ${cmd}

Lab Command
    [Arguments]    ${cmd}
    Enter Command Name    ${cmd}
    Wait Until Page Contains Element    ${CMD PALETTE ITEM ACTIVE}
    Click Element    ${CMD PALETTE ITEM ACTIVE}

Capture All Code Cells
    [Arguments]    ${prefix}=${EMPTY}    ${timeout}=30s
    ${cells} =    Get WebElements    ${JLAB XP CODE CELLS}
    Lab Command    Expand All Code
    Ensure Sidebar Is Closed
    FOR    ${idx}    ${cell}    IN ENUMERATE    @{cells}
        ${sel} =    Set Variable    ${JLAB XP CODE CELLS}\[${idx.__add__(1)}]
        Run Keyword and Ignore Error    Wait Until Element does not contain    ${sel}    [*]:    timeout=${timeout}
        Capture Element Screenshot    ${sel}    ${prefix}cell-${idx.__repr__().zfill(3)}.png
    END

Restart and Run All
    Lab Command    Clear All Outputs
    Lab Command    Restart Kernel and Run All Cells
    Accept Default Dialog Option
    Ensure Sidebar Is Closed
    Wait Until Keyword Succeeds    10x    10s
    ...    Wait Until Element Contains    ${JLAB XP LAST CODE PROMPT}    [*]:

Reset Application State
    Try to Close All Tabs
    Accept Default Dialog Option
    Ensure All Kernels Are Shut Down
    Lab Command    Reset Application State
    Wait Until Keyword Succeeds    3x    5s    Wait For Splash

Accept Default Dialog Option
    [Documentation]    Accept a dialog, if it exists
    ${el} =    Get WebElements    ${CSS DIALOG OK}
    IF    ${el.__len__()}    Click Element    ${CSS DIALOG OK}

Ensure All Kernels Are Shut Down
    Enter Command Name    Shut Down All Kernels
    ${els} =    Get WebElements    ${CMD PALETTE ITEM ACTIVE}
    IF    ${els.__len__()}    Click Element    ${CMD PALETTE ITEM ACTIVE}
    ${accept} =    Set Variable    css:.jp-mod-accept.jp-mod-warn
    IF    ${els.__len__()}    Wait Until Page Contains Element    ${accept}
    IF    ${els.__len__()}    Click Element    ${accept}
