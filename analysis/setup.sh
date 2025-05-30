#!/bin/bash

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Determinar qué comando de Python usar
if command_exists python3; then
    PYTHON_CMD=python3
elif command_exists python; then
    # Verificar la versión de Python
    version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if (( $(echo "$version >= 3.8" | bc -l) )); then
        PYTHON_CMD=python
    else
        echo "Error: Se requiere Python 3.8 o superior"
        exit 1
    fi
else
    echo "Error: No se encontró Python. Por favor, instala Python 3.8 o superior"
    exit 1
fi

echo "Usando Python: $($PYTHON_CMD --version)"

# Limpiar entorno anterior si existe
if [ -d "venv" ]; then
    echo "Eliminando entorno virtual anterior..."
    rm -rf venv
fi

# Limpiar entorno anterior si existe
if [ -d ".venv" ]; then
    echo "Eliminando entorno virtual anterior..."
    rm -rf .venv
fi

# Crear entorno virtual
echo "Creando nuevo entorno virtual..."
$PYTHON_CMD -m venv .venv

# Activar entorno virtual
source .venv/bin/activate

# Actualizar pip
echo "Actualizando pip..."
python -m pip install --upgrade pip

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Crear directorios necesarios si no existen
echo "Creando directorios..."
mkdir -p data
mkdir -p logs
mkdir -p output

echo "¡Entorno configurado correctamente!"
echo ""
echo "Para activar el entorno virtual:"
echo "  source .venv/bin/activate"
echo ""
echo "Para desactivar el entorno virtual:"
echo "  deactivate"
echo ""
echo "Para limpiar dependencias globales de pip:"
echo "  pip freeze > temp_requirements.txt"
echo "  pip uninstall -y -r temp_requirements.txt"
echo "  rm temp_requirements.txt" 