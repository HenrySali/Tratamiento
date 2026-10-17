#!/bin/bash

# ============================================
# Script para ejecutar la interfaz web
# ============================================

echo "╔════════════════════════════════════════════════════════╗"
echo "║   🎵 TRATAMIENTO - Audio Processor Web Interface      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Verificar que el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado"
    echo "Ejecuta primero: python3 -m venv venv"
    exit 1
fi

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Verificar que Flask está instalado
echo "🔍 Verificando dependencias..."
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Instalando Flask..."
    pip install flask werkzeug
fi

# Limpiar archivos temporales
echo "🧹 Limpiando archivos temporales..."
rm -rf __pycache__ 2>/dev/null
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null

# Crear directorios necesarios
mkdir -p uploads processed_audio

# Información
echo ""
echo "✅ Todo listo!"
echo ""
echo "🌐 Iniciando servidor en:"
echo "   http://localhost:5000"
echo ""
echo "💡 Consejos:"
echo "   • Abre el navegador en http://localhost:5000"
echo "   • Arrastra y suelta tu archivo de audio"
echo "   • Presiona CTRL+C para detener el servidor"
echo ""

# Ejecutar aplicación
python web_app.py
