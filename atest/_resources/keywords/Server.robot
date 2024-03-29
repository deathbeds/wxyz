*** Settings ***
Library     OperatingSystem
Library     Process
Library     String
Resource    Lab.robot
Resource    Browser.robot
Resource    Meta.robot
Resource    ../variables/Server.robot
Library     ../../_libraries/Ports.py


*** Keywords ***
Setup Server and Browser
    ${port} =    Get Unused Port
    Run Keyword and Ignore Error    Tag for Pabot
    Set Global Variable    ${PORT}    ${port}
    Set Global Variable    ${URL}    http://localhost:${PORT}${URL PREFIX}
    ${accel} =    Evaluate    "COMMAND" if "${OS}" == "Darwin" else "CTRL"
    Set Global Variable    ${ACCEL}    ${accel}
    ${token} =    Generate Random String
    Set Global Variable    ${TOKEN}    ${token}
    ${home} =    Set Variable    ${OUTPUT DIR}${/}home
    ${root} =    Normalize Path    ${OUTPUT DIR}${/}..${/}..${/}..
    Create Directory    ${home}
    Create Notebok Server Config    ${home}
    Initialize User Settings
    ${cmd} =    Create Lab Launch Command    ${root}
    Set Screenshot Directory    ${SCREENS ROOT}
    Set Global Variable    ${NEXT LAB}    ${NEXT LAB.__add__(1)}
    Set Global Variable    ${LAB LOG}    ${OUTPUT DIR}${/}lab-${PABOT ID}-${NEXT LAB}.log
    Set Global Variable    ${PREVIOUS LAB LOG LENGTH}    0
    Set Environment Variable    JUPYTER_CONFIG_DIR    ${home}
    ${server} =    Start Process    ${cmd}    shell=yes    env:HOME=${home}    cwd=${home}    stdout=${LAB LOG}
    ...    stderr=STDOUT
    Set Global Variable    ${SERVER}    ${server}
    Open JupyterLab
    ${script} =    Get Element Attribute    id:jupyter-config-data    innerHTML
    ${config} =    Evaluate    __import__("json").loads(r"""${script}""")
    Set Global Variable    ${PAGE CONFIG}    ${config}
    Set Global Variable    ${LAB VERSION}    ${config["appVersion"]}

Create Lab Launch Command
    [Documentation]    Create a JupyterLab CLI shell string, escaping for traitlets
    [Arguments]    ${root}
    ${WORKSPACES DIR} =    Set Variable    ${OUTPUT DIR}${/}workspaces
    ${app args} =    Set Variable
    ...    --no-browser --debug --ServerApp.base_url\='${URL PREFIX}' --port\=${PORT} --ServerApp.token\='${TOKEN}' --ExtensionApp.open_browser\=False --ServerApp.open_browser\=False
    ${path args} =    Set Variable
    ...    --LabApp.user_settings_dir\='${SETTINGS DIR.replace('\\', '\\\\')}' --LabApp.workspaces_dir\='${WORKSPACES DIR.replace('\\', '\\\\')}'
    ${cmd} =    Set Variable
    ...    jupyter-lab ${app args} ${path args}
    RETURN    ${cmd}

Create Notebok Server Config
    [Documentation]    Copies in jupyter server config file to disable npm/build checks
    [Arguments]    ${home}
    Copy File    ${FIXTURES}${/}${JPSERVER CONF}    ${home}${/}${JPSERVER CONF}

Initialize User Settings
    Set Suite Variable    ${SETTINGS DIR}    ${OUTPUT DIR}${/}user-settings    children=${True}
    Create File    ${SETTINGS DIR}${/}@jupyterlab${/}codemirror-extension${/}commands.jupyterlab-settings
    ...    {"styleActiveLine": true}
    Create File    ${SETTINGS DIR}${/}@jupyterlab${/}extensionmanager-extension${/}plugin.jupyterlab-settings
    ...    {"enabled": false}
    Create File
    ...    ${SETTINGS DIR}${/}@jupyterlab${/}apputils-extension${/}palette.jupyterlab-settings
    ...    {"modal": false}

Tear Down Everything
    Close All Browsers
    Evaluate    __import__("urllib.request").request.urlopen("${URL}api/shutdown?token=${TOKEN}", data=[])
    Wait For Process    ${SERVER}    timeout=30s
    Terminate All Processes
    Terminate All Processes    kill=${True}
