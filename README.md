# 🎓 Jarvis - Professeur de Dioula avec IA

Jarvis est un agent IA intelligent conçu pour enseigner la langue dioula. Il utilise un système RAG (Retrieval-Augmented Generation) basé sur un dictionnaire dioula complet, et offre une interface vocale naturelle grâce aux technologies d'OpenAI.

## 🌟 Fonctionnalités

- **🎤 Interface Vocale**: Parlez en dioula, Jarvis vous répond
- **📚 Base de Connaissances RAG**: Accès au dictionnaire dioula complet
- **🔊 Synthèse Vocale**: Réponses avec prononciation phonétique correcte (voix Alloy)
- **📝 Mode Texte**: Possibilité d'écrire au lieu de parler
- **🎯 Enseignement Personnalisé**: Jarvis adapte ses réponses à votre niveau

## 🏗️ Architecture

```
Jarvis-djoula/
├── app.py                  # Application principale (FastAPI)
├── jarvis_agent.py         # Agent IA Jarvis
├── rag_system.py           # Système RAG avec ChromaDB
├── dioula_dictionary.py    # Base de données du dictionnaire
├── voice_interface.py      # Interface vocale (STT/TTS)
├── requirements.txt        # Dépendances Python
├── .env                    # Variables d'environnement
└── README.md              # Ce fichier
```

## 🚀 Installation

### 1. Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Clé API OpenAI

### 2. Installation des dépendances

```bash
# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration

Le fichier `.env` est déjà configuré avec la clé API OpenAI. Si vous devez la modifier :

```bash
# Éditer le fichier .env
OPENAI_API_KEY=votre_clé_api_ici
```

## 🎯 Utilisation

### Démarrer l'application

```bash
python app.py
```

L'application sera accessible sur : **http://localhost:8000**

### Interface Web

1. Ouvrez votre navigateur à l'adresse `http://localhost:8000`
2. Choisissez une option :
   - **Option 1 - Audio**: Uploadez un fichier audio (MP3, WAV, etc.)
   - **Option 2 - Texte**: Écrivez directement votre question
3. Jarvis analyse et répond en dioula avec phonétique
4. Écoutez la réponse vocale avec la prononciation correcte

### API Endpoints

#### POST `/process-audio`
Traite un fichier audio et retourne la transcription + réponse de Jarvis

**Request:**
```bash
curl -X POST "http://localhost:8000/process-audio" \
  -F "file=@votre_audio.mp3"
```

**Response:**
```json
{
  "transcript": "Comment on dit bonjour?",
  "response": "I ni sɔgɔma (prononciation: i ni so-go-ma) - Bonjour à toi le matin...",
  "audio_file": "jarvis_response_123456.mp3"
}
```

#### POST `/process-text`
Traite du texte et retourne la réponse de Jarvis

**Request:**
```bash
curl -X POST "http://localhost:8000/process-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Comment dire merci en dioula?"}'
```

**Response:**
```json
{
  "response": "A ni ce (prononciation: a ni tchè) - Merci...",
  "audio_file": "jarvis_text_123456.mp3"
}
```

#### GET `/audio/{filename}`
Récupère un fichier audio généré

#### GET `/health`
Vérifie l'état du service

## 📚 Système RAG

Le système RAG (Retrieval-Augmented Generation) permet à Jarvis d'accéder à un dictionnaire dioula complet :

- **Indexation vectorielle** avec ChromaDB
- **Embeddings** OpenAI (text-embedding-3-small)
- **Recherche sémantique** pour trouver les mots et expressions pertinents
- **Contexte enrichi** pour des réponses précises

## 🎤 Technologies Vocales

### Speech-to-Text (Whisper)
- Modèle : `whisper-1` d'OpenAI
- Supporte le français et le dioula
- Haute précision de transcription

### Text-to-Speech
- Modèle : `tts-1` d'OpenAI
- Voix : **Alloy** (optimisée pour la clarté)
- Vitesse : 0.9x (pour une meilleure compréhension)
- Respect de la phonétique dioula

## 🔧 Personnalisation

### Modifier le prompt système

Éditez `jarvis_agent.py` ligne 17 pour ajuster le comportement de Jarvis :

```python
SYSTEM_PROMPT = """Tu es Jarvis, un professeur de dioula...
[Personnalisez ici]
"""
```

### Ajouter des mots au dictionnaire

Éditez `dioula_dictionary.py` et ajoutez vos entrées dans `DIOULA_DICTIONARY`.

### Changer la voix TTS

Dans `voice_interface.py`, modifiez le paramètre `voice` :
- Options: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

## 🧪 Tests

### Tester le système RAG
```bash
python rag_system.py
```

### Tester l'agent Jarvis
```bash
python jarvis_agent.py
```

### Tester l'interface vocale
```bash
python voice_interface.py
```

## 📁 Données Générées

- `./chroma_db/` - Base de données vectorielle ChromaDB
- `./audio_outputs/` - Fichiers audio générés par Jarvis
- `./uploads/` - Fichiers audio uploadés par les utilisateurs

## ⚠️ Notes Importantes

1. **Clé API** : Ne partagez jamais votre clé API OpenAI
2. **Coût** : Les API OpenAI sont payantes (STT, TTS, GPT-4)
3. **Langues** : Le système est optimisé pour le dioula avec support français
4. **Phonétique** : Jarvis indique systématiquement la prononciation

## 🤝 Contribution

Ce projet est conçu pour l'enseignement du dioula. Les contributions sont les bienvenues !

## 📄 Licence

Ce projet est fourni à des fins éducatives.

## 🆘 Support

En cas de problème :
1. Vérifiez que votre clé API OpenAI est valide
2. Assurez-vous que toutes les dépendances sont installées
3. Consultez les logs dans le terminal

## 🎓 Exemples d'Utilisation

### Apprendre les salutations
**Vous**: "Comment on dit bonjour le matin?"
**Jarvis**: "I ni sɔgɔma (prononciation: i ni so-go-ma) - c'est comme ça qu'on dit bonjour le matin en dioula..."

### Apprendre du vocabulaire
**Vous**: "Comment on dit 'travail'?"
**Jarvis**: "Baara (prononciation: ba-ra) - c'est le mot pour travail..."

### Pratiquer la conversation
**Vous**: "I ni ce!"
**Jarvis**: "I ni ce fana! (prononciation: i ni tchè fa-na) - Merci à toi aussi..."

---

**Développé avec ❤️ pour l'apprentissage du dioula**
