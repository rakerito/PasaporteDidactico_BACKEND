from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.supabase_client import get_supabase
from app.core.config import config


def _personal():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_notificacion_personal)


def _general():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_notificacion_general)


def _general_leida():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_notificacion_general_leida)


def mis_notificaciones(id_usuario1: int):
    try:
        personales = _personal().select("*").eq("id_usuario1", id_usuario1).execute().data
        for p in personales:
            p["origen"] = "personal"

        generales = _general().select("*").execute().data
        leidas = _general_leida().select("id_notificacion_general").eq("id_usuario1", id_usuario1).execute().data
        ids_ya_vistas = {l["id_notificacion_general"] for l in leidas}

        generales_pendientes = []
        for g in generales:
            if g["id_notificacion_general"] not in ids_ya_vistas:
                g["id_notificacion"] = g["id_notificacion_general"]
                g["origen"] = "general"
                g["leida"] = False
                generales_pendientes.append(g)

        todas = personales + generales_pendientes
        todas.sort(key=lambda n: n["creada_en"], reverse=True)
        return todas

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener notificaciones: {e}")


def resumen(id_usuario1: int):
    try:
        notificaciones = mis_notificaciones(id_usuario1)
        no_leidas = [n for n in notificaciones if not n.get("leida")]

        conteo = {"sello": 0, "curso": 0, "constancia": 0, "mantenimiento": 0, "general": 0}
        for n in no_leidas:
            tipo = n.get("tipo")
            if tipo in conteo:
                conteo[tipo] += 1

        return {**conteo, "total": len(no_leidas)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resumir notificaciones: {e}")


def vaciar(id_usuario1: int):
    """
    'Vacía' las notificaciones del usuario:
    - Las personales se eliminan de verdad (son solo suyas).
    - Las generales NO se eliminan, solo se marca que este usuario ya las vio.
    """
    try:
        _personal().delete().eq("id_usuario1", id_usuario1).execute()

        generales = _general().select("id_notificacion_general").execute().data
        leidas = _general_leida().select("id_notificacion_general").eq("id_usuario1", id_usuario1).execute().data
        ids_ya_vistas = {l["id_notificacion_general"] for l in leidas}

        nuevas = [
            {"id_usuario1": id_usuario1, "id_notificacion_general": g["id_notificacion_general"]}
            for g in generales
            if g["id_notificacion_general"] not in ids_ya_vistas
        ]

        if nuevas:
            _general_leida().insert(jsonable_encoder(nuevas)).execute()

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al vaciar notificaciones: {e}")


def crear_personal(datos: dict):
    try:
        datos = jsonable_encoder(datos)
        res = _personal().insert(datos).execute()
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear notificación: {e}")


def crear_general(datos: dict):
    try:
        datos = jsonable_encoder(datos)
        res = _general().insert(datos).execute()
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear notificación general: {e}")


def eliminar_general(id_notificacion_general: int):
    try:
        res = _general().delete().eq("id_notificacion_general", id_notificacion_general).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar notificación general: {e}")


def marcar_leida(id_usuario1: int, origen: str, id_notificacion: int):
    """
    Marca UNA notificación como leída para este usuario.
    - Personal: se actualiza su propia fila (con verificación de dueño).
    - General: se registra en la tabla de 'ya vistas' solo para este usuario.
    """
    try:
        if origen == "personal":
            res = (
                _personal()
                .update({"leida": True})
                .eq("id_notificacion", id_notificacion)
                .eq("id_usuario1", id_usuario1)
                .execute()
            )
            if not res.data:
                raise HTTPException(status_code=404, detail="Notificación no encontrada.")
            return res.data[0]

        elif origen == "general":
            ya_vista = (
                _general_leida()
                .select("*")
                .eq("id_usuario1", id_usuario1)
                .eq("id_notificacion_general", id_notificacion)
                .execute()
            )
            if not ya_vista.data:
                _general_leida().insert({
                    "id_usuario1": id_usuario1,
                    "id_notificacion_general": id_notificacion,
                }).execute()
            return {"status": "ok"}

        else:
            raise HTTPException(status_code=400, detail="Origen inválido, debe ser 'personal' o 'general'.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al marcar como leída: {e}")