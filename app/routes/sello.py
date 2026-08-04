from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencias import usuario_actual
from app.models.sello import crearSello, actualizarSello, recuperarSello, soloSello, listaSello
from app.service import sello_service

router = APIRouter()


@router.get("/sellos", response_model=listaSello, tags=["Sellos"])
def listar_sellos(usuario: dict = Depends(usuario_actual)):
    return {"items": sello_service.listar()}


@router.get("/sellos/buscar", response_model=listaSello, tags=["Sellos"])
def buscar_sellos(nombre: str, usuario: dict = Depends(usuario_actual)):
    return {"items": sello_service.buscar(nombre)}


@router.get("/sellos/{id_sello}", response_model=soloSello, tags=["Sellos"])
def obtener_sello(id_sello: int, usuario: dict = Depends(usuario_actual)):
    encontrado = sello_service.obtener_por_id(id_sello)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Sello no encontrado.")
    return {"item": encontrado}


@router.post("/sellos", response_model=recuperarSello, tags=["Sellos"])
def crear_sello(datos: crearSello, usuario: dict = Depends(usuario_actual)):
    return sello_service.crear(datos.model_dump())


@router.put("/sellos/{id_sello}", response_model=recuperarSello, tags=["Sellos"])
def actualizar_sello(id_sello: int, datos: actualizarSello, usuario: dict = Depends(usuario_actual)):
    actualizado = sello_service.actualizar(id_sello, datos.model_dump(exclude_unset=True))
    if not actualizado:
        raise HTTPException(status_code=404, detail="Sello no encontrado.")
    return actualizado


@router.delete("/sellos/{id_sello}", tags=["Sellos"])
def eliminar_sello(id_sello: int, usuario: dict = Depends(usuario_actual)):
    eliminado = sello_service.eliminar(id_sello)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Sello no encontrado.")
    return eliminado