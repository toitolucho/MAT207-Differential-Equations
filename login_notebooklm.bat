@echo off
title NotebookLM Login
echo ========================================================
echo  NotebookLM Authentication
echo ========================================================
echo.
echo Launching browser for Google sign-in...
echo Once the NotebookLM page loads, please sign in to your Google account.
echo.
nlm login --storage protected
echo.
echo ========================================================
if %ERRORLEVEL% equ 0 (
    echo Login successful! Listing your notebooks:
    echo.
    nlm notebook list
) else (
    echo An issue occurred during login.
)
echo ========================================================
echo.
pause
