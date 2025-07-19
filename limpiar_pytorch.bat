@echo off
setlocal

echo === LIMPIANDO CARPETAS DE BUILD Y CACHE ===

:: Ruta del proyecto
set PROYECTO_DIR=%~dp0

:: Carpeta de build
set BUILD_DIR=%PROYECTO_DIR%build

:: Archivos comunes de cache
set CMAKE_CACHE=%PROYECTO_DIR%CMakeCache.txt
set CMAKE_FILES=%PROYECTO_DIR%CMakeFiles

:: Limpiar build
if exist "%BUILD_DIR%" (
    echo Eliminando carpeta build...
    rmdir /S /Q "%BUILD_DIR%"
) else (
    echo No se encontró la carpeta build.
)

:: Limpiar CMakeCache.txt
if exist "%CMAKE_CACHE%" (
    echo Eliminando CMakeCache.txt...
    del /F /Q "%CMAKE_CACHE%"
)

:: Limpiar carpeta CMakeFiles
if exist "%CMAKE_FILES%" (
    echo Eliminando carpeta CMakeFiles...
    rmdir /S /Q "%CMAKE_FILES%"
)

echo === LIMPIEZA COMPLETA ===
pause