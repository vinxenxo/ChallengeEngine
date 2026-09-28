@echo off
setlocal
set C11C_PROJECT_ROOT=%~dp0..
python "%~dp0..\c11c-suite\c11c-producer\main.py" %*
endlocal
