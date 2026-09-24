@echo off
setlocal
set "C11C_PROJECT_ROOT=%~dp0.."
if not "%~1"=="" if /I "%~1"=="--project" if not "%~2"=="" set "C11C_PROJECT_ROOT=%~2"
python main.py
endlocal
