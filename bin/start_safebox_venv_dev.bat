@echo off

@REM powershell -NoExit -Command "cd /d %~dp0; .\env\Scripts\Activate.ps1"

title DEV VENV SAFEBOX

@REM powershell -NoExit -ExecutionPolicy Bypass -Command "Set-Location '%~dp0'; .\.venv\Scripts\Activate.ps1"

powershell -NoExit -ExecutionPolicy Bypass -Command "Set-Location '%~dp0..'; & '%~dp0..\venv\Scripts\Activate.ps1'"