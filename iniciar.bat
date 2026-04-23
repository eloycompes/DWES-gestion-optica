@echo off
echo.
echo ==========================================
echo Inicio del sistema
echo ==========================================

if not exist "venv\Scripts\activate.bat" (
    echo No se ha encontrado el entorno virtual.
    echo Ejecuta primero instalar.bat
    pause
    exit /b
)

if not exist "manage.py" (
    echo No se encuentra manage.py
    echo Ejecuta este archivo en la carpeta raiz del proyecto.
    pause
    exit /b
)

call venv\Scripts\activate

echo Iniciando servidor Django...
echo http://127.0.0.1:8000

start http://127.0.0.1:8000

python manage.py runserver