from fastapi import APIRouter, Depends

from app.core.dependencias import usuario_actual
from app.models.curso import crearCurso, actualizarCurso, recuperarCurso, soloCurso, listaCurso
from app.service import curso_service

router = APIRouter()


@router.get("/cursos", response_model=listaCurso, tags=["Cursos"])
def listar_cursos(usuario: dict = Depends(usuario_actual)):
    return {"items": curso_service.listar()}


@router.get("/cursos/buscar", response_model=listaCurso, tags=["Cursos"])
def buscar_cursos(nombre: str, usuario: dict = Depends(usuario_actual)):
    return {"items": curso_service.buscar(nombre)}


@router.get("/cursos/{id_curso}", response_model=soloCurso, tags=["Cursos"])
def obtener_curso(id_curso: int, usuario: dict = Depends(usuario_actual)):
    return {"item": curso_service.obtener_por_id(id_curso)}


@router.post("/cursos", response_model=recuperarCurso, tags=["Cursos"])
def crear_curso(datos: crearCurso, usuario: dict = Depends(usuario_actual)):
    return curso_service.crear(datos.model_dump())


@router.put("/cursos/{id_curso}", response_model=recuperarCurso, tags=["Cursos"])
def actualizar_curso(id_curso: int, datos: actualizarCurso, usuario: dict = Depends(usuario_actual)):
    return curso_service.actualizar(id_curso, datos.model_dump(exclude_unset=True))


@router.delete("/cursos/{id_curso}", tags=["Cursos"])
def eliminar_curso(id_curso: int, usuario: dict = Depends(usuario_actual)):
    return curso_service.eliminar(id_curso)