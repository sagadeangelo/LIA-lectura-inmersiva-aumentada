@echo off
echo === LIMPIANDO CACHE DE CMAKE ===

REM Ruta del proyecto
set PROYECTO_DIR=C:\PROYECTOS-FLUTTER\LIA-lectura-inmersiva-aumentada

REM Carpeta de build que CMake genera (ajusta si es diferente)
set BUILD_DIR=%PROYECTO_DIR%\build

if exist "%BUILD_DIR%" (
    echo Eliminando carpeta de build: %BUILD_DIR%
    rmdir /s /q "%BUILD_DIR%"
) else (
    echo No se encontró carpeta de build. Nada que limpiar.
)

REM También puede haber un CMakeCache.txt en el root
if exist "%PROYECTO_DIR%\CMakeCache.txt" (
    echo Eliminando CMakeCache.txt
    del /q "%PROYECTO_DIR%\CMakeCache.txt"
)

echo === LIMPIEZA COMPLETA ===
pause