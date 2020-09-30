*** Settings ***
Suite Setup       Setup Suite For Screenshots    smoke
Resource          Keywords.robot

*** Test Cases ***
Lab Loads
    Capture Page Screenshot    00-smoke.png
