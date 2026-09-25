@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_c11c_full_art_direction_corpus.ps1" %*
set "RC=%ERRORLEVEL%"
echo.
echo C11-C full corpus runner exit code: %RC%
exit /b %RC%
