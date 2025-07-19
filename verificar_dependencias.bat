@echo off
setlocal

echo === Verificando dependencias de Python ===

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Revisar e instalar si falta algún paquete
echo.
echo --- Verificando numpy ---
pip show numpy >nul 2>&1 || pip install numpy

echo --- Verificando pyyaml ---
pip show pyyaml >nul 2>&1 || pip install pyyaml

echo --- Verificando typing_extensions ---
pip show typing_extensions >nul 2>&1 || pip install typing_extensions

echo --- Verificando setuptools ---
pip show setuptools >nul 2>&1 || pip install setuptools

echo.
echo ✅ Verificación completada.
pause