import os
from langchain_core.tools import tool
from agent.utils.vector_manager import VectorManager

# Rutas de archivos basadas en la estructura del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FITNESS_DIR = os.path.join(BASE_DIR, "fitness")
NUTRITION_DIR = os.path.join(FITNESS_DIR, "Nutricion")
AGENT_KB_DIR = os.path.join(BASE_DIR, "agent", "knowledge")
MD_KB_PATH = os.path.join(BASE_DIR, "knowledge_base.md")

# Definición de Colecciones
COLLECTIONS = {
    "training": [
        os.path.join(FITNESS_DIR, "GANAR-MASA-MUSCULAR-Guía-Completa.pdf"),
        os.path.join(FITNESS_DIR, "GUIA-GRATUITA-VOLUMEN-DE-ENTRENAMIENTO.pdf"),
        os.path.join(FITNESS_DIR, "Rutinas_JTPT_.pdf"),
        MD_KB_PATH
    ],
    "exercises": [
        os.path.join(FITNESS_DIR, "Enciclopedia_de_ejercicios_de_musculacion.pdf")
    ],
    "recovery": [
        os.path.join(FITNESS_DIR, "8_sobreentrenamiento_y_recuperacion.pdf")
    ],
    "nutrition": [
        os.path.join(AGENT_KB_DIR, "Manual-nutricion-dietetica-CARBAJAL.pdf"),
        os.path.join(NUTRITION_DIR, "Presentacion-Nutrición-Cesar.pdf"),
        os.path.join(NUTRITION_DIR, "S2173129212700686.pdf")
    ]
}

# Inicializadores de Manager (lazy)
managers = {name: VectorManager(name) for name in COLLECTIONS.keys()}

def get_files_in_dir(directory, extensions=('.pdf', '.md', '.txt')):
    """Lista archivos en un directorio de forma recursiva."""
    files = []
    if not os.path.exists(directory):
        return files
    for root, _, filenames in os.walk(directory):
        for f in filenames:
            if f.endswith(extensions):
                files.append(os.path.join(root, f))
    return files

@tool
def index_new_knowledge(category: str = "all"):
    """
    Escanea los directorios locales y vectoriza archivos nuevos que no hayan sido procesados.
    Categorías: 'training', 'exercises', 'recovery', 'nutrition', 'all'.
    Usa esto si crees que hay información nueva que aún no ha sido indexada.
    """
    target_categories = COLLECTIONS.keys() if category == "all" else [category]
    results = []
    
    for cat in target_categories:
        if cat not in COLLECTIONS:
            continue
            
        # Para categorías que son directorios, escaneamos
        files = COLLECTIONS[cat]
        if cat == "nutrition":
            # Caso especial: Nutrición tiene varios sitios
            files = [os.path.join(AGENT_KB_DIR, "Manual-nutricion-dietetica-CARBAJAL.pdf")]
            files += get_files_in_dir(NUTRITION_DIR)
        
        manager = managers[cat]
        chunk_params = {"chunk_size": 800, "chunk_overlap": 100} if cat == "exercises" else {"chunk_size": 1000, "chunk_overlap": 200}
        
        res = manager.sync_with_files(files, **chunk_params)
        results.append(f"[{cat.upper()}]: {res}")
        
    return "\n".join(results)

def ensure_initialized(collection_name):
    manager = managers[collection_name]
    if manager.get_vectorstore() is None:
        index_new_knowledge(collection_name)
    return manager

@tool
def search_training_advice(query: str):
    """
    Consulta principios de entrenamiento, hipertrofia, sobrecarga progresiva y volumen.
    """
    try:
        manager = ensure_initialized("training")
        return manager.search(query, k=4)
    except Exception as e:
        return f"Error buscando consejos: {str(e)}"

@tool
def search_exercise_technique(query: str):
    """
    Busca técnica de ejercicios específicos en la enciclopedia de musculación.
    """
    try:
        manager = ensure_initialized("exercises")
        return manager.search(query, k=3)
    except Exception as e:
        return f"Error buscando técnica: {str(e)}"

@tool
def search_recovery_and_rest(query: str):
    """
    Busca información sobre sobreentrenamiento, descanso y sueño.
    """
    try:
        manager = ensure_initialized("recovery")
        return manager.search(query, k=3)
    except Exception as e:
        return f"Error buscando recuperación: {str(e)}"

@tool
def search_nutrition_articles(query: str):
    """
    Busca en manuales y artículos sobre nutrición deportiva y dietas.
    """
    try:
        manager = ensure_initialized("nutrition")
        return manager.search(query, k=4)
    except Exception as e:
        return f"Error buscando nutrición: {str(e)}"
