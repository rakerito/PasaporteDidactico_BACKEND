from fastapi import APIRouter, Depends

from app.core.dependencias import usuario_actual
from app.models.curso_categoria import crearCursoCategoria, listaCursoCategoria
from app.service import curso_categoria_service

router = APIRouter()


@router.get("/curso-categoria/curso/{id_curso}", response_model=listaCursoCategoria, tags=["Curso-Categoria"])
def listar_categorias_de_curso(id_curso: int, usuario: dict = Depends(usuario_actual)):
    return {"items": curso_categoria_service.listar_por_curso(id_curso)}


@router.get("/curso-categoria/categoria/{id_categoria}", response_model=listaCursoCategoria, tags=["Curso-Categoria"])
def listar_cursos_de_categoria(id_categoria: int, usuario: dict = Depends(usuario_actual)):
    return {"items": curso_categoria_service.listar_por_categoria(id_categoria)}


@router.post("/curso-categoria", tags=["Curso-Categoria"])
def asignar_categoria(datos: crearCursoCategoria, usuario: dict = Depends(usuario_actual)):
    return curso_categoria_service.asignar(datos.id_curso, datos.id_categoria)


@router.delete("/curso-categoria/{id_curso}/{id_categoria}", tags=["Curso-Categoria"])
def quitar_categoria(id_curso: int, id_categoria: int, usuario: dict = Depends(usuario_actual)):
    return curso_categoria_service.quitar(id_curso, id_categoria)