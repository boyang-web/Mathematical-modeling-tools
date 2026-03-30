@echo off
setlocal

cd /d "%~dp0"

set "DIST_DIR=%~dp0dist\math-modeling-toolkit"
set "RELEASE_DIR=%~dp0release"
set "RELEASE_ZIP=%RELEASE_DIR%\math-modeling-toolkit-win.zip"
set "LAUNCHER_BAT=%DIST_DIR%\start_toolkit.bat"

set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
if exist "%PYTHON_EXE%" goto python_found

set "PYTHON_EXE=%~dp0.venv\bin\python.exe"
if exist "%PYTHON_EXE%" goto python_found

set "PYTHON_EXE=python"

:python_found
echo Using Python interpreter: %PYTHON_EXE%

echo [1/5] Checking PyInstaller...
"%PYTHON_EXE%" -m PyInstaller --version >nul 2>nul
if errorlevel 1 goto install_pyinstaller
echo PyInstaller is already available.
goto pyinstaller_ready

:install_pyinstaller
echo PyInstaller is not installed. Trying to install it now...
"%PYTHON_EXE%" -m pip install pyinstaller
if errorlevel 1 goto pyinstaller_install_failed

:pyinstaller_ready

echo [2/5] Cleaning old build output...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist release rmdir /s /q release
if exist launch.spec del /q launch.spec

echo [3/5] Building distributable folder...
"%PYTHON_EXE%" -m PyInstaller --noconfirm --clean --onedir --console --name math-modeling-toolkit --collect-all streamlit --collect-all pandas --collect-all numpy --collect-all openpyxl --collect-all xlrd --add-data "app;app" --add-data "core;core" --add-data "models;models" launch.py
if errorlevel 1 goto build_failed

echo [4/5] Writing distribution helper files...
if not exist "%DIST_DIR%" (
  echo Build output not found: %DIST_DIR%
  goto build_failed
)

> "%LAUNCHER_BAT%" echo @echo off
>> "%LAUNCHER_BAT%" echo setlocal
>> "%LAUNCHER_BAT%" echo cd /d "%%~dp0"
>> "%LAUNCHER_BAT%" echo start "" "math-modeling-toolkit.exe"

copy /Y README.md "%DIST_DIR%\README.md" >nul

echo [5/5] Creating zip package...
mkdir "%RELEASE_DIR%"
powershell -NoProfile -Command "Compress-Archive -Path '%DIST_DIR%\*' -DestinationPath '%RELEASE_ZIP%' -Force"
if errorlevel 1 goto build_failed

echo.
echo Build finished.
echo Folder package: %DIST_DIR%
echo Zip package: %RELEASE_ZIP%
echo You can send the whole folder or the zip file to testers.
pause
exit /b 0

:pyinstaller_install_failed
echo.
echo Failed to install PyInstaller automatically.
echo Please check your network or install it manually with:
echo %PYTHON_EXE% -m pip install pyinstaller
pause
exit /b 1

:build_failed
echo.
echo Build failed. Please review the error messages above.
pause
exit /b 1
