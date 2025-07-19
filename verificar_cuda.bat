@echo off
setlocal enabledelayedexpansion

echo ====================================
echo === ACTIVANDO ENTORNO VIRTUAL... ===
echo ====================================

REM Activar entorno virtual
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Error: No se pudo activar el entorno virtual.
    pause
    exit /b
)

echo.
echo ====================================
echo === VERIFICANDO CUDA EN PYTORCH ===
echo ====================================

python verificar_cuda.py

if errorlevel 1 (
    echo ❌ Error al ejecutar verificar_cuda.py
) else (
    echo ✅ Verificación completada exitosamente.
)

echo.
pause