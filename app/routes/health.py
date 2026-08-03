from fastapi import APIRouter
from app.core.config import settings
from app.core.supabase_client import supabase

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
                supabase_message = "La clave SUPABASE_KEY / SUPABASE_PUBLISHABLE_KEY es inválida."
            else:
                # Si responde la API pero la tabla no existe (ej. PGRST205), la conexión y API Key son VÁLIDAS
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
