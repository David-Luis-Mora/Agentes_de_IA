# 🤖 GymAI - Tu Entrenador Personal con Inteligencia Artificial

![GymAI Banner](https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=1200)

**GymAI** es un asistente de fitness avanzado que utiliza agentes de IA (LangGraph) para diseñar rutinas de entrenamiento personalizadas, ofrecer consejos de nutrición mediante RAG (Generación Aumentada por Recuperación) y gestionar tu progreso físico.

---

## ✨ Características Principales

- 🧠 **Agente de Razonamiento**: Utiliza LangGraph para decidir cuándo buscar ejercicios, cuándo consultar manuales técnicos o cuándo guardar una rutina.
- 🏋️ **Buscador de Ejercicios Híbrido**: Combina datos técnicos de **Wger API** con imágenes y videos en alta definición de **AscendAPI**.
- 📚 **Soporte RAG**: Consulta manuales de nutrición y guías de hipertrofia locales almacenados en archivos PDF y Markdown.
- 💾 **Memoria de Conversación**: Persistencia asíncrona mediante SQLite para que el agente recuerde tus objetivos y lesiones anteriores.
- 📱 **Interfaz Moderna**: Aplicación SPA construida con Vue 3 y Vite, con un diseño premium y reactivo.

---

## 🛠️ Stack Tecnológico

- **IA**: LangChain, LangGraph, Ollama (LLM local), ChromaDB (Vectores).
- **Backend**: Django 5.1 + Django REST Framework.
- **Frontend**: Vue 3 + Pinia + Vite.
- **Base de Datos**: SQLite3 (Memoria y Datos).

---

## 🚀 Guía de Instalación Local

Sigue estos pasos detallados para replicar el proyecto en tu equipo:

### 1. Requisitos Previos
- **Python 3.10+**
- **Node.js 18+**
- **Ollama** (Instalado y ejecutándose)
- **Modelos de Ollama**: `ollama pull qwen2.5:7b` (o el que configures en el código).

### 2. Clonar y Configurar Entorno
```bash
git clone <url-del-repositorio>
cd Agentes_de_IA

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración de Variables de Entorno
Copia el archivo de ejemplo y rellena tus credenciales:
```bash
cp .env.example .env
```
> [!IMPORTANT]
> Edita el archivo `.env` y añade tu `RAPIDAPI_KEY` obtenida en [RapidAPI](https://rapidapi.com/ascendapi/api/edb-with-videos-and-images-by-ascendapi).

### 4. Preparar el Backend
```bash
cd backend
python manage.py migrate
python manage.py runserver
```

### 5. Preparar el Frontend
En otra terminal:
```bash
cd frontend
npm install
npm run dev
```

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una separación clara de responsabilidades:
- `/backend/agent`: Contiene la lógica del cerebro (Factory, Tools y Prompts).
- `/backend/api`: Endpoints de Django que conectan el agente con el mundo exterior.
- `/backend/core`: Modelos de base de datos para perfiles de usuario y rutinas.
- `/frontend`: Interfaz de usuario desacoplada.

---

## 📝 Reflexión Final

### Limitaciones Encontradas
- **Hardware**: El uso de modelos grandes en Ollama (como Qwen 35B) requiere una GPU potente para mantener tiempos de respuesta aceptables bajo 2 minutos.
- **Latencia de APIs**: La dependencia de APIs externas (Wger/Ascend) puede afectar la fluidez si los servidores de terceros están saturados.

### Problemas Solucionados
- Se implementó un flujo asíncrono (`ainvoke`) en Django para evitar el bloqueo del hilo principal durante el razonamiento del agente.
- Se resolvió el mapeo de datos entre dos APIs distintas para ofrecer información visual (videos) y técnica (músculos) en un solo objeto de respuesta.

### Mejoras a Futuro
- **Integración MCP Completa**: Conectar el servidor `gym-tracker-mcp` para que el agente pueda leer el historial de levantamientos reales del usuario.
- **Streaming de Respuestas**: Implementar WebSockets para mostrar el razonamiento del agente en tiempo real en la UI.

---
Creado con ❤️ para la asignatura de Agentes de IA.

