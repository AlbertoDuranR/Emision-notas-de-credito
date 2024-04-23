@echo off

title AppNotasCreditoFrontend.bat

:inicio

REM Obtener el PID del proceso que está utilizando el puerto 3000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000"') do (
    set "PID=%%a"
)

REM Finalizar el proceso que está utilizando el puerto 3000
if defined PID (
    taskkill /F /PID %PID%
    echo Proceso que utiliza el puerto 3000 finalizado.
) else (
    echo No se encontró ningún proceso utilizando el puerto 3000.
)

REM Levantar FrontEnd VueJS
echo Iniciando FrontEnd VueJS...
cd "E:\Python\Emision-notas-de-credito\app_enc"
npm run dev

REM Mensaje de finalización
echo Proceso completado.

REM Esperar unos segundos antes de reiniciar
timeout /t 60

REM Reiniciar el proceso desde el inicio
goto inicio