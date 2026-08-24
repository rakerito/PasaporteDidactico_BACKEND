from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_docente)


# =====================================
# CONSULTAS
# =====================================

def obtener_por_id(id_docente: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_docente", id_docente)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar docente: {e}"
        )


def obtener_por_usuario(id_usuario1: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_usuario1", id_usuario1)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar docente por usuario: {e}"
        )


def listar():
    try:
        res = (
            _table()
            .select("*")
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar docentes: {e}"
        )


def listar_por_division(division: str):
    try:
        res = (
            _table()
            .select("*")
            .ilike("division", f"%{division}%")
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar docentes por división: {e}"
        )


# =====================================
# CRUD
# =====================================

def crear(datos: dict):
    try:
        if not datos:
            raise HTTPException(
                status_code=400,
                detail="No se recibieron datos."
            )

        # Un usuario solo debería tener un perfil de docente
        existe = obtener_por_usuario(datos["id_usuario1"])

        if existe:
            raise HTTPException(
                status_code=409,
                detail="Este usuario ya tiene un perfil de docente."
            )

        datos = jsonable_encoder(datos)

        res = (
            _table()
            .insert(datos)
            .execute()
        )
        return res.data[0]

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear docente: {e}"
        )


def actualizar(id_docente: int, datos: dict):
    try:
        if not datos:
            raise HTTPException(
                status_code=400,
                detail="No se recibieron datos."
            )

        datos = jsonable_encoder(datos)

        res = (
            _table()
            .update(datos)
            .eq("id_docente", id_docente)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar docente: {e}"
        )


def eliminar(id_docente: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_docente", id_docente)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar docente: {e}"
        )

def estadisticas(id_docente: int):
    """
    Calcula, para un docente:
    - cursos_completados: número de tomas con estatus 'Completado'
    - logros_obtenidos: sellos distintos + constancias ya cumplidas
    - nivel: según el número de cursos completados
    """
    try:
        sb = get_supabase()

        # --- Cursos completados y sellos obtenidos ---
        tomas = (
            sb.schema(config.supabase_schema)
            .table(config.supabase_toma)
            .select("id_curso1")
            .eq("id_docente1", id_docente)
            .ilike("estatus", "completado")
            .execute()
        )

        cursos_completados = len(tomas.data)
        ids_curso = [t["id_curso1"] for t in tomas.data]

        sellos_obtenidos_ids = set()
        if ids_curso:
            cursos = (
                sb.schema(config.supabase_schema)
                .table(config.supabase_curso)
                .select("id_sello1")
                .in_("id_curso", ids_curso)
                .execute()
            )
            sellos_obtenidos_ids = {c["id_sello1"] for c in cursos.data if c.get("id_sello1")}

        # --- Constancias ya cumplidas: todas cuyos sellos requeridos ya se tienen ---
        constancias_obtenidas = 0
        if sellos_obtenidos_ids:
            otorga = (
                sb.schema(config.supabase_schema)
                .table(config.supabase_otorga)
                .select("id_sello2, id_constancia1")
                .execute()
            )

            requeridos_por_constancia: dict[int, set[int]] = {}
            for fila in otorga.data:
                requeridos_por_constancia.setdefault(fila["id_constancia1"], set()).add(fila["id_sello2"])

            for requeridos in requeridos_por_constancia.values():
                if requeridos and requeridos.issubset(sellos_obtenidos_ids):
                    constancias_obtenidas += 1

        logros_obtenidos = len(sellos_obtenidos_ids) + constancias_obtenidas

        # Regla de nivel basada en CURSOS COMPLETADOS (catálogo de 50+ cursos).
        if cursos_completados >= 25:
            nivel = "Avanzado"
        elif cursos_completados >= 10:
            nivel = "Intermedio"
        else:
            nivel = "Básico"

        return {
            "cursos_completados": cursos_completados,
            "logros_obtenidos": logros_obtenidos,
            "nivel": nivel,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular estadísticas: {e}")


def subir_foto(id_docente: int, contenido: bytes, nombre_archivo: str, content_type: str):
    try:
        sb = get_supabase()
        ruta = f"docente_{id_docente}/{nombre_archivo}"

        sb.storage.from_(config.supabase_bucket_fotos).upload(
            ruta,
            contenido,
            {"content-type": content_type or "image/jpeg", "upsert": "true"},
        )

        url_publica = sb.storage.from_(config.supabase_bucket_fotos).get_public_url(ruta)

        actualizado = (
            _table()
            .update({"foto_url": url_publica})
            .eq("id_docente", id_docente)
            .execute()
        )
        return actualizado.data[0] if actualizado.data else {"foto_url": url_publica}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la foto: {e}")
def mis_sellos(id_docente: int):
    """
    Regresa los sellos del catálogo divididos en dos grupos para un docente:
    - obtenidos: sellos que ya ganó (por cursos completados)
    - no_obtenidos: el resto del catálogo
    """
    try:
        sb = get_supabase()

        tomas = (
            sb.schema(config.supabase_schema)
            .table(config.supabase_toma)
            .select("id_curso1")
            .eq("id_docente1", id_docente)
            .ilike("estatus", "completado")
            .execute()
        )
        ids_curso = [t["id_curso1"] for t in tomas.data]

        ids_sello_obtenidos = set()
        if ids_curso:
            cursos = (
                sb.schema(config.supabase_schema)
                .table(config.supabase_curso)
                .select("id_sello1")
                .in_("id_curso", ids_curso)
                .execute()
            )
            ids_sello_obtenidos = {c["id_sello1"] for c in cursos.data if c.get("id_sello1")}

        todos_los_sellos = (
            sb.schema(config.supabase_schema)
            .table(config.supabase_sello)
            .select("*")
            .execute()
        ).data

        obtenidos = [s for s in todos_los_sellos if s["id_sello"] in ids_sello_obtenidos]
        no_obtenidos = [s for s in todos_los_sellos if s["id_sello"] not in ids_sello_obtenidos]

        return {"obtenidos": obtenidos, "no_obtenidos": no_obtenidos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los sellos del docente: {e}")