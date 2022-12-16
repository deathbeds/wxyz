*** Settings ***
Documentation       Tests with WXYZ notebooks

Resource            ../_resources/keywords/Browser.robot

Suite Setup         Setup Suite For Screenshots    notebooks

Force Tags          ui:notebook    wxyz:notebooks
