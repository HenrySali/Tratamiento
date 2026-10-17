@echo off
REM ============================================
REM Script para ejecutar la interfaz web (Windows)
REM ============================================

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🎵 TRATAMIENTO - Audio Processor Web Interface      ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Verificar que el entorno virtual existe
if not exist "venv" (
    echo ❌ Entorno virtual no encontrado
    echo Ejecuta primero: python -m venv venv
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 📦 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar que Flask está instalado
echo 🔍 Verificando dependencias...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Instalando Flask...
    pip install flask werkzeug
)

REM Crear directorios necesarios
if not exist "uploads" mkdir uploads
if not exist "processed_audio" mkdir processed_audio

REM Información
echo.
echo ✅ Todo listo!
echo.
echo 🌐 Iniciando servidor en:
echo    http://localhost:5000
echo.
echo 💡 Consejos:
echo    • Abre el navegador en http://localhost:5000
echo    • Arrastra y suelta tu archivo de audio
echo    • Presiona CTRL+C para detener el servidor
echo.

REM Ejecutar aplicación
python web_app.py

pause
