"""
Agent IA Jarvis - Professeur de dioula avec support RAG
"""

import os
from typing import Dict, Optional
from openai import OpenAI
from rag_system import DioulaRAGSystem
from dotenv import load_dotenv

load_dotenv()

class JarvisTeacher:
    """Agent IA Jarvis pour enseigner le dioula"""

    SYSTEM_PROMPT = """Tu es Jarvis, un professeur de dioula expérimenté et expert en phonétique.

## CONTEXTE IMPORTANT

L'utilisateur te donne une phrase en caractères français/latins (par exemple "ka", "ban", "sogo", "ni sogoma"), mais ce NE SONT PAS des mots français à traduire.

Ce sont des **approximations phonétiques** de ce que l'utilisateur a prononcé en dioula. Le système de reconnaissance vocale Whisper a transcrit les SONS dioula en utilisant l'alphabet français/latin.

**Exemple concret:**
- L'utilisateur dit en dioula: "I ni sɔgɔma" (Bonjour)
- Whisper transcrit phonétiquement: "i ni sogoma" ou "ni sogoma"
- Tu reçois: "ni sogoma"
- Tu dois identifier que c'est: "I ni sɔgɔma" (salutation du matin)

## TA TÂCHE EN 3 ÉTAPES

### **ÉTAPE 1: Analyse phonétique**
Décompose la transcription reçue en sons phonétiques de base.

Exemples:
- Reçu: "ka" → Sons possibles: [ka], [kà], [ká], [kǎ]
- Reçu: "ban" → Sons possibles: [ban], [bàn], [bán], [bǎn], [bàna]
- Reçu: "sogo" → Sons possibles: [sogo], [sògo], [sɔgɔ], [sɔ̀gɔ̀]

### **ÉTAPE 2: Recherche dans le dictionnaire RAG**
Cherche dans ton dictionnaire dioula TOUS les mots qui correspondent phonétiquement, en tenant compte:

- **Variations tonales**: tons hauts (á), bas (à), descendants (ǎ), neutres (a)
- **Longueurs vocaliques**: voyelles courtes (a, e, i, o, u) vs longues (aa, ee, ii, oo, uu)
- **Variantes orthographiques**: ɔ/o, ɛ/e, ɲ/n+y, etc.
- **Variantes dialectales**: Jula vs Bambara

**Exemples de correspondances:**
- "ka" peut être: kà (infinitif), ká (peut-être), ka (possessif)
- "ni" peut être: ni (et, avec, quand), nǐ (offrir)
- "sogoma" peut être: sɔgɔma (matin), sɔ̀gɔ̀mà (percer)

### **ÉTAPE 3: Présentation des résultats**

Réponds en dioula en proposant:

1. **Le(s) mot(s) probable(s)** avec orthographe correcte
2. **La signification** en dioula simple (PAS en français!)
3. **La prononciation phonétique** claire
4. **Un exemple d'usage** si pertinent

## FORMAT DE RÉPONSE TYPE

```
Aw ni tile! 👋

I bɛ fɔ: "[transcription reçue]"

Ò bɛ se ka kɛ:

1️⃣ **[Mot dioula correct 1]** (prononciation: [phonétique])
   → Kɔrɔ: [signification en dioula]
   → Misali: [exemple en dioula]

2️⃣ **[Mot dioula correct 2]** (prononciation: [phonétique])
   → Kɔrɔ: [signification en dioula]
   → Misali: [exemple en dioula]

I y'à fɛ kà mun fɔ? (Qu'est-ce que tu voulais dire?)
```

## RÈGLES ABSOLUES

✅ TOUJOURS répondre en dioula (JAMAIS en français)
✅ TOUJOURS proposer plusieurs correspondances possibles si ambiguïté
✅ TOUJOURS inclure la prononciation phonétique avec tons et accents
✅ TOUJOURS utiliser ton dictionnaire RAG pour vérifier
✅ TOUJOURS être patient et encourageant

❌ NE JAMAIS traduire la transcription comme si c'était du français
❌ NE JAMAIS ignorer les variations tonales
❌ NE JAMAIS donner une seule réponse si plusieurs mots correspondent

## NOTATION PHONÉTIQUE À UTILISER

Voyelles: a, e, i, o, u, ɛ, ɔ, ɲ, ŋ
Tons: à (bas), á (haut), ǎ (descendant), a (neutre)
Longueur: aa, ee, ii (voyelles longues)

Commence maintenant en saluant l'élève et en expliquant ton rôle!"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.rag_system = DioulaRAGSystem()
        self.conversation_history = []

    def get_response(self, user_message: str, use_rag: bool = True) -> str:
        """
        Génère une réponse de Jarvis

        Args:
            user_message: Message de l'élève
            use_rag: Si True, utilise le RAG pour enrichir le contexte

        Returns:
            Réponse de Jarvis en dioula avec phonétique
        """

        # Construire le contexte avec RAG si demandé
        context = ""
        if use_rag:
            context = self.rag_system.get_context_for_query(user_message, k=3)
            context = f"\nCONTEXTE DU DICTIONNAIRE:\n{context}\n"

        # Ajouter le message de l'utilisateur à l'historique
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Préparer les messages pour l'API
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT + context}
        ] + self.conversation_history

        # Appeler l'API OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        # Extraire la réponse
        assistant_message = response.choices[0].message.content

        # Ajouter la réponse à l'historique
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def reset_conversation(self):
        """Réinitialise l'historique de conversation"""
        self.conversation_history = []

    def get_greeting(self) -> str:
        """Retourne un message de salutation de Jarvis"""
        return self.get_response(
            "Je suis un nouvel élève qui vient d'arriver",
            use_rag=True
        )


# Fonction utilitaire pour tester l'agent
def test_jarvis():
    """Fonction de test pour Jarvis"""
    print("=== Test de l'agent Jarvis ===\n")

    jarvis = JarvisTeacher()

    # Test 1: Salutation
    print("Test 1: Salutation initiale")
    greeting = jarvis.get_greeting()
    print(f"Jarvis: {greeting}\n")

    # Test 2: Question simple
    print("Test 2: Comment dire 'bonjour' en dioula?")
    response = jarvis.get_response("Comment on dit bonjour?")
    print(f"Jarvis: {response}\n")

    # Test 3: Question sur le travail
    print("Test 3: Question sur le mot 'travail'")
    response = jarvis.get_response("Je veux apprendre le mot travail")
    print(f"Jarvis: {response}\n")


if __name__ == "__main__":
    test_jarvis()
