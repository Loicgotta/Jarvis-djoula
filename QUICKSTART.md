# 🚀 Guide de Démarrage Rapide - Jarvis

## Installation en 3 étapes

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2️⃣ Démarrer l'application

```bash
python app.py
```

OU utilisez le script de démarrage :

```bash
./start.sh
```

### 3️⃣ Ouvrir dans le navigateur

Ouvrez : **http://localhost:8000**

## 🎤 Utilisation Rapide

### Option 1 : Audio
1. Enregistrez un message vocal en dioula ou français
2. Uploadez le fichier (MP3, WAV, etc.)
3. Cliquez sur "Envoyer à Jarvis"
4. Écoutez la réponse en dioula avec phonétique

### Option 2 : Texte
1. Écrivez votre question dans la zone de texte
2. Cliquez sur "Envoyer le texte à Jarvis"
3. Lisez et écoutez la réponse

## ✅ Test Rapide

Vérifiez que tout fonctionne :

```bash
python test_system.py
```

## 📝 Exemples de Questions

- "Comment on dit bonjour en dioula?"
- "Je veux apprendre à me présenter"
- "Quel est le mot pour 'travail'?"
- "Comment demander 'Comment vas-tu?'"

## ⚡ Commandes Utiles

```bash
# Démarrer l'application
python app.py

# Tester le système
python test_system.py

# Tester uniquement le RAG
python rag_system.py

# Tester uniquement l'agent
python jarvis_agent.py
```

## 🆘 Problèmes Courants

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key not found"
Vérifiez que `.env` contient votre clé OpenAI

### "Port already in use"
Changez le port dans `app.py` ligne 395

## 📚 Documentation Complète

Consultez [README.md](README.md) pour la documentation complète.

---

**Prêt à apprendre le dioula ? Lancez Jarvis maintenant ! 🎓**
