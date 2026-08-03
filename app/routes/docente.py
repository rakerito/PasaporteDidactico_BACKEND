from fastapi import APIRouter, Depends

from app.core.dependencias import usuario_actual
from app.service import docente_service

router = APIRouter()


@router.get("/docentes", tags=["Docentes"])
def listar_docentes(usuario: dict = Depends(usuario_actual)):
    return {"items": docente_service.listar()}


@router.get("/docentes/{id_docente}", tags=["Docentes"])
def obtener_docente(id_docente: int, usuario: dict = Depends(usuario_actual)):
    return {"item": docente_service.obtener_por_id(id_docente)}


@router.post("/docentes", tags=["Docentes"])
def crear_docente(datos: dict, usuario: dict = Depends(usuario_actual)):
    return docente_service.crear(datos)


@router.put("/docentes/{id_docente}", tags=["Docentes"])
def actualizar_docente(id_docente: int, datos: dict, usuario: dict = Depends(usuario_actual)):
    return docente_service.actualizar(id_docente, datos)


@router.delete("/docentes/{id_docente}", tags=["Docentes"])
def eliminar_docente(id_docente: int, usuario: dict = Depends(usuario_actual)):
    return docente_service.eliminar(id_docente)