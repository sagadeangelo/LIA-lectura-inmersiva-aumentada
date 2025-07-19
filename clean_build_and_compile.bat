@echo off
setlocal

echo =============================================
echo 🧹 Eliminando carpeta build anterior (si existe)...
echo =============================================

IF EXIST build (
    rmdir /S /Q build
    echo ✔ Carpeta build eliminada.
) ELSE (
    echo ℹ No hay carpeta build que eliminar.
)

echo.
echo =============================================
echo 🔧 Iniciando compilación de PyTorch limpia...
echo =============================================

REM Iniciar entorno de compilación de VS si no está iniciado
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

REM Establecer variables del compilador correctas
set "CC=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.36.32532\bin\Hostx64\x64\cl.exe"
set "CXX=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.36.32532\bin\Hostx64\x64\cl.exe"

REM Ejecutar CMake
cmake -GNinja ^
 -DBUILD_PYTHON=True ^
 -DBUILD_TEST=True ^
 -DCMAKE_BUILD_TYPE=Release ^
 -DCMAKE_INSTALL_PREFIX=%CD%\pytorch\torch ^
 -DCMAKE_PREFIX_PATH=%CD%\venv\Lib\site-packages ^
 -DPython_EXECUTABLE=%CD%\venv\Scripts\python.exe ^
 -DTORCH_BUILD_VERSION=2.9.0a0+git89d842f ^
 -DUSE_NUMPY=True ^
 %CD%\pytorch

pause
endlocal