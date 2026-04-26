import os
from langchain_core.tools import tool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base.txt")

@tool
def search_knowledge_base(query: str):
    """
    Busca en la base de conocimientos local consejos de expertos en fitness, principios de hipertrofia e información nutricional.
    Utiliza esto para respaldar tus recomendaciones con principios basados en la ciencia.
    """
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return "Base de conocimientos no encontrada."
    
    with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Para un archivo pequeño, podemos simplemente devolver las secciones relevantes o todo el contenido.
    # Si el archivo crece, implementaremos división en trozos (chunking) y búsqueda por similitud.
    # Por ahora, buscaremos palabras clave.
    
    keywords = query.lower().split()
    lines = content.split('\n')
    relevant_lines = []
    
    for line in lines:
        if any(kw in line.lower() for kw in keywords):
            relevant_lines.append(line)
            
    if not relevant_lines:
        return content[:2000]
        
    return "\n".join(relevant_lines[:20])
