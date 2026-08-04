from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencias import usuario_actual, solo_admin
from app.models.otorga import crearOtorga, recuperarOtorga, soloOtorga, listaOtorga
from app.service import otorga_service

router = APIRouter()


@router.get("/otorgas", response_model=listaOtorga, tags=["Otorga"])
def listar_otorgas(usuario: dict = Depends(usuario_actual)):
    return {"items": otorga_service.listar()}


@router.get("/otorgas/constancia/{id_constancia1}", response_model=listaOtorga, tags=["Otorga"])
def listar_otorgas_por_constancia(id_constancia1: int, usuario: dict = Depends(usuario_actual)):
    return {"items": otorga_service.listar_por_constancia(id_constancia1)}


@router.get("/otorgas/{id_otorga}", response_model=soloOtorga, tags=["Otorga"])
def obtener_otorga(id_otorga: int, usuario: dict = Depends(usuario_actual)):
    encontrado = otorga_service.obtener_por_id(id_otorga)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Otorgamiento no encontrado.")
    return {"item": encontrado}


@router.post("/otorgas", response_model=recuperarOtorga, tags=["Otorga"])
def crear_otorga(datos: crearOtorga, usuario: dict = Depends(solo_admin)):
    return otorga_service.crear(datos.model_dump())


@router.delete("/otorgas/{id_otorga}", tags=["Otorga"])
def eliminar_otorga(id_otorga: int, usuario: dict = Depends(solo_admin)):
    eliminado = otorga_service.eliminar(id_otorga)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Otorgamiento no encontrado.")
    return eliminado