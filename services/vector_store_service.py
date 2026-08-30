import os
import chromadb
from sentence_transformers import SentenceTransformer
from config.settings import DATA_DIR

class VectorStoreService:
    _instance = None
    _client = None
    _collection = None
    _model = None

    def __new__(cls):
        """
        Implements the Singleton pattern to ensure only one ChromaDB persistent client 
        and Sentence Transformer model instance is created across the application lifecycle,
        preventing Chroma instance collision errors.
        """
        if cls._instance is None:
            cls._instance = super(VectorStoreService, cls).__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        """Initializes persistent ChromaDB client and local embedding model once."""
        chroma_path = str(DATA_DIR / "chroma_db")
        os.makedirs(chroma_path, exist_ok=True)
        
        # Initialize persistent client safely
        cls._client = chromadb.PersistentClient(path=chroma_path)
        cls._collection = cls._client.get_or_create_collection(name="pragyan_knowledge_base")
        cls._model = SentenceTransformer('all-MiniLM-L6-v2')

    def __init__(self):
        # Initialization is fully handled by the Singleton __new__ and _initialize methods
        pass

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
            
        embedding = self._model.encode(text).tolist()
        self._collection.upsert(
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
            query_embedding = self._model.encode(query).tolist()
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            documents = results.get("documents", [])
            return documents[0] if documents else []
        except Exception as e:
            print(f"Vector search warning: {str(e)}")
            return []
