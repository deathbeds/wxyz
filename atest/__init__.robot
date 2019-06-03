*** Settings ***
Library           JupyterLibrary
Resource          ./Launch.robot
Suite Setup       Start New WXYZ Lab Server
Suite Teardown    Terminate All Jupyter Servers
