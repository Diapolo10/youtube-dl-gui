@echo off
rem We won't be needing unnecessary output

rem Enable UTF-8 character support
chcp 65001

rem Define current directory path
set mypath=%~dp0

rem Get desktop location
for /f "usebackq tokens=1,2,*" %%B IN (`reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop`) do set DESKTOP=%%D

set install_dir="%systemdrive%\larin_ohjelmat\youtube-dl-gui"
echo %install_dir%
mkdir "%install_dir%"
rem mkdir "%install_dir%\src\dl"
mkdir "%DESKTOP%\ladatut_videot"
if ERRORLEVEL 1 (
    echo.
    ver > nul
)

where /q py

if ERRORLEVEL 1 (
    echo Larin videolataaja vaatii Python-tulkin version 3.6 tai uudemman. Asennathan sen ensin.
    echo Sen voi ladata osoitteesta: https://www.python.org/downloads/release/python-380/
    echo.
    exit /b 0
) else (
    echo Python-asennus havaittu. Mainiota!
    echo.
    call py -m pip install winshell
    if ERRORLEVEL 1 (
        echo Virhe asennettaessa Python-moduulia 'winshell'
        exit /b 0
    ) else (
        echo Python-moduuli winshell asennettu
    )
    echo.
)

if ERRORLEVEL 1 (
    echo Problem!
    echo %ERRORLEVEL%
) else (
    echo No problems detected.
)

rem Create desktop shortcuts
call python -c "import os, winshell; from win32com.client import Dispatch; desktop=winshell.desktop();path=os.path.join(desktop, 'Larin videolataaja.lnk'); wDir=r'C:\larin_ohjelmat\youtube-dl-gui\launcher'; target=f'{wDir}\\launcher.py'; icon=f'{wDir}\\launcher.py'; shell=Dispatch('WScript.Shell'); shortcut=shell.CreateShortcut(path); shortcut.Targetpath=target; shortcut.WorkingDirectory=wDir; shortcut.IconLocation=icon; shortcut.save();"
if ERRORLEVEL 1 (
    echo Ongelma luodessa pikakuvakkeita!
) else (
    echo Pikakuvakkeet luotu työpöydälle
)

echo.
echo Asennus valmis, löydät ohjelman työpöydältäsi!


exit /b 0
