:: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
:: !!!!!!!!!!!!! [This script is intended for Windows OS ONLY] !!!!!!!!!!!!!!!
:: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
:: ===========================================================================
:: This batch file is used to install the Python packages listed in requirements.txt 
:: Make sure to run this script in the same directory as requirements.txt
:: It uses pip to install the packages listed in requirements.txt
:: ===========================================================================

@echo off

REM ORIGINAL Code Page is 437
for /f "tokens=2 delims=:" %%G in ('chcp') do set "originalCP=%%G"
chcp 65001 >nul 

title REQUIREMENTS INSTALLER
cls


REM Check if requirements.txt exists
IF NOT EXIST requirements.txt (
    powershell -NoProfile -Command ^
        "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' `requirements.txt` not found!'"
    powershell -NoProfile -Command ^
        "Write-Host '▶▶' -ForegroundColor Blue -NoNewline; Write-Host ' Please make sure you are in the correct directory.'"
    pause
    goto :exit_clean
) ELSE (
    powershell -NoProfile -Command ^
        "Write-Host '[√]' -ForegroundColor Green -NoNewline; Write-Host ' `requirements.txt`' -ForegroundColor Yellow -NoNewLine; Write-Host ' FOUND:' -NoNewLine; Write-Host ' "%~dp0requirements.txt"' -ForegroundColor Cyan"
    echo.
)

REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    powershell -NoProfile -Command ^
        "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Python is not installed or not added to PATH.'"
    powershell -NoProfile -Command ^
        "Write-Host '[>>]' -ForegroundColor Blue -NoNewline; Write-Host ' Please install Python and add it to your PATH.'"
    powershell -NoProfile -Command ^
        "Write-Host '[#]' -ForegroundColor Yellow -NoNewline; Write-Host ' Opening a tutorial on how to add Python to your PATH...'"
    start https://phoenixnap.com/kb/add-python-to-path
    pause
    goto :exit_clean
) ELSE (
    powershell -NoProfile -Command ^
        "Write-Host '[√]' -ForegroundColor Green -NoNewline; Write-Host ' Python is installed.'"
    echo.
)

REM Check if pip is installed
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    powershell -NoProfile -Command ^
        "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Pip is not installed or not added to PATH.'"
    powershell -NoProfile -Command ^
        "Write-Host '[#]' -ForegroundColor Yellow -NoNewline; Write-Host ' Attempting to install pip for you now...'"
    goto :install_pip
) ELSE (
    powershell -NoProfile -Command ^
        "Write-Host '[√]' -ForegroundColor Green -NoNewline; Write-Host ' Pip is installed.'"
    echo.
    goto :install_requirements
)


:install_requirements
REM Install the required packages
powershell -NoProfile -Command ^
        "Write-Host '=========================================================' -ForegroundColor Yellow; Write-Host '[#]' -ForegroundColor Yellow -NoNewline; Write-Host ' Installing required packages from requirements.txt...'; Write-Host '=========================================================' -ForegroundColor Yellow"
echo.
pip install -r requirements.txt
echo.
IF ERRORLEVEL 1 (
    powershell -NoProfile -Command ^
        "Write-Host '=============================================' -ForegroundColor Magenta; Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Failed to install required packages. Please try to install them manually.'; Write-Host '=============================================' -ForegroundColor Magenta"
    echo.
    set /p void_value=Press any key to close command prompt...
    goto :exit_clean
) ELSE (
    powershell -NoProfile -Command ^
        "Write-Host '=============================================' -ForegroundColor Magenta; Write-Host '[√]' -ForegroundColor Green -NoNewline; Write-Host ' Required packages installed successfully.'; Write-Host '=============================================' -ForegroundColor Magenta"
    echo.
    set /p void_value=Press any key to close command prompt...
    goto :exit_clean
)


:exit_clean
chcp %originalCP% >nul
exit /b

:install_pip
powershell -NoProfile -Command ^
    "Write-Host '[#]' -ForegroundColor Yellow -NoNewline; Write-Host ' Installing pip...'"
powershell -Command "Start-Process cmd -ArgumentList '/c python -m ensurepip' -Verb RunAs"
IF ERRORLEVEL 1 (
    powershell -NoProfile -Command ^
        "Write-Host '[X]' -ForegroundColor Red -NoNewline; Write-Host ' Failed to install pip. Please try to install it manually.'"
    pause
    goto :exit_clean
)
powershell -NoProfile -Command ^
    "Write-Host '[√]' -ForegroundColor Green -NoNewline; Write-Host ' Pip installed successfully.'"
goto :install_requirements