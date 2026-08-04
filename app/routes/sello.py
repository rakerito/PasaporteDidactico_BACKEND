from fastapi import APIRouter, Depends

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
    return {"item": sello_service.obtener_por_id(id_sello)}


@router.post("/sellos", response_model=recuperarSello, tags=["Sellos"])
def crear_sello(datos: crearSello, usuario: dict = Depends(usuario_actual)):
    return sello_service.crear(datos.model_dump())


@router.put("/sellos/{id_sello}", response_model=recuperarSello, tags=["Sellos"])
def actualizar_sello(id_sello: int, datos: actualizarSello, usuario: dict = Depends(usuario_actual)):
    return sello_service.actualizar(id_sello, datos.model_dump(exclude_unset=True))


@router.delete("/sellos/{id_sello}", tags=["Sellos"])
def eliminar_sello(id_sello: int, usuario: dict = Depends(usuario_actual)):
    return sello_service.eliminar(id_sello)