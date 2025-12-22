"""
Système RAG (Retrieval-Augmented Generation) pour le dictionnaire dioula
"""

import os
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from dioula_dictionary import get_dictionary_entries
from dotenv import load_dotenv

load_dotenv()

class DioulaRAGSystem:
    """Système RAG pour rechercher dans le dictionnaire dioula"""

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialiser les embeddings OpenAI
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=self.openai_api_key,
            model="text-embedding-3-small"
        )

        # Chemin pour stocker la base de données vectorielle
        self.persist_directory = "./chroma_db"

        # Charger ou créer la base de données vectorielle
        self.vectorstore = self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialise ou charge la base de données vectorielle"""

        # Charger les entrées du dictionnaire
        entries = get_dictionary_entries()

        # Préparer les documents pour ChromaDB
        documents = []
        metadatas = []

        for entry in entries:
            documents.append(entry["full_entry"])
            metadatas.append({
                "word": entry["word"],
                "context": entry["context"]
            })

        # Créer le vectorstore avec ChromaDB
        vectorstore = Chroma.from_texts(
            texts=documents,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=self.persist_directory
        )

        return vectorstore

    def search_dictionary(self, query: str, k: int = 5) -> List[Dict]:
        """
        Recherche dans le dictionnaire dioula

        Args:
            query: Le texte à rechercher (en français ou dioula)
            k: Nombre de résultats à retourner

        Returns:
            Liste de dictionnaires contenant les entrées pertinentes
        """
        results = self.vectorstore.similarity_search(query, k=k)

        formatted_results = []
        for doc in results:
            formatted_results.append({
                "content": doc.page_content,
                "word": doc.metadata.get("word", ""),
                "metadata": doc.metadata
            })

        return formatted_results

    def get_context_for_query(self, query: str, k: int = 5) -> str:
        """
        Récupère le contexte pertinent pour une requête

        Returns:
            String formaté avec les entrées du dictionnaire pertinentes
        """
        results = self.search_dictionary(query, k=k)

        if not results:
            return "Aucune entrée pertinente trouvée dans le dictionnaire."

        context = "Entrées du dictionnaire dioula pertinentes:\n\n"
        for i, result in enumerate(results, 1):
            context += f"--- Entrée {i} ---\n"
            context += result["content"]
            context += "\n\n"

        return context


if __name__ == "__main__":
    # Test du système RAG
    print("Initialisation du système RAG...")
    rag = DioulaRAGSystem()

    print("\nTest de recherche: 'bonjour'")
    results = rag.search_dictionary("bonjour", k=3)
    for result in results:
        print(f"\nMot: {result['word']}")
        print(f"Contenu: {result['content'][:200]}...")
