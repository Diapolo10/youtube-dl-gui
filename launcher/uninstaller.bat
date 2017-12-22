@echo off
rmdir /s /q "%systemdrive%\larin_ohjelmat\youtube-dl-gui"
if ERRORLEVEL 1 (
    @echo Error when uninstalling program; make sure there are no programs using the directory. & echo.> error.log
) else (
    echo Uninstallation successful
)
