#!/bin/bash

# Script de démarrage pour Render

echo "🚀 Démarrage de Jarvis sur Render..."

# Installer les dépendances si nécessaire
pip install -r requirements.txt

# Démarrer l'application avec Uvicorn
# Render fournit automatiquement la variable $PORT
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
