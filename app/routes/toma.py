from fastapi import APIRouter, Depends

from app.core.dependencias import usuario_actual
from app.models.toma import crearToma, actualizarToma, recuperarToma, soloToma, listaToma
from app.service import toma_service

router = APIRouter()


@router.get("/tomas", response_model=listaToma, tags=["Tomas"])
def listar_tomas(usuario: dict = Depends(usuario_actual)):
    return {"items": toma_service.listar()}


@router.get("/tomas/docente/{id_docente1}", response_model=listaToma, tags=["Tomas"])
def listar_tomas_por_docente(id_docente1: int, usuario: dict = Depends(usuario_actual)):
    return {"items": toma_service.listar_por_docente(id_docente1)}


@router.get("/tomas/curso/{id_curso1}", response_model=listaToma, tags=["Tomas"])
def listar_tomas_por_curso(id_curso1: int, usuario: dict = Depends(usuario_actual)):
    return {"items": toma_service.listar_por_curso(id_curso1)}


@router.get("/tomas/{id_toma}", response_model=soloToma, tags=["Tomas"])
def obtener_toma(id_toma: int, usuario: dict = Depends(usuario_actual)):
    return {"item": toma_service.obtener_por_id(id_toma)}


@router.post("/tomas", response_model=recuperarToma, tags=["Tomas"])
def crear_toma(datos: crearToma, usuario: dict = Depends(usuario_actual)):
    return toma_service.crear(datos.model_dump())


@router.put("/tomas/{id_toma}", response_model=recuperarToma, tags=["Tomas"])
def actualizar_toma(id_toma: int, datos: actualizarToma, usuario: dict = Depends(usuario_actual)):
    return toma_service.actualizar(id_toma, datos.model_dump(exclude_unset=True))


@router.delete("/tomas/{id_toma}", tags=["Tomas"])
def eliminar_toma(id_toma: int, usuario: dict = Depends(usuario_actual)):
    return toma_service.eliminar(id_toma)