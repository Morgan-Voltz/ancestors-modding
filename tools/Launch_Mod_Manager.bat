@echo off
title Ancestors Difficulty Mod Manager
echo ============================================
echo   Ancestors — Difficulty Mod Manager
echo   By DaddyOurs
echo ============================================
echo.

:: Try Python from PATH
where python >/dev/null 2>&1
if %ERRORLEVEL% equ 0 (
    python "%~dp0AncestorsDifficultyMod.py"
    if %ERRORLEVEL% equ 0 goto :end
)

:: Try python3
where python3 >/dev/null 2>&1
if %ERRORLEVEL% equ 0 (
    python3 "%~dp0AncestorsDifficultyMod.py"
    if %ERRORLEVEL% equ 0 goto :end
)

:: Try common Python installations
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Microsoft\WindowsApps\python3.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
) do (
    if exist %%P (
        echo Found Python at %%P
        %%P "%~dp0AncestorsDifficultyMod.py"
        if %ERRORLEVEL% equ 0 goto :end
    )
)

echo.
echo ERROR: Python not found!
echo.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause

:end
