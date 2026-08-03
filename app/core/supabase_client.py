from supabase import create_client, Client
from app.core.config import config, settings

def get_supabase() -> Client:
    """
    Retorna un cliente de Supabase inicializado con la URL y clave activa del proyecto.
    """
    return create_client(config.supabase_url, config.supabase_key)

def get_supabase_client() -> Client:
    return get_supabase()

# Instancia global del cliente de Supabase
supabase: Client = get_supabase()
