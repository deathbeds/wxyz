*** Settings ***
Library           JupyterLibrary
Resource          ./resources/Launch.robot
Suite Setup       Start New WXYZ Lab Server
Suite Teardown    Terminate All Jupyter Servers
Force Tags        os:${OS}
