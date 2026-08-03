from fastapi import APIRouter
from app.core.config import settings
from app.core.supabase import supabase

router = APIRouter()

@router.get("/health", summary="Verificación de estado de la API y Supabase")
def health_check():
    supabase_status = "not_configured"
    supabase_message = "URL por defecto"

    if settings.SUPABASE_URL != "https://tu-proyecto.supabase.co":
        try:
            # Intento de consulta ligera a Supabase
            supabase.from_("_test_ping").select("*").limit(1).execute()
            supabase_status = "connected"
            supabase_message = "Conexión exitosa"
        except Exception as e:
            err_str = str(e)
            if "Invalid API key" in err_str or "401" in err_str:
                supabase_status = "invalid_key"
                supabase_message = "La clave SUPABASE_KEY en .env / config.py es inválida. Revisa tu Supabase Dashboard -> Project Settings -> API (usa la clave 'anon public')."
            else:
                # Si responde la API pero la tabla no existe, la conexión y API Key SON VÁLIDAS.
                supabase_status = "connected"
                supabase_message = "Conectado correctamente a Supabase"

    return {
        "status": "ok",
        "app_name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "supabase": {
            "url": settings.SUPABASE_URL,
            "status": supabase_status,
            "message": supabase_message
        }
    }

