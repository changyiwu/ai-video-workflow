@echo off
REM VoxCPM2 one-shot (default voice engine): generate candidates then auto-pick, both in the Voice venv. Usage: make_voxcpm.cmd jobs.json
REM See voxcpm_batch.py / voice_pick.py headers. Keep this file ASCII-only (cmd reads it in the console codepage).
setlocal
REM Voice venv: PY_VOICE (set in configs\profile*.cmd), else %AI_ROOT%\Voice (AI_ROOT defaults to C:\AI).
set PYTHONUTF8=1
if not defined AI_ROOT set "AI_ROOT=C:\AI"
if not defined PY_VOICE set "PY_VOICE=%AI_ROOT%\Voice\venv\Scripts\python.exe"
"%PY_VOICE%" "%~dp0voxcpm_batch.py" %1 < NUL || exit /b 1
"%PY_VOICE%" "%~dp0voice_pick.py" %1
endlocal
