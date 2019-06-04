*** Settings ***
Library   JupyterLibrary
Resource          ../resources/Browser.robot
Suite Setup       Set Screenshot Directory   ${OUTPUT DIR}${/}01_lab${/}02_widgets

*** Test Cases ***
Widgets
    Wait Until Page Contains   Launcher
