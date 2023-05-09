@echo off
setlocal enabledelayedexpansion

rem Microsoft Edge Userdir Path
set edge_user_data=%LocalAppData%\Microsoft\Edge\User Data
if not exist "%edge_user_data%" (
    echo Microsoft Edge user directory not found.
    pause
    exit /b 1
)
echo %edge_user_data% > userdir.txt

rem Path of "msedgedriver.exe" in the directory one level above
set msedgedriver_path=%~dp0driver\msedgedriver.exe
echo %msedgedriver_path% > msedgedriver_path.txt

rem Path of "oldShipList" in the directory one level above
set oldShipList_path=%~dp0oldShipList
echo %oldShipList_path% > oldShipList_path.txt

rem Path of "output.csv" in the directory one level above
set output_path=%~dp0output.csv
echo %output_path% > output_path.txt
pause
