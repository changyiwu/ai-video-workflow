@echo off
REM BreezyVoice one-shot: generate candidates (BreezyVoice venv) then auto-pick (Voice venv). Usage: make_breezyvoice.cmd jobs.json
REM See breezyvoice_batch.py / breezyvoice_pick.py headers. Keep this file ASCII-only (cmd reads it in the console codepage).
setlocal
REM Install root AI_ROOT (default C:\AI) holds BreezyVoice\ and Voice\; PY_BREEZYVOICE / PY_VOICE override the two venvs.
set PYTHONUTF8=1
if not defined AI_ROOT set "AI_ROOT=C:\AI"
if not defined PY_BREEZYVOICE set "PY_BREEZYVOICE=%AI_ROOT%\BreezyVoice\venv\Scripts\python.exe"
if not defined PY_VOICE set "PY_VOICE=%AI_ROOT%\Voice\venv\Scripts\python.exe"
set "PYTHONPATH=%AI_ROOT%\BreezyVoice\winstub;%AI_ROOT%\BreezyVoice\code;%AI_ROOT%\BreezyVoice\code\third_party\Matcha-TTS"
"%PY_BREEZYVOICE%" "%~dp0breezyvoice_batch.py" %1 < NUL || exit /b 1
set PYTHONPATH=
"%PY_VOICE%" "%~dp0breezyvoice_pick.py" %1
endlocal
