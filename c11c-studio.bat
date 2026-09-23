@echo off
setlocal enabledelayedexpansion
title C11-C Studio - Control Panel
cd /d "%~dp0"

REM =================== CONFIG ===================
set "BOOTSTRAP=bootstrap_studio.py"
set "TARGET=c11c-studio"
set "PROJECT_ROOT="

REM Optional: pass project root as 1st argument
if not "%~1"=="" set "PROJECT_ROOT=%~1"

REM =================== PYTHON ===================
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY (
  where py >nul 2>nul && set "PY=py -3"
)
if not defined PY (
  echo [!] Python not found on PATH. Install Python 3.10+ first.
  pause
  exit /b 1
)

if not exist "%BOOTSTRAP%" (
  echo [!] %BOOTSTRAP% not found in %CD%
  echo     Put c11c.bat next to the bootstrap script.
  pause
  exit /b 1
)

REM =================== MENU =====================
:menu
cls
echo ============================================================
echo    C11-C STUDIO  -  CONTROL PANEL
echo ============================================================
echo.
echo    Bootstrap : %BOOTSTRAP%
echo    Target    : %TARGET%
if defined PROJECT_ROOT (
  echo    Project   : !PROJECT_ROOT!
) else (
  echo    Project   : ^(not set^)
)
echo.
echo    --- BOOTSTRAP ---------------------------------------
echo    [1] Generate files only          ^(bootstrap^)
echo    [2] Generate + Install deps      ^(bootstrap + venv^)
echo    [3] Generate + Install + Run     ^(all-in-one^)
echo.
echo    --- MANAGE ------------------------------------------
echo    [4] Install deps only            ^(assumes files exist^)
echo    [5] Launch studio
echo    [6] Validate environment         ^(CLI, no GUI^)
echo.
echo    --- REGENERATE --------------------------------------
echo    [7] Regenerate CODE only         ^(overwrite app files^)
echo    [8] Regenerate ENV only          ^(rebuild .venv^)
echo    [9] Regenerate ALL               ^(fresh install^)
echo.
echo    --- UTIL --------------------------------------------
echo    [A] Apply patch files            ^(patch_*.py^)
echo    [V] Verify bootstrap script      ^(py_compile^)
echo    [P] Set project root path
echo    [C] Clean .venv
echo    [O] Open target folder
echo    [Q] Quit
echo.
set /p CHOICE="Choice: "
if /i "!CHOICE!"=="1" goto boot_only
if /i "!CHOICE!"=="2" goto boot_install
if /i "!CHOICE!"=="3" goto boot_run
if /i "!CHOICE!"=="4" goto install_only
if /i "!CHOICE!"=="5" goto run_studio
if /i "!CHOICE!"=="6" goto validate
if /i "!CHOICE!"=="7" goto regen_code
if /i "!CHOICE!"=="8" goto regen_env
if /i "!CHOICE!"=="9" goto regen_all
if /i "!CHOICE!"=="A" goto apply_patches
if /i "!CHOICE!"=="V" goto verify
if /i "!CHOICE!"=="P" goto set_project
if /i "!CHOICE!"=="C" goto clean
if /i "!CHOICE!"=="O" goto open_target
if /i "!CHOICE!"=="Q" goto end
goto menu

REM =================== ACTIONS ==================

:boot_only
echo.
echo [*] Bootstrapping files into "%TARGET%"...
%PY% "%BOOTSTRAP%" --target "%TARGET%"
echo.
pause
goto menu

:boot_install
echo.
echo [*] Bootstrapping + installing deps...
%PY% "%BOOTSTRAP%" --target "%TARGET%" --install
echo.
pause
goto menu

:boot_run
echo.
call :need_project
if errorlevel 1 goto menu
echo [*] Bootstrapping + installing + launching studio...
%PY% "%BOOTSTRAP%" --target "%TARGET%" --install --run --project "!PROJECT_ROOT!"
echo.
pause
goto menu

:install_only
echo.
if not exist "%TARGET%\requirements.txt" (
  echo [!] "%TARGET%\requirements.txt" not found. Run option [1] first.
  pause
  goto menu
)
if not exist "%TARGET%\.venv" (
  echo [*] Creating venv...
  %PY% -m venv "%TARGET%\.venv"
)
echo [*] Installing deps...
"%TARGET%\.venv\Scripts\python.exe" -m pip install --upgrade pip
"%TARGET%\.venv\Scripts\python.exe" -m pip install -r "%TARGET%\requirements.txt"
echo.
pause
goto menu

:run_studio
echo.
if not exist "%TARGET%\main.py" (
  echo [!] "%TARGET%\main.py" not found. Bootstrap first.
  pause
  goto menu
)
set "STUDIO_PY="
if exist "%TARGET%\.venv\Scripts\python.exe" set "STUDIO_PY=%TARGET%\.venv\Scripts\python.exe"
if not defined STUDIO_PY set "STUDIO_PY=%PY%"
if defined PROJECT_ROOT (
  echo [*] Launching with project: !PROJECT_ROOT!
  "!STUDIO_PY!" "%TARGET%\main.py" --project "!PROJECT_ROOT!"
) else (
  echo [*] Launching without project ^(GUI will prompt^)...
  "!STUDIO_PY!" "%TARGET%\main.py"
)
echo.
pause
goto menu

:validate
echo.
call :need_project
if errorlevel 1 goto menu
set "STUDIO_PY="
if exist "%TARGET%\.venv\Scripts\python.exe" set "STUDIO_PY=%TARGET%\.venv\Scripts\python.exe"
if not defined STUDIO_PY set "STUDIO_PY=%PY%"
"!STUDIO_PY!" "%TARGET%\main.py" --project "!PROJECT_ROOT!" --validate
echo.
pause
goto menu

:regen_code
echo.
echo [!] This OVERWRITES all app code files in "%TARGET%".
echo     .venv and local files will be preserved.
echo.
set /p CONFIRM="Continue? (y/N): "
if /i not "!CONFIRM!"=="y" goto menu
%PY% "%BOOTSTRAP%" --target "%TARGET%"
echo.
echo [+] Code regenerated. Re-apply patches with option [A] if needed.
pause
goto menu

:regen_env
echo.
echo [!] This DELETES "%TARGET%\.venv" and reinstalls dependencies.
echo     App code will be preserved.
echo.
set /p CONFIRM="Continue? (y/N): "
if /i not "!CONFIRM!"=="y" goto menu
if exist "%TARGET%\.venv" rmdir /s /q "%TARGET%\.venv"
echo [*] Creating fresh venv...
%PY% -m venv "%TARGET%\.venv"
echo [*] Installing deps...
"%TARGET%\.venv\Scripts\python.exe" -m pip install --upgrade pip
"%TARGET%\.venv\Scripts\python.exe" -m pip install -r "%TARGET%\requirements.txt"
echo.
echo [+] Environment regenerated.
pause
goto menu

:regen_all
echo.
echo [!] FULL REGENERATE:
echo     - DELETE "%TARGET%" completely
echo     - Bootstrap from scratch
echo     - Install deps
echo.
set /p CONFIRM="Type DELETE to confirm: "
if /i not "!CONFIRM!"=="DELETE" goto menu
if exist "%TARGET%" rmdir /s /q "%TARGET%"
%PY% "%BOOTSTRAP%" --target "%TARGET%" --install
echo.
echo [+] Full regenerate complete.
echo     Re-apply patches with option [A] if needed.
pause
goto menu

:apply_patches
echo.
set "FOUND=0"
for %%P in (patch_*.py) do (
  if exist "%%P" (
    set "FOUND=1"
    echo [*] Applying %%P ...
    %PY% "%%P" --target "%TARGET%"
    echo.
  )
)
if "!FOUND!"=="0" (
  echo [i] No patch_*.py files found in %CD%
)
pause
goto menu

:verify
echo.
echo [*] Compile-check %BOOTSTRAP%...
%PY% -m py_compile "%BOOTSTRAP%"
if errorlevel 1 (
  echo [FAIL] Syntax errors found.
) else (
  echo [PASS] %BOOTSTRAP% compiles cleanly.
)
echo.
pause
goto menu

:set_project
echo.
set /p PROJECT_ROOT="Path to ChallengeEngineV01_STATELESS: "
if not exist "!PROJECT_ROOT!" (
  echo [!] Path does not exist: !PROJECT_ROOT!
  set "PROJECT_ROOT="
) else (
  echo [+] Set to: !PROJECT_ROOT!
)
pause
goto menu

:clean
echo.
echo [!] This deletes "%TARGET%\.venv".
set /p CONFIRM="Continue? (y/N): "
if /i not "!CONFIRM!"=="y" goto menu
if exist "%TARGET%\.venv" rmdir /s /q "%TARGET%\.venv"
echo [+] Removed %TARGET%\.venv
pause
goto menu

:open_target
if exist "%TARGET%" (
  explorer "%TARGET%"
) else (
  echo [!] "%TARGET%" does not exist yet.
  pause
)
goto menu

REM =================== HELPERS ==================

:need_project
if defined PROJECT_ROOT exit /b 0
echo Project root not set.
set /p PROJECT_ROOT="Path to ChallengeEngineV01_STATELESS: "
if not exist "!PROJECT_ROOT!" (
  echo [!] Path does not exist: !PROJECT_ROOT!
  set "PROJECT_ROOT="
  exit /b 1
)
exit /b 0

:end
endlocal
exit /b 0