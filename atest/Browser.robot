*** Settings ***
Library   JupyterLibrary

*** Keywords ***
Open WXYZ Lab
  [Arguments]  ${browser}
  Set Tags   browser:${browser}
  Open JupyterLab    browser=${browser}
