@echo off
setlocal

REM 👉 Cambia esta ruta si tu instalación es diferente
set VC_VARS="C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

echo --- Iniciando entorno Visual C++ ---
call %VC_VARS%
if errorlevel 1 (
  echo ❌ No se pudo cargar vcvars64.bat
  pause
  exit /b 1
)

echo --- Activando entorno virtual ---
call venv\Scripts\activate.bat
if errorlevel 1 (
  echo ❌ No se pudo activar venv
  pause
  exit /b 1
)

echo --- Verificando CMake ---
cmake --version >nul 2>&1
if errorlevel 1 (
  echo ❌ CMake no encontrado en el PATH
  pause
  exit /b 1
)

echo --- Verificando Ninja ---
ninja --version >nul 2>&1
if errorlevel 1 (
  echo ❌ Ninja no encontrado en el PATH
  pause
  exit /b 1
)

echo --- Limpiando carpeta de build ---
if exist build (
  rmdir /s /q build
) else (
  echo (No existía la carpeta build)
)
mkdir build
cd build

echo --- Ejecutando CMake ---
cmake -GNinja ^
  -DBUILD_PYTHON=ON ^
  -DBUILD_TEST=ON ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_INSTALL_PREFIX=%CD%\..\pytorch\torch ^
  -DCMAKE_PREFIX_PATH=%CD%\..\venv\Lib\site-packages ^
  -DPython_EXECUTABLE=%CD%\..\venv\Scripts\python.exe ^
  -DUSE_NUMPY=ON ^
  ..\pytorch

if errorlevel 1 (
  echo ❌ Error durante configuración CMake
  pause
  exit /b 1
)

echo --- Iniciando compilación con Ninja ---
ninja
if errorlevel 1 (
  echo ❌ Error durante compilación Ninja
  pause
  exit /b 1
)

echo ✅ Compilación completada exitosamente
pause