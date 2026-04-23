import os
from langchain_core.tools import tool

KNOWLEDGE_BASE_PATH = "/home/inta@informatica.edu/Escritorio/Agentes_de_IA/knowledge_base.txt"

@tool
def search_knowledge_base(query: str):
    """
    Searches the local knowledge base for expert fitness advice, hypertrophy principles, and nutrition information.
    Use this to back up recommendations with science-based principles.
    """
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return "Knowledge base not found."
    
    with open(KNOWLEDGE_BASE_PATH, 'r') as f:
        content = f.read()
    
    # For a small file, we can just return the relevant sections or the whole content
    # If the file grows, implement chunking and similarity search.
    # For now, let's look for keywords.
    
    keywords = query.lower().split()
    lines = content.split('\n')
    relevant_lines = []
    
    for line in lines:
        if any(kw in line.lower() for kw in keywords):
            relevant_lines.append(line)
            
    if not relevant_lines:
        return content[:2000]
        
    return "\n".join(relevant_lines[:20])
