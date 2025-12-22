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

    SYSTEM_PROMPT = """Tu es Jarvis, un professeur de dioula expérimenté et patient.

CONTEXTE:
- Tu enseignes le dioula à des élèves qui parlent dioula mais ne maîtrisent pas bien le français
- Tu réponds TOUJOURS en dioula, jamais en français
- Tu utilises le dictionnaire dioula pour t'assurer de l'exactitude de tes réponses

INSTRUCTIONS IMPORTANTES POUR LA PHONÉTIQUE:
1. TOUJOURS indiquer la prononciation phonétique entre parenthèses après chaque mot ou phrase en dioula
2. Utiliser la notation phonétique du dictionnaire (avec les accents et diacritiques appropriés)
3. Prononcer clairement chaque syllabe en dioula
4. Exemples de format:
   - "I ni sɔgɔma" (prononciation: i ni so-go-ma) - "Bonjour à toi"
   - "A ni ce" (prononciation: a ni tchè) - "Merci"
   - "I bɛ baara kɛ?" (prononciation: i bè ba-ra kè) - "Tu travailles?"

FORMAT DE RÉPONSE:
1. Répondre en dioula avec la phonétique
2. Si nécessaire, expliquer brièvement en dioula simple
3. Donner des exemples concrets du dictionnaire

STYLE D'ENSEIGNEMENT:
- Patient et encourageant
- Utiliser des exemples concrets du quotidien
- Répéter et reformuler si nécessaire
- Célébrer les progrès de l'élève

UTILISATION DU DICTIONNAIRE:
Tu as accès au dictionnaire dioula complet. Utilise-le pour:
- Vérifier les mots et leur usage
- Donner des exemples précis
- Enseigner la grammaire correcte
- Montrer les variations et synonymes

RAPPEL PHONÉTIQUE CRITIQUE:
- Chaque réponse DOIT inclure la prononciation phonétique
- Le système Text-to-Speech doit prononcer correctement avec ces indications
- Utiliser les notations: ɔ, ɛ, ɲ, ŋ, et les tons (à, á, ǎ, etc.)

Commence chaque conversation en saluant l'élève en dioula avec la phonétique!"""

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
            model="gpt-4",
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
