@echo off
REM VoxCPM2 one-shot (default voice engine): generate candidates then auto-pick, both in the Voice venv. Usage: make_voxcpm.cmd jobs.json
REM See voxcpm_batch.py / breezyvoice_pick.py headers. Keep this file ASCII-only (cmd reads it in the console codepage).
setlocal
set PYTHONUTF8=1
C:\AI\Voice\venv\Scripts\python.exe C:\AI\tools\voxcpm_batch.py %1 < NUL || exit /b 1
C:\AI\Voice\venv\Scripts\python.exe C:\AI\tools\breezyvoice_pick.py %1
endlocal
