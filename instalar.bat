@echo off
echo.
echo ==========================================
echo Instalacion del sistema
echo ==========================================

python --version >nul 2>&1
if errorlevel 1 (
    echo Python no esta instalado o no esta en PATH.
    pause
    exit /b
)

if not exist "venv" (
    python -m venv venv
    echo Entorno virtual creado.
) else (
    echo El entorno virtual ya existe.
)

call venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --noinput

echo.
echo Instalacion completada correctamente.
pause