@echo off
setlocal
set "kotomi_python=python"
if exist "%~dp0.venv\Scripts\python.exe" set "kotomi_python=%~dp0.venv\Scripts\python.exe"
if defined VIRTUAL_ENV set "kotomi_python=%VIRTUAL_ENV%\Scripts\python.exe"
"%kotomi_python%" "%~dp0tools\diagnostics\data_audit.py" %*
set "kotomi_result=%errorlevel%"
echo %cmdcmdline% | findstr /i /c:" /c " >nul
if not errorlevel 1 if not defined CI pause
exit /b %kotomi_result%
