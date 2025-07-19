@echo off
:: ================================
::  Refrescando tokens de Freesound.org...
:: ================================
echo [%DATE% %TIME%] Ejecutando actualización de token... > token_refresh.log

:: Activar entorno virtual
call .\venv\Scripts\activate

:: Ejecutar el script Python y redirigir salida a log
python refresh_token_freesound.py >> token_refresh.log 2>&1

:: Verificar si fue exitoso
findstr /C:"✅ Tokens actualizados correctamente." token_refresh.log >nul
if %errorlevel%==0 (
    echo ✅ Tokens actualizados correctamente. También se guardó en token_refresh.log
) else (
    echo ❌ Hubo un error. Revisa token_refresh.log para más detalles.
)

echo.
pause