from fastapi import APIRouter, Depends

from app.core.dependencias import solo_admin
from app.models.requiere import crearRequiere
from app.service import requiere_service

router = APIRouter()


@router.get("/requiere", tags=["Requiere"])
def listar_requiere(usuario: dict = Depends(solo_admin)):
    return {"items": requiere_service.listar()}


@router.get("/requiere/curso/{id_curso2}", tags=["Requiere"])
def listar_requiere_por_curso(id_curso2: int, usuario: dict = Depends(solo_admin)):
    return {"items": requiere_service.listar_por_curso(id_curso2)}


@router.post("/requiere", tags=["Requiere"])
def crear_requiere(datos: crearRequiere, usuario: dict = Depends(solo_admin)):
    return requiere_service.crear(datos.model_dump())


@router.delete("/requiere/{id_curso2}/{id_sello1}", tags=["Requiere"])
def eliminar_requiere(id_curso2: int, id_sello1: int, usuario: dict = Depends(solo_admin)):
    return requiere_service.eliminar(id_curso2, id_sello1)