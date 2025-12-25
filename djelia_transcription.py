"""
Module d'intégration avec l'API Djelia AI pour la transcription vocale en bambara
"""

import requests
from pathlib import Path
from typing import Optional


class DjeliaTranscription:
    """Gère la transcription vocale en bambara via l'API Djelia AI"""

    def __init__(self, api_key: str):
        """
        Initialise le client Djelia AI

        Args:
            api_key: Clé API pour Djelia AI
        """
        self.api_key = api_key
        self.base_url = "https://djelia.cloud/api/v1"
        self.transcribe_endpoint = f"{self.base_url}/models/transcribe"

    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """
        Transcrit un fichier audio en bambara

        Args:
            audio_file_path: Chemin vers le fichier audio à transcrire

        Returns:
            Texte transcrit ou None en cas d'erreur
        """
        try:
            # Vérifier que le fichier existe
            audio_path = Path(audio_file_path)
            if not audio_path.exists():
                print(f"Erreur: Le fichier {audio_file_path} n'existe pas")
                return None

            # Préparer les headers avec la clé API
            headers = {
                "x-api-key": self.api_key
            }

            # Ouvrir et envoyer le fichier audio
            with open(audio_file_path, "rb") as audio_file:
                files = {
                    "file": (audio_path.name, audio_file, self._get_mime_type(audio_path.suffix))
                }

                print(f"Envoi du fichier audio à Djelia AI pour transcription...")
                response = requests.post(
                    self.transcribe_endpoint,
                    headers=headers,
                    files=files,
                    timeout=30
                )

            # Vérifier la réponse
            if response.status_code == 200:
                result = response.json()
                # La structure exacte de la réponse peut varier, ajuster selon la documentation
                transcript = result.get("text") or result.get("transcript") or result.get("transcription")

                if transcript:
                    print(f"Transcription réussie: {transcript}")
                    return transcript
                else:
                    print(f"Réponse inattendue de l'API: {result}")
                    return None
            else:
                print(f"Erreur lors de la transcription: {response.status_code}")
                print(f"Détails: {response.text}")
                return None

        except requests.exceptions.Timeout:
            print("Erreur: Délai d'attente dépassé lors de la transcription")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête à Djelia AI: {e}")
            return None
        except Exception as e:
            print(f"Erreur inattendue lors de la transcription: {e}")
            return None

    def _get_mime_type(self, file_extension: str) -> str:
        """
        Retourne le type MIME basé sur l'extension du fichier

        Args:
            file_extension: Extension du fichier (ex: .mp3, .wav)

        Returns:
            Type MIME correspondant
        """
        mime_types = {
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".m4a": "audio/m4a",
            ".webm": "audio/webm",
            ".ogg": "audio/ogg",
            ".flac": "audio/flac"
        }
        return mime_types.get(file_extension.lower(), "audio/mpeg")


# Fonction de test
def test_djelia_transcription():
    """Fonction de test pour la transcription Djelia"""
    print("=== Test de la transcription Djelia AI ===\n")

    # Note: Remplacer par votre vraie clé API pour tester
    api_key = "4cc23e20-129b-42a0-af09-ca814e9ac23b"
    djelia = DjeliaTranscription(api_key)

    print("Module Djelia AI initialisé avec succès!")
    print("Pour tester, fournissez un fichier audio en bambara.")


if __name__ == "__main__":
    test_djelia_transcription()
