@echo off
setlocal
pushd "%~dp0"
set "kotomi_python=python"
if exist ".venv\Scripts\python.exe" set "kotomi_python=%CD%\.venv\Scripts\python.exe"
if defined VIRTUAL_ENV set "kotomi_python=%VIRTUAL_ENV%\Scripts\python.exe"
"%kotomi_python%" "%~dp0tools\run_tests.py" %*
set "kotomi_result=%errorlevel%"
echo Test runner finished with exit code %kotomi_result%.
popd
echo %cmdcmdline% | findstr /i /c:" /c " >nul
if not errorlevel 1 if not defined CI pause
exit /b %kotomi_result%
