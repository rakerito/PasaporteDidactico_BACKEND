# Backend Pasaporte Didáctico (FastAPI + Supabase)

Backend desarrollado en Python con **FastAPI** preparado para interactuar con la aplicación móvil en **Flutter** y la base de datos en **Supabase**.

## 🚀 Requisitos Previos

- Python 3.9 o superior
- Pip (Gestor de paquetes de Python)

## 🛠️ Configuración del Entorno de Desarrollo

1. **Crear un entorno virtual:**
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual:**
   - En Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - En Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno:**
   Edita el archivo `.env` e ingresa tus credenciales reales de Supabase:
   ```env
   SUPABASE_URL="https://tu-proyecto.supabase.co"
   SUPABASE_KEY="tu-anon-key-de-supabase"
   ```

## 🏃‍♂️ Ejecutar el Servidor

Inicia el servidor en modo desarrollo con recarga automática:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

> **Nota para Flutter:** El parámetro `--host 0.0.0.0` permite que dispositivos o emuladores en la misma red local (o `10.0.2.2` en emulador Android) puedan comunicarse con el servidor local en la IP de tu computadora.

## 📄 Documentación Interactiva de la API

Una vez iniciado el servidor, puedes acceder a la documentación automática de FastAPI en:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📁 Estructura del Proyecto

```text
app/
├── api/          # Routers y endpoints por versión (v1/)
├── core/         # Configuración y cliente Supabase
├── schemas/      # Modelos Pydantic para solicitudes y respuestas
└── main.py       # Punto de entrada de la aplicación FastAPI
```
