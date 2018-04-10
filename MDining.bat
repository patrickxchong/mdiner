@echo off
start python app.py
SLEEP 1
START /B CMD /C CALL "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --allow-file-access-from-files http://127.0.0.1:5000/