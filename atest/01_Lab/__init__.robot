*** Settings ***
Library           JupyterLibrary
Resource          ../resources/Browser.robot
Test Setup        Open WXYZ Lab
Test Teardown     Clean Up WXYZ Lab
