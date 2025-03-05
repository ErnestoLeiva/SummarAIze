:: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
:: !!!!!!!!!!!!! [This script is intended for Windows OS ONLY] !!!!!!!!!!!!!!!
:: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
:: ===========================================================================
:: This script is used to update the version number in package.json using npm version
:: It offers options for patch, minor, major, or custom updates.
:: Make sure to run this script in the same directory as package.json.
:: ===========================================================================

@echo off
title VERSION UPDATER
cls

REM Check if package.json exists
IF NOT EXIST package.json (
    powershell -NoProfile -Command ^
        "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' `package.json` not found!'"
    powershell -NoProfile -Command ^
        "Write-Host '[>>]' -ForegroundColor Blue -NoNewline; Write-Host ' Please make sure you are in the correct directory.'"
    pause
    goto :exit_clean
)


REM Ask user for update type
:option_selection
powershell -NoProfile -Command "Write-Host 'Choose the type of version update:' -ForegroundColor Cyan; Write-Host '  1. ' -NoNewline; Write-Host 'Patch update' -ForegroundColor Green -NoNewline; Write-Host ' (npm version patch|E.G. 1.2.3 -> 1.2.4)' -ForegroundColor DarkGray; Write-Host '  2. ' -NoNewline; Write-Host 'Minor update' -ForegroundColor Yellow -NoNewline; Write-Host ' (npm version minor|E.G. 1.2.3 -> 1.3.0)' -ForegroundColor DarkGray; Write-Host '  3. ' -NoNewline; Write-Host 'Major update' -ForegroundColor Red -NoNewline; Write-Host ' (npm version major|E.G. 1.2.3 -> 2.0.0)' -ForegroundColor DarkGray; Write-Host '  4. ' -NoNewline; Write-Host 'Custom update' -ForegroundColor Cyan -NoNewline; Write-Host ' (npm version <custom version>|E.G. 1.2.3 -> 3.1.2)' -ForegroundColor DarkGray; Write-Host '  5. ' -NoNewline; Write-Host 'Cancel' -ForegroundColor Magenta -NoNewline; Write-Host ' (exit)' -ForegroundColor DarkGray"
echo ------------------------------------------
set /p updateType=Enter your choice (1/2/3/4/5): 
echo.


REM Branch based on user input
if "%updateType%"=="1" goto patch_update
if "%updateType%"=="2" goto minor_update
if "%updateType%"=="3" goto major_update
if "%updateType%"=="4" goto custom_update
if "%updateType%"=="5" goto exit_clean

powershell -NoProfile -Command ^
        "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Invalid choice. You must choose an option from the list of choices.'"
echo.
set /p void_value=Press any key to try again... (or Ctrl+C to exit)
cls
goto :option_selection



REM ======================================================================
REM ============================= MAIN LOGIC =============================
REM ======================================================================



REM ------------------------------
REM PATCH UPDATE VERSION E.G. 1.2.3 -> 1.2.4
:patch_update
powershell -NoProfile -Command "Write-Host '[!]' -ForegroundColor Green -NoNewline; Write-Host ' Applying patch version update...'"
echo.

REM run using /c so that it terminates its own process, redirecting both STDOUT and STDERR to temp.txt 
cmd /c "npm version patch > temp.txt 2>&1"

REM Check for errors in the output
for /f "delims=" %%a in ('type temp.txt ^| find /c /i "err"') do set err=%%a

REM Check if the error level is greater than 0 and handle accordingly
IF %err% GTR 0 (
    powershell -NoProfile -Command "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Failed to update the version number.'"
    echo.
    for /f "usebackq delims=" %%l in ("temp.txt") do (
        powershell -NoProfile -Command "Write-Host '%%l' -ForegroundColor Red"
    )
    echo.
    del temp.txt
    pause
    goto :exit_clean
) ELSE (
    REM No errors found; capture the npm command output (the new version) from temp.txt
    for /F "delims=" %%b in (temp.txt) do set "NEW_VERSION=%%b"
    del temp.txt
)
goto show_version



REM ------------------------------
REM MINOR UPDATE VERSION E.G. 1.2.3 -> 1.3.0
:minor_update
powershell -NoProfile -Command "Write-Host '[!]' -ForegroundColor Green -NoNewline; Write-Host ' Applying minor version update...'"
echo.

REM run using /c so that it terminates its own process, redirecting both STDOUT and STDERR to temp.txt 
cmd /c "npm version minor > temp.txt 2>&1"

REM Check for errors in the output
for /f "delims=" %%a in ('type temp.txt ^| find /c /i "err"') do set err=%%a

REM Check if the error level is greater than 0 and handle accordingly
IF %err% GTR 0 (
    powershell -NoProfile -Command "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Failed to update the version number.'"
    echo.
    for /f "usebackq delims=" %%l in ("temp.txt") do (
        powershell -NoProfile -Command "Write-Host '%%l' -ForegroundColor Red"
    )
    echo.
    del temp.txt
    pause
    goto :exit_clean
) ELSE (
    REM No errors found; capture the npm command output (the new version) from temp.txt
    for /F "delims=" %%b in (temp.txt) do set "NEW_VERSION=%%b"
    del temp.txt
)
goto show_version


REM ------------------------------
REM MAJOR UPDATE VERSION E.G. 1.2.3 -> 2.0.0
:major_update
powershell -NoProfile -Command "Write-Host '[!]' -ForegroundColor Green -NoNewline; Write-Host ' Applying major version update...'"
echo.

REM run using /c so that it terminates its own process, redirecting both STDOUT and STDERR to temp.txt 
cmd /c "npm version major > temp.txt 2>&1"

REM Check for errors in the output
for /f "delims=" %%a in ('type temp.txt ^| find /c /i "err"') do set err=%%a

REM Check if the error level is greater than 0 and handle accordingly
IF %err% GTR 0 (
    powershell -NoProfile -Command "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Failed to update the version number.'"
    echo.
    for /f "usebackq delims=" %%l in ("temp.txt") do (
        powershell -NoProfile -Command "Write-Host '%%l' -ForegroundColor Red"
    )
    echo.
    del temp.txt
    pause
    goto :exit_clean
) ELSE (
    REM No errors found; capture the npm command output (the new version) from temp.txt
    for /F "delims=" %%b in (temp.txt) do set "NEW_VERSION=%%b"
    del temp.txt
)
goto show_version


REM ------------------------------
REM CUSTOM UPDATE VERSION E.G. 1.2.3 -> custom (e.g., 3.1.2)
:custom_update
setlocal EnableDelayedExpansion
set /p customVersion=Enter the custom version (e.g., 3.1.2): 
echo.

REM Trim leading/trailing whitespace by reassigning the variable via a for /f.
REM This handles any accidental spaces or carriage returns.
for /f "tokens=1* delims=" %%A in ("!customVersion!") do set "customVersion=%%~A"

REM Validate the custom version format using regex in PowerShell (more reliabler efor some reason)
powershell -NoProfile -Command ^
  "if ('%customVersion%' -match '^[0-9]+\.[0-9]+\.[0-9]+$') { exit 0 } else { exit 1 }"
IF ERRORLEVEL 1 (
    powershell -NoProfile -Command "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Invalid version format. Please use the format X.Y.Z (e.g., 3.1.2).'"
    echo.
    set /p void_value=Press any key to try again...
    cls
    goto :custom_update
)
endlocal & set "customVersion=%customVersion%" 

powershell -NoProfile -Command "Write-Host '[!]' -ForegroundColor Green -NoNewline; Write-Host ' Applying custom version update...'"
echo.

REM run using /c so that it terminates its own process, redirecting both STDOUT and STDERR to temp.txt 
cmd /c "npm version %customVersion% > temp.txt 2>&1"

REM Check for errors in the output
for /f "delims=" %%a in ('type temp.txt ^| find /c /i "err"') do set err=%%a

REM Check if the error level is greater than 0 and handle accordingly
IF %err% GTR 0 (
    powershell -NoProfile -Command "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Failed to update the version number.'"
    echo.
    for /f "usebackq delims=" %%l in ("temp.txt") do (
        powershell -NoProfile -Command "Write-Host '%%l' -ForegroundColor Red"
    )
    echo.
    del temp.txt
    pause
    goto :exit_clean
) ELSE (
    REM No errors found; capture the npm command output (the new version) from temp.txt
    for /F "delims=" %%b in (temp.txt) do set "NEW_VERSION=%%b"
    del temp.txt
)
goto show_version


REM ------------------------------
REM SHOW THE NEW VERSION NUMBER 
:show_version
IF "%NEW_VERSION%"=="" (
    powershell -NoProfile -Command "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' No version number returned.'"
) ELSE (
    powershell -NoProfile -Command "Write-Host '[!]' -ForegroundColor Green -NoNewline; Write-Host ' Version number updated successfully.'"
    echo.
    echo New version: %NEW_VERSION%
)
pause

:exit_clean
endlocal
exit /b
