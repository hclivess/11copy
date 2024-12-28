@echo off
echo Building 11copy with Nuitka...

REM Install required packages if not present
pip install nuitka
pip install customtkinter
pip install zstandard

REM Clean previous builds
if exist "11copy.dist" rd /s /q "11copy.dist"
if exist "11copy.build" rd /s /q "11copy.build"
if exist "11copy.exe" del /f /q "11copy.exe"

REM Compile with Nuitka
python -m nuitka ^
    --standalone ^
    --enable-plugin=tk-inter ^
    --windows-disable-console ^
    --windows-icon-from-ico=icon.ico ^
    --include-module=customtkinter ^
    --include-package=darkdetect ^
    --include-package-data=customtkinter ^
    --output-dir=build ^
    --assume-yes-for-downloads ^
    --windows-company-name=11copy ^
    --windows-product-name=11copy ^
    --windows-file-version=1.0.0 ^
    --windows-product-version=1.0.0 ^
    --onefile ^
    11copy.py

echo Build complete!
pause