@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_c11c_art_direction_review_v2.ps1" %*
exit /b %ERRORLEVEL%
