#!/bin/bash

# Script de démarrage pour Jarvis - Professeur de Dioula

echo "🎓 =========================================="
echo "   Jarvis - Professeur de Dioula"
echo "========================================== 🎓"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Python 3 détecté"

# Vérifier si les dépendances sont installées
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

echo "📥 Installation des dépendances..."
pip install -q -r requirements.txt

echo ""
echo "🚀 Démarrage de Jarvis..."
echo "📍 URL: http://localhost:8000"
echo ""
echo "💡 Astuce: Ouvrez http://localhost:8000 dans votre navigateur"
echo ""
echo "⚠️  Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Démarrer l'application
python3 app.py
