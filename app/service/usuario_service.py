from datetime import datetime

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config
from app.service.encryptar import hash_password


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_usuario)


# =====================================
# CONSULTAS
# =====================================

def obtener_por_correo(correo: str):
    try:
        res = (
            _table()
            .select("*")
            .eq("correo", correo)
            .execute()
        )

        if not res.data:
            return None

        return res.data[0]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener usuario: {e}"
        )


def obtener_por_id(id_usuario: int):
    try:
        res = (
            _table()
            .select("*")
            .eq("id_usuario", id_usuario)
            .execute()
        )

        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar usuario: {e}"
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
            detail=f"Error al listar usuarios: {e}"
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
            detail=f"Error al buscar usuarios: {e}"
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

        # Verificar correo existente
        existe = obtener_por_correo(datos["correo"])

        if existe:
            raise HTTPException(
                status_code=409,
                detail="El correo ya está registrado."
            )

        # Generar el número de usuario: año de inscripción + no. de empleado a 6 dígitos
        anio_actual = datetime.now().year
        numero_usuario = f"{anio_actual}{datos['no_empleado'].zfill(6)}"

        existente_numero = (
            _table()
            .select("id_usuario")
            .eq("numero_usuario", numero_usuario)
            .execute()
        )
        if existente_numero.data:
            raise HTTPException(
                status_code=409,
                detail="Ya existe un usuario con ese número de empleado registrado este año."
            )

        datos["numero_usuario"] = numero_usuario

        datos["contraseña"] = hash_password(
            datos["contraseña"]
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
            detail=f"Error al crear usuario: {e}"
        )


def actualizar(id_usuario: int, datos: dict):
    try:
        if not datos:
            raise HTTPException(
                status_code=400,
                detail="No se recibieron datos."
            )

        if "contraseña" in datos:
            datos["contraseña"] = hash_password(
                datos["contraseña"]
            )

        datos = jsonable_encoder(datos)

        res = (
            _table()
            .update(datos)
            .eq("id_usuario", id_usuario)
            .execute()
        )

        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar usuario: {e}"
        )


def eliminar(id_usuario: int):
    try:
        res = (
            _table()
            .delete()
            .eq("id_usuario", id_usuario)
            .execute()
        )

        return res.data[0] if res.data else None

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar usuario: {e}"
        )