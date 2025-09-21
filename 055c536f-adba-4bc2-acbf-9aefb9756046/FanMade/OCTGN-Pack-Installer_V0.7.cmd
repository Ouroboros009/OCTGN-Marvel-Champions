:BEGIN
@echo off
title OCTGN FanMade Deck Installer
cls
SET  Version=0.7
if exist "%~dp0OCTGN-Pack-Installer_V%Version%.ps1" (
	PowerShell.exe -ExecutionPolicy Bypass -File "%~dp0OCTGN-Pack-Installer_V%Version%.ps1"
) else (
	echo.
	echo.
	echo     _____                            .__  .__                       
	echo    /     \ _____ __________  __ ____ ^|  ^| ^|  ^|   ____  __ __  ______
	echo   /  \ /  \\__  \\_  __ \  \/ // __ \^|  ^| ^|  ^|  /  _ \^|  ^|  \/  ___/
	echo  /    Y    \/ __ \^|  ^| \/\   /\  ___/^|  ^|_^|  ^|_^(  ^<_^> ^)  ^|  /\___ \
	echo  \____^|__  (____  /__^|    \_/  \___  ^>____/____/\____/^|____//____  ^>
	echo          \/     \/                 \/                            \/ 
	echo.
	echo                  OCTGN FanMade Deck Installer V%Version% 
	echo.
	echo.
	echo [91mOCTGN-Pack-Installer_V%Version%.ps1[0m : File is missing in the current folder.
	echo.
	echo Good bye
	pause
)
:END

