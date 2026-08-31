#!/usr/bin/env bash
# ==============================================================================
# Script de empaquetado para entrega final de la Prueba de Desempeño
# Genera un archivo .zip limpio con todos los componentes requeridos
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_ZIP="$PROJECT_DIR/Prueba_Desempeno_AI_Automatizador.zip"

cd "$PROJECT_DIR"

echo "======================================================================"
echo "📦 GENERANDO PAQUETE DE ENTREGA (.ZIP)"
echo "======================================================================"

# Eliminar zip previo si existe
rm -f "$OUTPUT_ZIP"

# Crear archivo zip excluyendo entornos virtuales y node_modules
zip -r "$OUTPUT_ZIP" . \
  -x "*.venv/*" \
  -x "frontend/node_modules/*" \
  -x "frontend/dist/*" \
  -x "*/__pycache__/*" \
  -x "*.git/*" \
  -x ".env" \
  -x "*.DS_Store"

echo ""
echo "======================================================================"
echo "✅ ARCHIVO DE ENTREGA GENERADO EXITOSAMENTE:"
echo "📁 $OUTPUT_ZIP ($(du -h "$OUTPUT_ZIP" | cut -f1))"
echo "======================================================================"
