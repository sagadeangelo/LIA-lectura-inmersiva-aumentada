@echo off
REM --------------------------------------------
REM Archivo: build_pytorch.bat
REM Propósito: Activar entorno y compilar PyTorch
REM Requiere: CMake 3.27.x o 3.29.x y MSVC 14.3x
REM --------------------------------------------

REM Cambia a la carpeta de tu proyecto
cd /d C:\PROYECTOS-FLUTTER\LIA-lectura-inmersiva-aumentada

REM Activar entorno virtual
call .\venv\Scripts\activate.bat

REM Iniciar el entorno del compilador de Visual Studio
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

REM Verifica que CMake funcione
echo --- Verificando versión de CMake ---
cmake --version
if errorlevel 1 (
    echo Error: CMake no está disponible en PATH.
    pause
    exit /b 1
)

REM Limpia build anterior si existiera
echo --- Eliminando build anterior ---
rmdir /s /q pytorch\build 2>nul

REM Ejecuta la instalación
echo --- Iniciando compilación de PyTorch ---
python pytorch\setup.py install

echo.
echo === Proceso finalizado. Presiona una tecla para salir... ===
pause