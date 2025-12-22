"""
Interface vocale utilisant les API OpenAI Speech-to-Text et Text-to-Speech
"""

import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class VoiceInterface:
    """Gère les interactions vocales avec Jarvis"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.audio_output_dir = Path("./audio_outputs")
        self.audio_output_dir.mkdir(exist_ok=True)

    def speech_to_text(self, audio_file_path: str, language: str = "fr") -> str:
        """
        Convertit un fichier audio en texte en utilisant Whisper d'OpenAI

        Args:
            audio_file_path: Chemin vers le fichier audio
            language: Langue de l'audio (par défaut: français)

        Returns:
            Texte transcrit
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="text"
                )

            return transcript

        except Exception as e:
            print(f"Erreur lors de la transcription: {e}")
            return ""

    def text_to_speech(
        self,
        text: str,
        output_filename: str = "response.mp3",
        voice: str = "alloy",
        model: str = "tts-1"
    ) -> str:
        """
        Convertit du texte en audio en utilisant l'API TTS d'OpenAI

        Args:
            text: Texte à convertir en parole
            output_filename: Nom du fichier de sortie
            voice: Voix à utiliser (alloy, echo, fable, onyx, nova, shimmer)
            model: Modèle TTS (tts-1 ou tts-1-hd)

        Returns:
            Chemin vers le fichier audio généré
        """
        try:
            # Créer le chemin complet du fichier de sortie
            output_path = self.audio_output_dir / output_filename

            # Générer l'audio
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                speed=0.9  # Légèrement plus lent pour une meilleure compréhension
            )

            # Sauvegarder l'audio
            response.stream_to_file(str(output_path))

            print(f"Audio généré: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"Erreur lors de la génération audio: {e}")
            return ""

    def process_voice_input(
        self,
        audio_file_path: str,
        jarvis_agent,
        output_filename: str = None
    ) -> tuple[str, str, str]:
        """
        Traite une entrée vocale complète: STT -> Agent -> TTS

        Args:
            audio_file_path: Chemin vers le fichier audio d'entrée
            jarvis_agent: Instance de JarvisTeacher
            output_filename: Nom du fichier audio de sortie (optionnel)

        Returns:
            Tuple (texte_transcrit, réponse_jarvis, chemin_audio_sortie)
        """

        # 1. Speech-to-Text
        print("Transcription de l'audio...")
        user_text = self.speech_to_text(audio_file_path)

        if not user_text:
            return "", "Désolé, je n'ai pas pu comprendre l'audio.", ""

        print(f"Élève a dit: {user_text}")

        # 2. Obtenir la réponse de Jarvis
        print("Jarvis réfléchit...")
        jarvis_response = jarvis_agent.get_response(user_text)
        print(f"Jarvis répond: {jarvis_response}")

        # 3. Text-to-Speech
        if output_filename is None:
            import time
            output_filename = f"jarvis_response_{int(time.time())}.mp3"

        print("Génération de l'audio de réponse...")
        audio_output_path = self.text_to_speech(
            text=jarvis_response,
            output_filename=output_filename,
            voice="alloy"
        )

        return user_text, jarvis_response, audio_output_path


# Fonction de test
def test_voice_interface():
    """Fonction de test pour l'interface vocale"""
    print("=== Test de l'interface vocale ===\n")

    # Créer un fichier audio de test (simulation)
    print("Note: Pour un test complet, fournissez un fichier audio réel.")
    print("Format accepté: mp3, mp4, mpeg, mpga, m4a, wav, webm")


if __name__ == "__main__":
    test_voice_interface()
