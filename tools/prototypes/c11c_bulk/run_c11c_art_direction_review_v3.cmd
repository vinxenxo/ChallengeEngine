@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_c11c_art_direction_review_v3.ps1" %*
exit /b %ERRORLEVEL%
