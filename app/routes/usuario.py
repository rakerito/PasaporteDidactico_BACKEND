from fastapi import APIRouter, Depends

from app.core.dependencias import usuario_actual
from app.models.usuario import crearUsuario, actualizarUsuario, recuperarUsuario, soloUsuario, listaUsuario
from app.service import usuario_service

router = APIRouter()


@router.get("/usuarios", response_model=listaUsuario, tags=["Usuarios"])
def listar_usuarios(usuario: dict = Depends(usuario_actual)):
    return {"items": usuario_service.listar()}


@router.get("/usuarios/buscar", response_model=listaUsuario, tags=["Usuarios"])
def buscar_usuarios(nombre: str, usuario: dict = Depends(usuario_actual)):
    return {"items": usuario_service.buscar(nombre)}


@router.get("/usuarios/{id_usuario}", response_model=soloUsuario, tags=["Usuarios"])
def obtener_usuario(id_usuario: int, usuario: dict = Depends(usuario_actual)):
    return {"item": usuario_service.obtener_por_id(id_usuario)}


@router.post("/usuarios", response_model=recuperarUsuario, tags=["Usuarios"])
def crear_usuario(datos: crearUsuario):
    # Sin Depends(usuario_actual): el registro debe poder hacerse sin sesión previa
    return usuario_service.crear(datos.model_dump())


@router.put("/usuarios/{id_usuario}", response_model=recuperarUsuario, tags=["Usuarios"])
def actualizar_usuario(id_usuario: int, datos: actualizarUsuario, usuario: dict = Depends(usuario_actual)):
    return usuario_service.actualizar(id_usuario, datos.model_dump(exclude_unset=True))


@router.delete("/usuarios/{id_usuario}", tags=["Usuarios"])
def eliminar_usuario(id_usuario: int, usuario: dict = Depends(usuario_actual)):
    return usuario_service.eliminar(id_usuario)