"""
Interface vocale pour le bambara utilisant Djelia AI et ElevenLabs
"""

from pathlib import Path
from typing import Tuple, Optional
import time
from djelia_transcription import DjeliaTranscription
from elevenlabs_agent import ElevenLabsAgent


class BambaraVoiceInterface:
    """
    Interface vocale complète pour le bambara:
    1. Transcription audio avec Djelia AI (reconnaissance vocale bambara)
    2. Conversation avec l'agent ElevenLabs
    3. Réponse audio de l'agent
    """

    def __init__(
        self,
        djelia_api_key: str = "4cc23e20-129b-42a0-af09-ca814e9ac23b",
        elevenlabs_api_key: str = "sk_e08a92815b5e911d119065275c82377c0396f3b0b2d80750",
        elevenlabs_agent_id: str = "agent_7801k3yd7xb4fgfva2r76j2fk9dm"
    ):
        """
        Initialise l'interface vocale bambara

        Args:
            djelia_api_key: Clé API Djelia AI
            elevenlabs_api_key: Clé API ElevenLabs
            elevenlabs_agent_id: ID de l'agent ElevenLabs
        """
        # Initialiser Djelia AI pour la transcription
        self.djelia = DjeliaTranscription(api_key=djelia_api_key)

        # Initialiser ElevenLabs pour l'agent conversationnel
        self.elevenlabs = ElevenLabsAgent(
            api_key=elevenlabs_api_key,
            agent_id=elevenlabs_agent_id
        )

        # Créer le dossier pour les réponses audio
        self.audio_output_dir = Path("./audio_outputs")
        self.audio_output_dir.mkdir(exist_ok=True)

    def process_bambara_voice(
        self,
        audio_file_path: str,
        output_filename: Optional[str] = None
    ) -> Tuple[str, str, str]:
        """
        Traite une entrée vocale en bambara de bout en bout:
        1. Transcription avec Djelia AI (bambara -> texte)
        2. Envoi du texte à l'agent ElevenLabs
        3. Récupération de la réponse (texte et audio)

        Args:
            audio_file_path: Chemin vers le fichier audio d'entrée (bambara)
            output_filename: Nom du fichier audio de sortie (optionnel)

        Returns:
            Tuple (texte_transcrit, réponse_agent, chemin_audio_réponse)
        """
        try:
            # Étape 1: Transcrire l'audio bambara avec Djelia AI
            print("=" * 60)
            print("ÉTAPE 1: Transcription audio avec Djelia AI...")
            print("=" * 60)

            transcript = self.djelia.transcribe_audio(audio_file_path)

            if not transcript:
                error_msg = "Impossible de transcrire l'audio"
                print(f"❌ Erreur: {error_msg}")
                return "", error_msg, ""

            print(f"✅ Transcription réussie: '{transcript}'")

            # Étape 2: Envoyer le texte à l'agent ElevenLabs
            print("\n" + "=" * 60)
            print("ÉTAPE 2: Envoi à l'agent ElevenLabs...")
            print("=" * 60)

            agent_response_data = self.elevenlabs.send_text_message(transcript)

            if not agent_response_data:
                error_msg = "Impossible d'obtenir une réponse de l'agent"
                print(f"❌ Erreur: {error_msg}")
                return transcript, error_msg, ""

            # Extraire la réponse textuelle
            agent_text = (
                agent_response_data.get("message") or
                agent_response_data.get("text") or
                agent_response_data.get("response") or
                str(agent_response_data)
            )

            print(f"✅ Réponse de l'agent: '{agent_text}'")

            # Étape 3: Récupérer l'audio de la réponse
            print("\n" + "=" * 60)
            print("ÉTAPE 3: Récupération de l'audio de réponse...")
            print("=" * 60)

            audio_path = ""

            # Vérifier s'il y a une URL audio dans la réponse
            audio_url = (
                agent_response_data.get("audio_url") or
                agent_response_data.get("audio") or
                agent_response_data.get("output", {}).get("audio_url")
            )

            if audio_url:
                # Télécharger l'audio
                if output_filename is None:
                    output_filename = f"elevenlabs_response_{int(time.time())}.mp3"

                audio_path = str(self.audio_output_dir / output_filename)

                if self.elevenlabs.download_audio_response(audio_url, audio_path):
                    print(f"✅ Audio téléchargé: {audio_path}")
                else:
                    print("⚠️ Impossible de télécharger l'audio")
                    audio_path = ""
            else:
                print("⚠️ Aucune URL audio dans la réponse de l'agent")
                # Optionnel: Générer un audio avec TTS si l'agent ne retourne pas d'audio
                # (nécessiterait d'intégrer ElevenLabs TTS standard)

            print("\n" + "=" * 60)
            print("✅ TRAITEMENT TERMINÉ")
            print("=" * 60)

            return transcript, agent_text, audio_path

        except Exception as e:
            error_msg = f"Erreur lors du traitement: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            return "", error_msg, ""

    def process_with_fallback_tts(
        self,
        audio_file_path: str,
        fallback_voice_interface=None,
        output_filename: Optional[str] = None
    ) -> Tuple[str, str, str]:
        """
        Traite une entrée vocale avec un fallback vers OpenAI TTS si ElevenLabs ne retourne pas d'audio

        Args:
            audio_file_path: Chemin vers le fichier audio d'entrée
            fallback_voice_interface: Instance de VoiceInterface (OpenAI) pour le fallback TTS
            output_filename: Nom du fichier audio de sortie (optionnel)

        Returns:
            Tuple (texte_transcrit, réponse_agent, chemin_audio_réponse)
        """
        transcript, response, audio_path = self.process_bambara_voice(
            audio_file_path,
            output_filename
        )

        # Si pas d'audio et qu'on a une interface de fallback, générer l'audio
        if not audio_path and fallback_voice_interface and response:
            print("\n⚠️ Utilisation du TTS de fallback (OpenAI)...")

            if output_filename is None:
                output_filename = f"fallback_tts_{int(time.time())}.mp3"

            audio_path = fallback_voice_interface.text_to_speech(
                text=response,
                output_filename=output_filename,
                voice="alloy"
            )

            if audio_path:
                print(f"✅ Audio généré avec le fallback: {audio_path}")

        return transcript, response, audio_path


# Fonction de test
def test_bambara_voice_interface():
    """Fonction de test pour l'interface vocale bambara"""
    print("=" * 60)
    print("TEST DE L'INTERFACE VOCALE BAMBARA")
    print("=" * 60)
    print()

    interface = BambaraVoiceInterface()

    print("✅ Interface vocale bambara initialisée avec succès!")
    print()
    print("Configuration:")
    print(f"  - Djelia AI: Activé (transcription bambara)")
    print(f"  - ElevenLabs Agent ID: agent_7801k3yd7xb4fgfva2r76j2fk9dm")
    print(f"  - Dossier de sortie: {interface.audio_output_dir}")
    print()
    print("Pour tester complètement, fournissez un fichier audio en bambara.")
    print()


if __name__ == "__main__":
    test_bambara_voice_interface()
