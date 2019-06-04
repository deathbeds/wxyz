*** Settings ***
Library   JupyterLibrary
Resource          ../resources/Browser.robot
Suite Setup       Set Screenshot Directory   ${OUTPUT DIR}${/}01_lab${/}01_basics

*** Test Cases ***
Launcher
    Wait Until Page Contains   Launcher
    Capture Page Screenshot  00_launcher.png
