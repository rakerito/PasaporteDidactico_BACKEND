from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_curso)


# =====================================
# CONSULTAS
# =====================================

def obtener_por_id(id_curso: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_curso", id_curso)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar curso: {e}"
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
            detail=f"Error al listar cursos: {e}"
        )


def buscar(nombre: str):
    try:
        res = (
            _table()
            .select("*")
            .ilike("nombre", f"%{nombre}%")
            .execute()
        )
        return res.data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar cursos: {e}"
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

        if datos.get("tipo") == "microcurso":
            validar_microcurso(datos)

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
            detail=f"Error al crear curso: {e}"
        )


def actualizar(id_curso: int, datos: dict):
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
            .eq("id_curso", id_curso)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar curso: {e}"
        )


def eliminar(id_curso: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_curso", id_curso)
            .execute()
        )
        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar curso: {e}"
        )

def listar_por_categoria(id_categoria: int):
    """
    Regresa los cursos completos que pertenecen a una categoría dada.
    """
    from app.service import curso_categoria_service

    ids_curso = curso_categoria_service.cursos_de_categoria_ids(id_categoria)

    if not ids_curso:
        return []

    try:
        res = (
            _table()
            .select("*")
            .in_("id_curso", ids_curso)
            .execute()
        )
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar cursos por categoría: {e}")

def listar_microcursos(id_curso_padre: int):
    """
    Regresa los microcursos que pertenecen a un curso normal dado.
    """
    try:
        res = (
            _table()
            .select("*")
            .eq("id_curso_padre", id_curso_padre)
            .execute()
        )
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar microcursos: {e}")


def validar_microcurso(datos: dict):
    """
    Verifica las reglas de negocio antes de crear/actualizar un microcurso:
    - El curso padre debe existir y ser de tipo 'normal'.
    - Un curso padre no puede tener más de 4 microcursos.
    Se usa solo cuando datos["tipo"] == "microcurso" y trae id_curso_padre.
    """
    id_padre = datos.get("id_curso_padre")

    if not id_padre:
        raise HTTPException(
            status_code=400,
            detail="Un microcurso debe indicar a qué curso (id_curso_padre) pertenece."
        )

    padre = obtener_por_id(id_padre)
    if not padre:
        raise HTTPException(status_code=400, detail="El curso padre indicado no existe.")

    if padre.get("tipo") != "normal":
        raise HTTPException(
            status_code=400,
            detail="Un microcurso solo puede pertenecer a un curso de tipo 'normal', no a otro microcurso."
        )

    hijos_actuales = listar_microcursos(id_padre)
    if len(hijos_actuales) >= 4:
        raise HTTPException(
            status_code=400,
            detail="Este curso ya tiene el máximo de 4 microcursos permitidos."
        )