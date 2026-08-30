import os
import chromadb
from sentence_transformers import SentenceTransformer
from config.settings import DATA_DIR

class VectorStoreService:
    def __init__(self):
        """
        Initializes a local persistent ChromaDB client and loads the lightweight 
        sentence-transformers embedding model ('all-MiniLM-L6-v2') for semantic retrieval.
        """
        chroma_path = str(DATA_DIR / "chroma_db")
        os.makedirs(chroma_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.client.get_or_create_collection(name="pragyan_knowledge_base")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_document(self, doc_id: str, text: str, metadata: dict = None):
        """
        Embeds and stores text chunks into the local ChromaDB vector store.
        
        Args:
            doc_id (str): Unique identifier for the document chunk.
            text (str): Raw text content extracted via OCR or document loaders.
            metadata (dict, optional): Associated metadata (e.g., source file, category).
        """
        if not text.strip():
            return
            
        embedding = self.model.encode(text).tolist()
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {"source": "uploaded_document"}]
        )

    def similarity_search(self, query: str, n_results: int = 3) -> list:
        """
        Executes semantic vector similarity search over stored institutional documents.
        
        Args:
            query (str): User conversational prompt or search query.
            n_results (int): Number of top matching document chunks to return.
            
        Returns:
            list: List of matching document text strings.
        """
        if not query.strip():
            return []
            
        try:
            query_embedding = self.model.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            documents = results.get("documents", [])
            return documents[0] if documents else []
        except Exception as e:
            print(f"Vector search warning (collection may be empty): {str(e)}")
            return []
