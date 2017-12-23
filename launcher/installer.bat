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

where /q python

if ERRORLEVEL 1 (
    echo Larin videolataaja vaatii Python-tulkin version 3.6 tai uudemman. Asennathan sen ensin.
    echo Asennuksen aikana tulee eteen pieni ruutu jonka vieressä lukee "Include in PATH" tai jotain. Varmista että tässä ruudussa on oikeinmerkki!
    echo Sen voi ladata osoitteesta: https://www.python.org/downloads/
    echo.
    exit /b 0
) else (
    echo Python-asennus havaittu. Mainiota!
    echo.
    call pip install winshell
    if ERRORLEVEL 1 (
        echo Virhe asennettaessa Python-moduulia 'winshell'
        exit /b 0
    ) else (
        echo Python-moduuli winshell asennettu
    )
    echo.
)

rem Check if git is installed
where /q git
if ERRORLEVEL 1 (
    echo Ohjelmaa Git ei ole asennettu järjestelmään, joten se asennetaan automaattisesti. Sitä käytetään ohjelman automaattisiin päivityksiin.
    echo.
    rem Download and install Git
    call python -c "import os.path; import subprocess; import urllib.request; import shutil; from winreg import *; dl_dir = QueryValueEx(OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'), '{374DE290-123F-4565-9164-39C4925E467B}')[0]; shutil.copyfileobj(urllib.request.urlopen(r'https://github.com/git-for-windows/git/releases/download/v2.15.1.windows.2/Git-2.15.1.2-64-bit.exe'), open(os.path.join(dl_dir, 'git_installer.exe'), 'wb')); subprocess.Popen([os.path.join(dl_dir, 'git_installer.exe')])"
    echo Git-ohjelman asennustyökalu on ladattu koneellesi, suoritathan sen asennuksen loppuun ennen kuin jatkat videolataajan asennusta.
    echo.
    set /p continue="Paina Enter, kun Git on asennettu."

    rem Reset ERRORLEVEL to 0
    ver > nul
) else (
    echo Git on ilmeisesti jo asennettu. Loistavaa!
    echo Luodaan Git-repoa...
    echo.

    rem Move to install directory to handle Git commands
    cd "%install_dir%\.."
    git clone -b gramps --single-branch "https://github.com/Diapolo10/youtube-dl-gui"
    cd "%mypath:~0,-1%"
)



if not exist "C:\larin_ohjelmat\youtube-dl-gui" (
    echo Päivitysten asennus epäonnistui, asennetaan suoraan levyltä...
    echo.
    xcopy /s /e /y /v /k /g "%mypath:~0,-1%"\..\* "%install_dir%"
) else (
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
