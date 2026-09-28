@echo off
setlocal
call "%~dp0..\c11c-maintenance\run.bat" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
