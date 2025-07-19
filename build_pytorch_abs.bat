@echo off
setlocal

echo === INICIANDO COMPILACIÓN DE PYTORCH ===

REM --- Activar entorno de Visual Studio ---
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

REM --- Rutas absolutas del proyecto ---
set PROYECTO=C:\PROYECTOS-FLUTTER\LIA-lectura-inmersiva-aumentada
set PYTORCH=%PROYECTO%\pytorch
set VENV=%PROYECTO%\venv

REM --- Verificar CMake ---
echo --- Verificando CMake ---
cmake --version >nul 2>&1
if errorlevel 1 (
    echo ❌ CMake no está instalado o no está en el PATH.
    pause
    exit /b 1
)

REM --- Eliminar build anterior ---
echo --- Eliminando carpeta build anterior ---
rmdir /s /q %PROYECTO%\build
mkdir %PROYECTO%\build
cd /d %PROYECTO%\build

REM --- Ejecutar CMake ---
echo --- Ejecutando CMake ---
cmake -GNinja ^
  -DBUILD_PYTHON=True ^
  -DBUILD_TEST=True ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_INSTALL_PREFIX=%PYTORCH%\torch ^
  -DCMAKE_PREFIX_PATH=%VENV%\Lib\site-packages ^
  -DPython_EXECUTABLE=%VENV%\Scripts\python.exe ^
  -DTORCH_BUILD_VERSION=2.9.0a0+git89d842f ^
  -DUSE_NUMPY=True ^
  %PYTORCH%

if errorlevel 1 (
    echo ❌ Error al ejecutar CMake. Abortando.
    pause
    exit /b 1
)

REM --- Ejecutar Ninja ---
echo --- Compilando con Ninja ---
ninja
if errorlevel 1 (
    echo ❌ Error durante la compilación.
    pause
    exit /b 1
)

echo ✅ Compilación completada con éxito.
pause