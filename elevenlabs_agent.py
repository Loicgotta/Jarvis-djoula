"""
Module d'intégration avec l'agent conversationnel ElevenLabs
"""

import requests
import json
from typing import Optional, Dict, Any
import time


class ElevenLabsAgent:
    """Gère les conversations avec un agent ElevenLabs"""

    def __init__(self, api_key: str, agent_id: str):
        """
        Initialise le client ElevenLabs

        Args:
            api_key: Clé API ElevenLabs
            agent_id: ID de l'agent conversationnel
        """
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = "https://api.elevenlabs.io/v1"

    def get_signed_url(self) -> Optional[str]:
        """
        Obtient une URL signée pour la conversation

        Returns:
            URL signée ou None en cas d'erreur
        """
        try:
            headers = {
                "xi-api-key": self.api_key
            }

            response = requests.get(
                f"{self.base_url}/convai/conversation/get_signed_url",
                params={"agent_id": self.agent_id},
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("signed_url")
            else:
                print(f"Erreur lors de l'obtention de l'URL signée: {response.status_code}")
                print(f"Détails: {response.text}")
                return None

        except Exception as e:
            print(f"Erreur lors de l'obtention de l'URL signée: {e}")
            return None

    def send_text_message(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Envoie un message texte à l'agent et reçoit une réponse

        Note: Cette méthode utilise une approche simplifiée.
        Pour une implémentation WebSocket complète, utilisez le SDK Python d'ElevenLabs.

        Args:
            text: Texte à envoyer à l'agent

        Returns:
            Réponse de l'agent (texte et/ou audio) ou None en cas d'erreur
        """
        try:
            # Pour le moment, nous utilisons une approche simple
            # Dans une implémentation complète, on utiliserait WebSocket

            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }

            # Créer une conversation
            conversation_data = {
                "agent_id": self.agent_id,
                "text": text
            }

            print(f"Envoi du message à l'agent ElevenLabs: {text}")

            # Note: L'endpoint exact peut varier selon la documentation ElevenLabs
            # Cette implémentation est une approximation basée sur les APIs courantes
            response = requests.post(
                f"{self.base_url}/convai/conversation",
                headers=headers,
                json=conversation_data,
                timeout=30
            )

            if response.status_code in [200, 201]:
                result = response.json()
                print("Réponse reçue de l'agent ElevenLabs")
                return result
            else:
                print(f"Erreur lors de l'envoi du message: {response.status_code}")
                print(f"Détails: {response.text}")
                return None

        except Exception as e:
            print(f"Erreur lors de l'envoi du message à l'agent: {e}")
            return None

    def get_text_response(self, user_message: str) -> Optional[str]:
        """
        Obtient une réponse textuelle de l'agent

        Args:
            user_message: Message de l'utilisateur

        Returns:
            Réponse textuelle de l'agent ou None en cas d'erreur
        """
        response = self.send_text_message(user_message)

        if response:
            # Extraire la réponse textuelle (la structure exacte dépend de l'API)
            text_response = (
                response.get("message") or
                response.get("text") or
                response.get("response") or
                response.get("output", {}).get("text")
            )
            return text_response

        return None

    def get_audio_response_url(self, user_message: str) -> Optional[str]:
        """
        Obtient l'URL de la réponse audio de l'agent

        Args:
            user_message: Message de l'utilisateur

        Returns:
            URL du fichier audio ou None en cas d'erreur
        """
        response = self.send_text_message(user_message)

        if response:
            # Extraire l'URL audio (la structure exacte dépend de l'API)
            audio_url = (
                response.get("audio_url") or
                response.get("audio") or
                response.get("output", {}).get("audio_url")
            )
            return audio_url

        return None

    def download_audio_response(self, audio_url: str, output_path: str) -> bool:
        """
        Télécharge la réponse audio de l'agent

        Args:
            audio_url: URL du fichier audio
            output_path: Chemin où sauvegarder l'audio

        Returns:
            True si le téléchargement a réussi, False sinon
        """
        try:
            response = requests.get(audio_url, timeout=30)

            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"Audio téléchargé: {output_path}")
                return True
            else:
                print(f"Erreur lors du téléchargement de l'audio: {response.status_code}")
                return False

        except Exception as e:
            print(f"Erreur lors du téléchargement de l'audio: {e}")
            return False


# Fonction de test
def test_elevenlabs_agent():
    """Fonction de test pour l'agent ElevenLabs"""
    print("=== Test de l'agent ElevenLabs ===\n")

    api_key = "sk_e08a92815b5e911d119065275c82377c0396f3b0b2d80750"
    agent_id = "agent_7801k3yd7xb4fgfva2r76j2fk9dm"

    agent = ElevenLabsAgent(api_key, agent_id)

    print("Module ElevenLabs initialisé avec succès!")
    print(f"Agent ID: {agent_id}")


if __name__ == "__main__":
    test_elevenlabs_agent()
