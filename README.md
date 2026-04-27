# 🤖 GymAI - Tu Entrenador Personal Inteligente

![GymAI Banner](https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=1200)

**GymAI** es un asistente de fitness revolucionario que combina la potencia de **LangChain**, **Django** y **Vue 3** para ofrecerte planes de entrenamiento y nutrición personalizados. Utiliza Agentes de IA avanzados que razonan sobre tus objetivos, nivel de experiencia y disponibilidad para guiarte en tu camino hacia una vida más saludable.

---

## ✨ Características Principales

- 🧠 **Agente de IA Experto**: Utiliza LangGraph para una orquestación sofisticada de tareas y razonamiento.
- 🏋️ **Buscador de Ejercicios**: Integración en tiempo real con la **API de Wger** para detalles técnicos y videos.
- 📈 **Seguimiento MCP (Model Context Protocol)**: Acceso a tu historial de progreso mediante el servidor Gym-Tracker.
- 💾 **Memoria a Largo Plazo**: Persistencia de conversaciones y datos de usuario mediante SQLite (Async).
- 📚 **RAG (Retrieval-Augmented Generation)**: Consulta manuales de nutrición y bases de conocimiento locales.
- 📱 **Interfaz Moderna**: Frontend reactivo construido con Vue 3 y Vite.

---

## 🚀 Guía de Instalación Rápida

Sigue estos pasos para recrear el proyecto completo en tu máquina local:

### 1. Clonar el repositorio principal
```bash
git clone <url-de-este-repositorio>
cd Agentes_de_IA
```

### 2. Configuración del Backend (Python)
Se recomienda usar un entorno virtual:
```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias consolidadas
pip install -r requirements.txt
```

### 3. Configuración del Servidor MCP (Node.js)
El "Gym Tracker MCP" es esencial para el seguimiento de progreso:
```bash
cd backend
git clone https://github.com/nicosaporiti/gym-tracker-mcp.git
cd gym-tracker-mcp

# Instalar y compilar
npm install
cp .env.example .env
# IMPORTANTE: Edita el .env con tus credenciales de Supabase
npm run build
```

### 4. Configuración del Frontend (Vue 3)
```bash
cd ../../frontend
npm install
npm run dev
```

### 5. Iniciar la aplicación
En una nueva terminal (con el backend activo):
```bash
cd backend
python manage.py migrate
python manage.py runserver
```

---

## ⚙️ Estructura del Proyecto

- `/backend`: Servidor Django REST Framework y lógica del Agente GymAI.
- `/frontend`: Aplicación cliente en Vue 3.
- `/backend/gym-tracker-mcp`: Servidor externo para la gestión de historial.
- `/backend/data`: Almacén de base de datos de vectores (Chroma) y memoria de chat (SQLite).

---

## 🔑 Variables de Entorno

Asegúrate de configurar los archivos `.env` tanto en el backend como en el servidor MCP para que las integraciones funcionen correctamente.

---

## 🛠️ Stack Tecnológico

- **IA**: LangChain, LangGraph, Ollama, ChromaDB.
- **Backend**: Django 5.1+, Python 3.10+.
- **Frontend**: Vue 3, Vite, Pinia.
- **Base de Datos**: SQLite3 / Supabase (para MCP).

---

Creado con ❤️ por el equipo de Agentes de IA.
