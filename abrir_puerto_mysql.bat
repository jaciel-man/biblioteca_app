@echo off
echo.
echo ========================================================
echo Abriendo puerto 3306 (MySQL) en el Firewall de Windows
echo ========================================================
echo.
netsh advfirewall firewall add rule name="MySQL para Celular" dir=in action=allow protocol=TCP localport=3306
echo.
echo Si dice "Aceptar" u "Ok", el puerto se abrio correctamente.
echo Presiona cualquier tecla para salir...
pause >nul
