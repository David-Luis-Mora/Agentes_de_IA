import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_PATH = os.path.join(BASE_DIR, "Manual-nutricion-dietetica-CARBAJAL.pdf")
CHROMA_DIR = os.path.join(BASE_DIR, "data", "nutrition_chroma_pdf")

def initialize_vector_store():
    """
    Inicializa o carga el almacén de vectores Chroma con conocimientos de nutrición del PDF.
    """
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large",
        base_url="http://localhost:11434",
    )

    if not os.path.exists(CHROMA_DIR):
        print("Inicializando nuevo Almacén de Vectores de Nutrición desde PDF...")
        if not os.path.exists(KB_PATH):
             return None
        
        loader = PyPDFLoader(KB_PATH)
        documents = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DIR,
            collection_name="nutrition_knowledge"
        )
        return vectorstore
    else:
        return Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings,
            collection_name="nutrition_knowledge"
        )

# ¿Inicializar globalmente o dentro de la herramienta?
# Por rendimiento, lo hacemos una sola vez.
_vectorstore = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = initialize_vector_store()
    return _vectorstore

@tool
def search_nutrition_knowledge(query: str):
    """
    Busca en la base de conocimientos de nutrición recomendaciones sobre dietas,
    ingesta de proteínas y suplementación.
    """
    try:
        vs = get_vectorstore()
        if vs is None:
            return "El manual de nutrición no está disponible."
            
        results = vs.similarity_search(query, k=2)
        content = "\n\n".join([doc.page_content for doc in results])
        return content
    except Exception as e:
        return f"Error al buscar en la base de conocimientos de nutrición: {str(e)}"
