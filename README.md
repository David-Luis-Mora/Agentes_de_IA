# Gym Assistant AI - Personalized Fitness Recommender

Este proyecto es un asistente de fitness inteligente que utiliza agentes de IA (LangChain) para recomendar rutinas y ejercicios personalizados basados en el perfil del usuario (peso, altura, disponibilidad y objetivos).

## Características principales

- **Agente de IA con LangChain**: Un "Entrenador Virtual" con personalidad profesional que razona sobre tus necesidades.
- **Integración con Wger API**: Consulta una base de datos de ejercicios real para obtener detalles técnicos y grupos musculares.
- **Gym Tracker MCP**: Integración con el protocolo MCP para acceder al historial de entrenamiento y progreso del usuario.
- **Sistema RAG (Retrieval-Augmented Generation)**: El agente fundamenta sus recomendaciones en una base de conocimientos sobre principios de hipertrofia y nutrición.
- **Perfil de Usuario Persistente**: Almacenamiento en base de datos (Django) de las preferencias y medidas del usuario.

## Arquitectura del Sistema

El sistema sigue una arquitectura de 3 capas:
1. **Frontend (API REST)**: Un backend en Django que expone endpoints para chat y gestión de perfiles.
2. **Capa de Agente (LangChain)**: Orquestación del LLM con herramientas personalizadas.
3. **Herramientas Externas**:
    - `Wger API`: Datos de ejercicios.
    - `Gym-Tracker MCP`: Historial de usuario.
    - `RAG Tool`: Conocimiento experto desde documentos locales.

## Tecnologías Utilizadas

- **Backend**: Django, Django REST Framework.
- **IA**: LangChain, Ollama (Gemma 2 / Qwen).
- **Protocolos**: MCP (Model Context Protocol).
- **Base de Datos**: SQLite3.

## Requisitos Previos

- Python 3.10+
- Node.js (para el servidor MCP)
- Ollama (con el modelo `gemma2:9b` o similar descargado)

## Instalación y Ejecución Local

1. **Clonar el repositorio**:
   ```bash
   git clone <repo-url>
   cd Agentes_de_IA
   ```

2. **Configurar el entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurar el servidor MCP**:
   ```bash
   cd gym-tracker-mcp
   npm install
   npm run build
   ```

4. **Variables de Entorno**:
   Copia el archivo `.env.example` a `.env` y completa tus credenciales.

5. **Migraciones de Base de Datos**:
   ```bash
   python manage.py migrate
   ```

6. **Iniciar el servidor**:
   ```bash
   python manage.py runserver
   ```

## Uso del Agente

Puedes interactuar con el agente enviando una petición POST a `/api/chat/`:
```json
{
  "user_id": 1,
  "message": "Hola coach, peso 80kg y quiero ganar músculo. Solo puedo ir 3 días a la semana."
}
```

## Mejoras Futuras
- Implementar persistencia real del historial de chat en la base de datos.
- Añadir soporte para subir imágenes de facturas/comida para análisis calórico.
- Generar archivos PDF con la rutina semanal automáticamente.
