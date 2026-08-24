from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.dependencias import usuario_actual, solo_admin
from app.models.notificacion import (
    crearNotificacionPersonal,
    crearNotificacionGeneral,
    listaNotificacion,
    resumenNotificaciones,
)
from app.service import notificacion_service

router = APIRouter()


class marcarLeidaRequest(BaseModel):
    origen: Literal["personal", "general"]
    id_notificacion: int


@router.get("/notificaciones", response_model=listaNotificacion, tags=["Notificaciones"])
def listar_mis_notificaciones(usuario: dict = Depends(usuario_actual)):
    id_usuario1 = int(usuario["sub"])
    return {"items": notificacion_service.mis_notificaciones(id_usuario1)}


@router.get("/notificaciones/resumen", response_model=resumenNotificaciones, tags=["Notificaciones"])
def resumen_mis_notificaciones(usuario: dict = Depends(usuario_actual)):
    id_usuario1 = int(usuario["sub"])
    return notificacion_service.resumen(id_usuario1)


@router.post("/notificaciones/marcar-leida", tags=["Notificaciones"])
def marcar_notificacion_leida(datos: marcarLeidaRequest, usuario: dict = Depends(usuario_actual)):
    id_usuario1 = int(usuario["sub"])
    return notificacion_service.marcar_leida(id_usuario1, datos.origen, datos.id_notificacion)


@router.delete("/notificaciones", tags=["Notificaciones"])
def vaciar_mis_notificaciones(usuario: dict = Depends(usuario_actual)):
    id_usuario1 = int(usuario["sub"])
    return notificacion_service.vaciar(id_usuario1)


@router.post("/notificaciones/personal", tags=["Notificaciones"])
def crear_notificacion_personal(datos: crearNotificacionPersonal, usuario: dict = Depends(solo_admin)):
    return notificacion_service.crear_personal(datos.model_dump())


@router.post("/notificaciones/general", tags=["Notificaciones"])
def crear_notificacion_general(datos: crearNotificacionGeneral, usuario: dict = Depends(solo_admin)):
    return notificacion_service.crear_general(datos.model_dump())


@router.delete("/notificaciones/general/{id_notificacion_general}", tags=["Notificaciones"])
def eliminar_notificacion_general(id_notificacion_general: int, usuario: dict = Depends(solo_admin)):
    eliminado = notificacion_service.eliminar_general(id_notificacion_general)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Notificación general no encontrada.")
    return eliminado