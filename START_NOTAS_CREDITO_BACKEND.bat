@echo off

REM Identificar y cerrar la ventana de cmd con el título especificado
powershell -Command "Get-Process | Where-Object {$_.MainWindowTitle -eq 'AppNotasCreditoBackend.bat'} | ForEach-Object {Stop-Process -Id $_.Id}"

title AppNotasCreditoBackend.bat

:inicio

REM Paso 1: Levantar .venv
echo Iniciando entorno virtual...
cd /d "E:\Python\Emision-notas-de-credito"
call .venv\Scripts\activate

REM Paso 3: Levantar el backend Django
echo Iniciando backend Django...
cd app_enc
python manage.py runserver 10.5.0.11:8000

REM Mensaje de finalización
echo Proceso completado.

REM Esperar unos segundos antes de reiniciar
timeout /t 10

REM Reiniciar el proceso desde el inicio
goto inicio