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
"%PYTHON%" -m pytest
if errorlevel 1 exit /b %ERRORLEVEL%
"%PYTHON%" -m ruff check src tests
exit /b %ERRORLEVEL%

