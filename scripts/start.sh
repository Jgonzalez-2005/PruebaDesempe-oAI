#!/usr/bin/env bash
# ==============================================================================
# Script de Inicio Rápido - Academia LinguaColombia AI Support System
# Inicia Backend (FastAPI :8000) y Frontend (Vite :5173) de forma coordinada
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "======================================================================"
echo "🇨🇴 INICIANDO SISTEMA DE ATENCIÓN CON IA - LINGUACOLOMBIA"
echo "======================================================================"

# 1. Verificar entorno virtual Python
if [ ! -d ".venv" ]; then
    echo "[*] Creando entorno virtual de Python..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "[*] Instalando dependencias de backend..."
    pip install --upgrade pip
    pip install -r backend/requirements.txt
else
    source .venv/bin/activate
fi

# 2. Generar base de conocimiento documental si no existe
if [ ! -f "data/documents/01_programas_y_niveles.html" ]; then
    echo "[*] Generando corpus documental oficial..."
    python3 scripts/generate_documents.py
fi

# 3. Verificar dependencias de frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "[*] Instalando dependencias de frontend (npm)..."
    cd frontend && npm install && cd ..
fi

# 4. Manejo de señales para apagado limpio
cleanup() {
    echo ""
    echo "[!] Deteniendo servicios..."
    if [ -n "$BACKEND_PID" ]; then
        kill "$BACKEND_PID" 2>/dev/null || true
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill "$FRONTEND_PID" 2>/dev/null || true
    fi
    echo "[✓] Servicios detenidos exitosamente."
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# 5. Iniciar Backend FastAPI
echo "[*] Arrancando Servidor Backend FastAPI en http://localhost:8000..."
cd "$PROJECT_DIR/backend"
PYTHONPATH=. "$PROJECT_DIR/.venv/bin/uvicorn" app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd "$PROJECT_DIR"

# Esperar a que el backend esté listo
sleep 2

# 6. Iniciar Frontend Vite
echo "[*] Arrancando Servidor Frontend Vite en http://localhost:5173..."
cd "$PROJECT_DIR/frontend"
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!
cd "$PROJECT_DIR"

echo ""
echo "======================================================================"
echo "✨ SISTEMA EN LÍNEA Y LISTO PARA OPERAR"
echo "======================================================================"
echo "🌐 Frontend (Interfaz Web Chat): http://localhost:5173"
echo "📚 Backend API & Swagger Docs:   http://localhost:8000/docs"
echo "🩺 Endpoint de Salud:             http://localhost:8000/api/health"
echo "======================================================================"
echo "Presiona Ctrl+C para detener ambos servidores."
echo ""

# Mantener script corriendo
wait
