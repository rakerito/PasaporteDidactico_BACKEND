from fastapi import APIRouter, Depends

from app.core.dependencias import usuario_actual
from app.models.categoria import crearCategoria, actualizarCategoria, recuperarCategoria, soloCategoria, listaCategoria
from app.service import categoria_service

router = APIRouter()


@router.get("/categorias", response_model=listaCategoria, tags=["Categorias"])
def listar_categorias(usuario: dict = Depends(usuario_actual)):
    return {"items": categoria_service.listar()}


@router.get("/categorias/{id_categoria}", response_model=soloCategoria, tags=["Categorias"])
def obtener_categoria(id_categoria: int, usuario: dict = Depends(usuario_actual)):
    return {"item": categoria_service.obtener_por_id(id_categoria)}


@router.post("/categorias", response_model=recuperarCategoria, tags=["Categorias"])
def crear_categoria(datos: crearCategoria, usuario: dict = Depends(usuario_actual)):
    return categoria_service.crear(datos.model_dump())


@router.put("/categorias/{id_categoria}", response_model=recuperarCategoria, tags=["Categorias"])
def actualizar_categoria(id_categoria: int, datos: actualizarCategoria, usuario: dict = Depends(usuario_actual)):
    return categoria_service.actualizar(id_categoria, datos.model_dump(exclude_unset=True))


@router.delete("/categorias/{id_categoria}", tags=["Categorias"])
def eliminar_categoria(id_categoria: int, usuario: dict = Depends(usuario_actual)):
    return categoria_service.eliminar(id_categoria)