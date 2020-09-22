*** Settings ***
Suite Setup       Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}smoke
Resource          Keywords.robot

*** Test Cases ***
Lab Loads
    Capture Page Screenshot    00-smoke.png
