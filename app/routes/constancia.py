from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencias import usuario_actual, solo_admin
from app.models.constancia import crearConstancia, actualizarConstancia, recuperarConstancia, soloConstancia, listaConstancia
from app.service import constancia_service

router = APIRouter()


@router.get("/constancias", response_model=listaConstancia, tags=["Constancias"])
def listar_constancias(usuario: dict = Depends(usuario_actual)):
    return {"items": constancia_service.listar()}


@router.get("/constancias/buscar", response_model=listaConstancia, tags=["Constancias"])
def buscar_constancias(nombre: str, usuario: dict = Depends(usuario_actual)):
    return {"items": constancia_service.buscar(nombre)}


@router.get("/constancias/{id_constancia}", response_model=soloConstancia, tags=["Constancias"])
def obtener_constancia(id_constancia: int, usuario: dict = Depends(usuario_actual)):
    encontrado = constancia_service.obtener_por_id(id_constancia)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Constancia no encontrada.")
    return {"item": encontrado}


@router.post("/constancias", response_model=recuperarConstancia, tags=["Constancias"])
def crear_constancia(datos: crearConstancia, usuario: dict = Depends(solo_admin)):
    return constancia_service.crear(datos.model_dump())


@router.put("/constancias/{id_constancia}", response_model=recuperarConstancia, tags=["Constancias"])
def actualizar_constancia(id_constancia: int, datos: actualizarConstancia, usuario: dict = Depends(solo_admin)):
    actualizado = constancia_service.actualizar(id_constancia, datos.model_dump(exclude_unset=True))
    if not actualizado:
        raise HTTPException(status_code=404, detail="Constancia no encontrada.")
    return actualizado


@router.delete("/constancias/{id_constancia}", tags=["Constancias"])
def eliminar_constancia(id_constancia: int, usuario: dict = Depends(solo_admin)):
    eliminado = constancia_service.eliminar(id_constancia)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Constancia no encontrada.")
    return eliminado