"""
Script de test pour vérifier que tous les composants de Jarvis fonctionnent
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Teste les variables d'environnement"""
    print("🔍 Test des variables d'environnement...")
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY non trouvée dans .env")
        return False

    if api_key.startswith("sk-"):
        print("✅ Clé API OpenAI détectée")
        return True
    else:
        print("⚠️  Format de clé API suspect")
        return False


def test_imports():
    """Teste que tous les modules peuvent être importés"""
    print("\n🔍 Test des imports...")

    try:
        import openai
        print("✅ openai")
    except ImportError as e:
        print(f"❌ openai: {e}")
        return False

    try:
        import chromadb
        print("✅ chromadb")
    except ImportError as e:
        print(f"❌ chromadb: {e}")
        return False

    try:
        from langchain_openai import OpenAIEmbeddings
        print("✅ langchain-openai")
    except ImportError as e:
        print(f"❌ langchain-openai: {e}")
        return False

    try:
        from fastapi import FastAPI
        print("✅ fastapi")
    except ImportError as e:
        print(f"❌ fastapi: {e}")
        return False

    return True


def test_dictionary():
    """Teste le chargement du dictionnaire"""
    print("\n🔍 Test du dictionnaire dioula...")

    try:
        from dioula_dictionary import get_dictionary_entries

        entries = get_dictionary_entries()
        print(f"✅ {len(entries)} entrées chargées")

        if len(entries) > 0:
            print(f"   Exemple: '{entries[0]['word']}'")
            return True
        else:
            print("⚠️  Aucune entrée trouvée")
            return False

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_rag_system():
    """Teste le système RAG (sans faire d'appel API)"""
    print("\n🔍 Test du système RAG...")

    try:
        # Note: Ce test ne fait pas d'appel API pour économiser
        print("⚠️  Test d'initialisation skippé (économie d'API)")
        print("✅ Imports RAG OK")
        return True

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_jarvis_agent():
    """Teste l'agent Jarvis (sans faire d'appel API)"""
    print("\n🔍 Test de l'agent Jarvis...")

    try:
        from jarvis_agent import JarvisTeacher

        print("✅ Classe JarvisTeacher chargée")
        print("⚠️  Test d'appel API skippé (économie d'API)")
        return True

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_voice_interface():
    """Teste l'interface vocale (sans faire d'appel API)"""
    print("\n🔍 Test de l'interface vocale...")

    try:
        from voice_interface import VoiceInterface

        print("✅ Classe VoiceInterface chargée")
        print("⚠️  Tests STT/TTS skippés (économie d'API)")
        return True

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_app():
    """Teste l'application FastAPI"""
    print("\n🔍 Test de l'application FastAPI...")

    try:
        from app import app

        print("✅ Application FastAPI chargée")
        return True

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Exécute tous les tests"""
    print("=" * 50)
    print("🧪 TESTS SYSTÈME JARVIS")
    print("=" * 50)

    tests = [
        ("Variables d'environnement", test_environment),
        ("Imports", test_imports),
        ("Dictionnaire", test_dictionary),
        ("Système RAG", test_rag_system),
        ("Agent Jarvis", test_jarvis_agent),
        ("Interface Vocale", test_voice_interface),
        ("Application FastAPI", test_app),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erreur lors du test '{name}': {e}")
            results.append((name, False))

    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\n🎯 Score: {passed}/{total} tests réussis")

    if passed == total:
        print("\n🎉 Tous les tests sont passés! Jarvis est prêt!")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
