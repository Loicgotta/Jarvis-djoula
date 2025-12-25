# Intégration Elevenlabs avec Jarvis

## Problème résolu

L'agent Elevenlabs Conversational AI recevait des messages invalides à cause des:
- ❌ Emojis (👋, 🎓, 1️⃣, 2️⃣, etc.)
- ❌ Markdown (**gras**, *italique*, `code`)
- ❌ Structures complexes avec symboles (→, ##, etc.)

## Solution

Un endpoint dédié `/elevenlabs-message` qui retourne des messages nettoyés.

## Utilisation

### Endpoint dédié Elevenlabs

**POST** `/elevenlabs-message`

**Body:**
```json
{
  "text": "ka"
}
```

**Réponse:**
```json
{
  "message": "Aw ni tile! I be fo: ka. O be se ka ke: 1. ka (prononciation: kà) Koro: infinitif yo. Misali: Ka baara (pour travailler). 2. ka (prononciation: ká) Koro: yala (peut-être). I y'a fe ka mun fo?"
}
```

Le champ `message` contient uniquement du texte simple, sans emojis ni markdown.

### Endpoints existants

Les endpoints `/process-audio` et `/process-text` retournent maintenant deux versions:
- `response`: Version complète avec emojis et markdown (pour affichage web)
- `response_clean`: Version nettoyée (pour Elevenlabs)

**Exemple:**
```json
{
  "transcript": "ni sogoma",
  "response": "Aw ni tile! 👋\n\nI bɛ fɔ: \"ni sogoma\"...",
  "response_clean": "Aw ni tile! I be fo: ni sogoma...",
  "audio_file": "jarvis_response_1234567890.mp3"
}
```

## Configuration Elevenlabs Agent

Dans votre configuration Elevenlabs Conversational AI:

1. **Webhook URL:** `https://votre-app.onrender.com/elevenlabs-message`
2. **Method:** POST
3. **Body template:**
```json
{
  "text": "{{user_message}}"
}
```
4. **Response mapping:** `{{message}}`

## Nettoyage appliqué

Le système enlève automatiquement:
- Tous les emojis et symboles Unicode
- Markdown (gras, italique, code)
- Numéros de liste avec emojis (1️⃣, 2️⃣)
- Flèches (→) remplacées par (:)
- Headers markdown (##)
- Espaces multiples

Le texte dioula avec accents tonaux est **préservé** (à, á, ǎ, ɛ, ɔ, ɲ, etc.)
