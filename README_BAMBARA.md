# 🇲🇱 Système de Reconnaissance Vocale Bambara avec Djelia AI et ElevenLabs

## 📋 Vue d'ensemble

Ce système offre une interface vocale complète pour le bambara, intégrant :

1. **Djelia AI** : API spécialisée pour la reconnaissance vocale en bambara
2. **ElevenLabs** : Agent conversationnel pour des réponses vocales naturelles
3. **Interface Web** : Interface utilisateur intuitive avec sélection de mode

## 🏗️ Architecture du Système

### Flux de Traitement Audio (Mode Bambara)

```
┌─────────────────┐
│  Utilisateur    │
│  parle bambara  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Capture audio  │
│  (Microphone)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Djelia AI     │
│  Transcription  │
│   (Bambara)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent          │
│  ElevenLabs     │
│  (Réponse)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Réponse audio  │
│  + texte à      │
│  l'utilisateur  │
└─────────────────┘
```

## 📁 Fichiers Créés

### 1. `djelia_transcription.py`
Module d'intégration avec l'API Djelia AI pour la transcription vocale en bambara.

**Fonctionnalités :**
- Transcription audio vers texte en bambara
- Support de multiples formats audio (MP3, WAV, M4A, WEBM, etc.)
- Gestion d'erreurs robuste

**Endpoint API :**
- URL : `https://djelia.cloud/api/v1/models/transcribe`
- Méthode : POST
- Authentification : Header `x-api-key`

### 2. `elevenlabs_agent.py`
Module d'intégration avec l'agent conversationnel ElevenLabs.

**Fonctionnalités :**
- Envoi de messages texte à l'agent
- Récupération des réponses (texte et audio)
- Téléchargement des fichiers audio de réponse

**Configuration :**
- Agent ID : `agent_7801k3yd7xb4fgfva2r76j2fk9dm`
- Endpoint : `https://api.elevenlabs.io/v1/convai/conversation`

### 3. `bambara_voice_interface.py`
Interface vocale complète qui orchestre le flux bambara (Djelia + ElevenLabs).

**Fonctionnalités :**
- Traitement de bout en bout (audio → transcript → réponse)
- Fallback vers OpenAI TTS si nécessaire
- Logging détaillé du processus

### 4. Endpoint dans `app.py`
Nouvel endpoint `/process-bambara-audio` pour le traitement audio bambara.

## 🔑 Clés API Utilisées

### Djelia AI
```
Clé API : 4cc23e20-129b-42a0-af09-ca814e9ac23b
```

### ElevenLabs
```
Clé API : sk_e08a92815b5e911d119065275c82377c0396f3b0b2d80750
Agent ID : agent_7801k3yd7xb4fgfva2r76j2fk9dm
```

## 🚀 Utilisation

### 1. Installation des Dépendances

```bash
pip install -r requirements.txt
```

La nouvelle dépendance `requests` a été ajoutée pour les appels API HTTP.

### 2. Démarrage du Serveur

```bash
python app.py
```

L'application sera disponible sur : `http://localhost:8000`

### 3. Utilisation de l'Interface Web

#### Mode de Sélection

L'interface propose deux modes :

1. **Mode Standard (OpenAI)**
   - Transcription : OpenAI Whisper
   - Réponses : GPT-4o

2. **Mode Bambara (Djelia AI + ElevenLabs)**
   - Transcription : Djelia AI (reconnaissance bambara native)
   - Réponses : Agent ElevenLabs

#### Options d'Entrée

**Option 1A : Enregistrement Direct**
1. Sélectionnez le mode "Bambara"
2. Cliquez sur "Enregistrer"
3. Parlez en bambara
4. Cliquez sur "Arrêter"
5. Cliquez sur "Envoyer à Jarvis"

**Option 1B : Upload de Fichier**
1. Sélectionnez le mode "Bambara"
2. Uploadez un fichier audio en bambara
3. Cliquez sur "Envoyer à Jarvis"

## 🔄 Flux de Données

### Requête (Frontend → Backend)

```javascript
POST /process-bambara-audio
Content-Type: multipart/form-data

{
  file: <fichier_audio_bambara>
}
```

### Réponse (Backend → Frontend)

```json
{
  "transcript": "Texte transcrit en bambara",
  "response": "Réponse de l'agent",
  "audio_file": "elevenlabs_response_123456.mp3"
}
```

## 🔍 Tests et Débogage

### Test des Modules Individuels

#### Test Djelia AI
```bash
python djelia_transcription.py
```

#### Test ElevenLabs
```bash
python elevenlabs_agent.py
```

#### Test Interface Complète
```bash
python bambara_voice_interface.py
```

### Logs

Le système affiche des logs détaillés pour chaque étape :
- ✅ Succès
- ❌ Erreur
- ⚠️ Avertissement

## 📊 Points d'Attention

### 1. Structure de Réponse API

Les structures de réponse exactes des APIs Djelia et ElevenLabs peuvent varier. Le code inclut plusieurs vérifications pour extraire les données correctement :

```python
# Djelia AI
transcript = result.get("text") or result.get("transcript") or result.get("transcription")

# ElevenLabs
agent_text = (
    response.get("message") or
    response.get("text") or
    response.get("response")
)
```

### 2. Fallback TTS

Si l'agent ElevenLabs ne retourne pas d'audio, le système utilise automatiquement OpenAI TTS (voix "alloy") comme solution de secours.

### 3. Formats Audio Supportés

- MP3
- WAV
- M4A
- WEBM
- OGG
- FLAC

## 🛠️ Personnalisation

### Changer l'Agent ElevenLabs

Pour utiliser un autre agent ElevenLabs :

1. Modifiez dans `app.py` :
```python
bambara_interface = BambaraVoiceInterface(
    elevenlabs_agent_id="votre_nouvel_agent_id"
)
```

### Changer la Clé API Djelia

Pour utiliser une autre clé Djelia AI :

1. Modifiez dans `app.py` :
```python
bambara_interface = BambaraVoiceInterface(
    djelia_api_key="votre_nouvelle_cle"
)
```

## 🔐 Sécurité

**Important :** Dans un environnement de production :
- Stockez les clés API dans des variables d'environnement
- Utilisez un fichier `.env`
- Ne committez jamais les clés API dans Git

## 📚 Documentation des APIs

### Djelia AI
- Site web : https://www.djelia.cloud/
- Documentation : Disponible sur le site

### ElevenLabs
- Documentation : https://elevenlabs.io/docs/conversational-ai/overview
- API Reference : https://elevenlabs.io/docs/api-reference/introduction

## 🤝 Support

Pour toute question ou problème :
1. Vérifiez les logs dans la console
2. Testez les modules individuellement
3. Vérifiez la validité des clés API

## 📝 Notes Supplémentaires

- Le système utilise un timeout de 30 secondes pour les requêtes API
- Les fichiers audio sont sauvegardés dans `./audio_outputs/`
- Les uploads sont stockés dans `./uploads/`

---

**Date de création :** 2025-12-25
**Version :** 1.0.0
