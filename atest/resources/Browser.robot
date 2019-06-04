*** Settings ***
Library  JupyterLibrary

*** Keywords ***
Open WXYZ Lab
  Set Tags   browser:${BROWSER}
  Open JupyterLab    browser=${BROWSER}
  Set Window Size   1024  768
  Wait Until Keyword Succeeds    5x    2s    Execute JupyterLab Command    Reset Application State

Clean Up WXYZ Lab
  Run keyword And Ignore Error   Execute JupyterLab Command    Save Notebook
  Wait Until Keyword Succeeds    5x    2s    Execute JupyterLab Command    Reset Application State
  Run keyword And Ignore Error    Handle Alert    timeout=1s
  Close Browser
