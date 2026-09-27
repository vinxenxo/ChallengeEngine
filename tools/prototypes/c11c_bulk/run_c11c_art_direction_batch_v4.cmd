@echo off
setlocal
cd /d "%~dp0..\..\.."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
