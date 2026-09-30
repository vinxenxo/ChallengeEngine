@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0create_c11c_freeze_zip.ps1" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
