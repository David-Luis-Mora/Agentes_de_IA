import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import logging

logger = logging.getLogger(__name__)

# Configuración centralizada
OLLAMA_BASE_URL = "http://192.168.117.48:11434" 
EMBEDDING_MODEL = "mxbai-embed-large"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VECTOR_STORES_DIR = os.path.join(BASE_DIR, "data", "vector_stores")

class VectorManager:
    def __init__(self, collection_name, persistent_dir=None):
        self.collection_name = collection_name
        self.persistent_dir = persistent_dir or os.path.join(VECTOR_STORES_DIR, collection_name)
        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        self._vectorstore = None

    def get_vectorstore(self):
        if self._vectorstore is None:
            if os.path.exists(self.persistent_dir):
                self._vectorstore = Chroma(
                    persist_directory=self.persistent_dir,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
            else:
                self._vectorstore = None
        return self._vectorstore

    def sync_with_files(self, file_paths, chunk_size=1000, chunk_overlap=200):
        """
        Sincroniza la base de datos con una lista de archivos.
        Añade solo archivos que no estén ya procesados (basado en metadatos básicos).
        """
        vs = self.get_vectorstore()
        
        # Obtener archivos ya procesados si existe el almacén
        processed_files = set()
        if vs:
            # intentamos obtener metadatos de los documentos
            data = vs.get()
            if data and 'metadatas' in data:
                for meta in data['metadatas']:
                    if 'source' in meta:
                        processed_files.add(meta['source'])

        files_to_add = [p for p in file_paths if os.path.exists(p) and p not in processed_files]
        
        if not files_to_add:
            return f"Colección {self.collection_name} ya está al día."

        logger.info(f"Añadiendo {len(files_to_add)} archivos nuevos a {self.collection_name}...")
        
        documents = []
        for path in files_to_add:
            try:
                if path.endswith('.pdf'):
                    loader = PyPDFLoader(path)
                elif path.endswith('.md') or path.endswith('.txt'):
                    loader = TextLoader(path, encoding='utf-8')
                else:
                    continue
                documents.extend(loader.load())
            except Exception as e:
                logger.error(f"Error cargando {path}: {e}")

        if not documents:
            return "No hay documentos nuevos válidos para añadir."

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_documents(documents)

        if vs:
            vs.add_documents(chunks)
        else:
            os.makedirs(self.persistent_dir, exist_ok=True)
            self._vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.persistent_dir,
                collection_name=self.collection_name
            )
        
        return f"Éxito: Se han vectorizado {len(files_to_add)} archivos nuevos en {self.collection_name}."

    def search(self, query, k=3):
        vs = self.get_vectorstore()
        if vs is None:
            return "Base de conocimientos todavía no inicializada."
        
        results = vs.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in results])
