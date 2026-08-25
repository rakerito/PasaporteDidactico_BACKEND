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
        res = _table().select("*").eq("id_curso", id_curso).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar curso: {e}")


def listar():
    try:
        res = _table().select("*").execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar cursos: {e}")


def buscar(nombre: str):
    try:
        res = _table().select("*").ilike("nombre", f"%{nombre}%").execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar cursos: {e}")


# =====================================
# CRUD
# =====================================

def crear(datos: dict):
    try:
        if not datos:
            raise HTTPException(status_code=400, detail="No se recibieron datos.")

        if datos.get("tipo") == "microcurso":
            validar_microcurso(datos)

        datos = jsonable_encoder(datos)
        res = _table().insert(datos).execute()
        return res.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear curso: {e}")


def actualizar(id_curso: int, datos: dict):
    try:
        if not datos:
            raise HTTPException(status_code=400, detail="No se recibieron datos.")
        datos = jsonable_encoder(datos)
        res = _table().update(datos).eq("id_curso", id_curso).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar curso: {e}")


def eliminar(id_curso: int):
    try:
        res = _table().delete().eq("id_curso", id_curso).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar curso: {e}")


# =====================================
# CATEGORÍAS
# =====================================

def listar_por_categoria(id_categoria: int):
    from app.service import curso_categoria_service

    ids_curso = curso_categoria_service.cursos_de_categoria_ids(id_categoria)
    if not ids_curso:
        return []
    try:
        res = _table().select("*").in_("id_curso", ids_curso).execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar cursos por categoría: {e}")


# =====================================
# MICROCURSOS
# =====================================

def listar_microcursos(id_curso_padre: int):
    try:
        res = _table().select("*").eq("id_curso_padre", id_curso_padre).execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar microcursos: {e}")


def validar_microcurso(datos: dict):
    """
    Verifica las reglas de negocio antes de crear un microcurso:
    - El curso padre debe existir y ser de tipo 'normal'.
    - Un curso padre no puede tener más de 4 microcursos.
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


# =====================================
# CURSOS ACTIVOS (con info enriquecida)
# =====================================

def listar_activos_detallado():
    """
    Regresa los cursos activos, cada uno ya con:
    - otorga: nombre del sello que da (no solo el id)
    - categorias: nombres separados por coma (no solo ids)
    - fecha_lim: texto calculado según fecha_lim_default o dias_para_completar
    """
    try:
        sb = get_supabase()

        cursos = (
            sb.schema(config.supabase_schema)
            .table(config.supabase_curso)
            .select("*")
            .ilike("estatus", "activo")
            .execute()
        ).data

        ids_sello = {c["id_sello1"] for c in cursos if c.get("id_sello1")}
        sellos_por_id = {}
        if ids_sello:
            sellos = (
                sb.schema(config.supabase_schema)
                .table(config.supabase_sello)
                .select("id_sello, nombre")
                .in_("id_sello", list(ids_sello))
                .execute()
            ).data
            sellos_por_id = {s["id_sello"]: s["nombre"] for s in sellos}

        ids_curso = [c["id_curso"] for c in cursos]
        categorias_por_curso: dict[int, list[str]] = {}
        if ids_curso:
            relaciones = (
                sb.schema(config.supabase_schema)
                .table(config.supabase_curso_categoria)
                .select("id_curso, id_categoria")
                .in_("id_curso", ids_curso)
                .execute()
            ).data

            ids_categoria = list({r["id_categoria"] for r in relaciones})
            nombres_categoria = {}
            if ids_categoria:
                cats = (
                    sb.schema(config.supabase_schema)
                    .table(config.supabase_categoria)
                    .select("id_categoria, nombre")
                    .in_("id_categoria", ids_categoria)
                    .execute()
                ).data
                nombres_categoria = {c["id_categoria"]: c["nombre"] for c in cats}

            for r in relaciones:
                categorias_por_curso.setdefault(r["id_curso"], []).append(
                    nombres_categoria.get(r["id_categoria"], "")
                )

        for c in cursos:
            c["otorga"] = sellos_por_id.get(c.get("id_sello1"))
            cats = categorias_por_curso.get(c["id_curso"], [])
            c["categorias"] = ", ".join(cats) if cats else None

            if c.get("fecha_lim_default"):
                c["fecha_lim"] = c["fecha_lim_default"]
            elif c.get("dias_para_completar"):
                c["fecha_lim"] = f"{c['dias_para_completar']} días después de inscribirte"
            else:
                c["fecha_lim"] = None

        return cursos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar cursos activos: {e}")


# =====================================
# DETALLE COMPLETO DE UN CURSO
# =====================================

def detalle_completo(id_curso: int):
    """
    Trae la info extendida de un curso para el modal de detalle:
    - descripción propia
    - a qué sello otorga (por su id_sello1)
    - sus categorías (nombres, no solo ids)
    - si es un curso 'normal' con microcursos hijos, la lista de esos microcursos
    """
    try:
        sb = get_supabase()

        curso_res = (
            sb.schema(config.supabase_schema)
            .table(config.supabase_curso)
            .select("*")
            .eq("id_curso", id_curso)
            .execute()
        )
        if not curso_res.data:
            raise HTTPException(status_code=404, detail="Curso no encontrado.")
        curso_info = curso_res.data[0]

        otorga_nombre = None
        if curso_info.get("id_sello1"):
            sello = (
                sb.schema(config.supabase_schema)
                .table(config.supabase_sello)
                .select("nombre")
                .eq("id_sello", curso_info["id_sello1"])
                .execute()
            )
            if sello.data:
                otorga_nombre = sello.data[0]["nombre"]

        relaciones = (
            sb.schema(config.supabase_schema)
            .table(config.supabase_curso_categoria)
            .select("id_categoria")
            .eq("id_curso", id_curso)
            .execute()
        )
        ids_categoria = [r["id_categoria"] for r in relaciones.data]
        nombres_categorias = []
        if ids_categoria:
            categorias = (
                sb.schema(config.supabase_schema)
                .table(config.supabase_categoria)
                .select("nombre")
                .in_("id_categoria", ids_categoria)
                .execute()
            )
            nombres_categorias = [c["nombre"] for c in categorias.data]

        cursos_requeridos = []
        if curso_info.get("tipo") == "normal":
            hijos = (
                sb.schema(config.supabase_schema)
                .table(config.supabase_curso)
                .select("id_curso, nombre")
                .eq("id_curso_padre", id_curso)
                .execute()
            )
            cursos_requeridos = hijos.data

        fecha_lim = None
        if curso_info.get("fecha_lim_default"):
            fecha_lim = curso_info["fecha_lim_default"]
        elif curso_info.get("dias_para_completar"):
            fecha_lim = f"{curso_info['dias_para_completar']} días después de inscribirte"

        return {
            "descripcion": curso_info.get("descripcion"),
            "otorga": otorga_nombre,
            "categorias": ", ".join(nombres_categorias) if nombres_categorias else None,
            "fecha_lim": fecha_lim,
            "cursos_requeridos": cursos_requeridos,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el detalle del curso: {e}")