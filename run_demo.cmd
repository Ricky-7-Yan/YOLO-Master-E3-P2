@echo off
setlocal
set "ROOT=%~dp0"
set "PYTHON=%ROOT%..\YOLO-Master-baseline\.venv\Scripts\python.exe"
if not exist "%PYTHON%" (
  echo ERROR: project-local Python not found: "%PYTHON%"
  exit /b 2
)
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
cd /d "%ROOT%"
set "PYTHONPATH=%ROOT%src"
"%PYTHON%" -m e3_p2 demo %*
exit /b %ERRORLEVEL%

