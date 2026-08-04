from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencias import usuario_actual, solo_admin
from app.models.usuario import crearUsuario, actualizarUsuario, recuperarUsuario, soloUsuario, listaUsuario
from app.service import usuario_service

router = APIRouter()


@router.get("/usuarios", response_model=listaUsuario, tags=["Usuarios"])
def listar_usuarios(usuario: dict = Depends(solo_admin)):
    return {"items": usuario_service.listar()}


@router.get("/usuarios/buscar", response_model=listaUsuario, tags=["Usuarios"])
def buscar_usuarios(nombre: str, usuario: dict = Depends(solo_admin)):
    return {"items": usuario_service.buscar(nombre)}


@router.get("/usuarios/{id_usuario}", response_model=soloUsuario, tags=["Usuarios"])
def obtener_usuario(id_usuario: int, usuario: dict = Depends(usuario_actual)):
    encontrado = usuario_service.obtener_por_id(id_usuario)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return {"item": encontrado}


@router.post("/usuarios", response_model=recuperarUsuario, tags=["Usuarios"])
def crear_usuario(datos: crearUsuario):
    return usuario_service.crear(datos.model_dump())


@router.put("/usuarios/{id_usuario}", response_model=recuperarUsuario, tags=["Usuarios"])
def actualizar_usuario(id_usuario: int, datos: actualizarUsuario, usuario: dict = Depends(usuario_actual)):
    actualizado = usuario_service.actualizar(id_usuario, datos.model_dump(exclude_unset=True))
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return actualizado


@router.delete("/usuarios/{id_usuario}", tags=["Usuarios"])
def eliminar_usuario(id_usuario: int, usuario: dict = Depends(solo_admin)):
    eliminado = usuario_service.eliminar(id_usuario)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return eliminado