@echo off
title Jompoi ERP Business System
cd /d "C:\Users\Thejeshwharan\OneDrive\Desktop\3Qspace\Jumpoi"

set "PY_EXE=C:\Users\Thejeshwharan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if exist "%PY_EXE%" (
    "%PY_EXE%" start_erp.py %*
) else (
    python start_erp.py %*
)

pause
