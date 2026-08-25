from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencias import usuario_actual, solo_admin
from app.models.curso import crearCurso, actualizarCurso, recuperarCurso, soloCurso, listaCurso
from app.service import curso_service, curso_categoria_service

router = APIRouter()


# =====================================
# Rutas de texto fijo / con segmento extra — SIEMPRE antes de /cursos/{id_curso}
# =====================================

@router.get("/cursos", response_model=listaCurso, tags=["Cursos"])
def listar_cursos(usuario: dict = Depends(usuario_actual)):
    return {"items": curso_service.listar()}


@router.get("/cursos/buscar", response_model=listaCurso, tags=["Cursos"])
def buscar_cursos(nombre: str, usuario: dict = Depends(usuario_actual)):
    return {"items": curso_service.buscar(nombre)}


@router.get("/cursos/activos", tags=["Cursos"])
def obtener_cursos_activos(usuario: dict = Depends(usuario_actual)):
    return curso_service.listar_activos_detallado()


@router.get("/cursos/categoria/{id_categoria}", tags=["Cursos"])
def buscar_cursos_por_categoria(id_categoria: int, usuario: dict = Depends(usuario_actual)):
    return {"items": curso_service.listar_por_categoria(id_categoria)}


# =====================================
# Rutas con /{id_curso} solo (una vez definidas las de arriba, ya no compiten)
# =====================================

@router.get("/cursos/{id_curso}", response_model=soloCurso, tags=["Cursos"])
def obtener_curso(id_curso: int, usuario: dict = Depends(usuario_actual)):
    encontrado = curso_service.obtener_por_id(id_curso)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Curso no encontrado.")
    return {"item": encontrado}


@router.get("/cursos/{id_curso}/categorias", tags=["Cursos"])
def obtener_categorias_del_curso(id_curso: int, usuario: dict = Depends(usuario_actual)):
    return {"items": curso_categoria_service.categorias_de_curso_detalle(id_curso)}


@router.get("/cursos/{id_curso}/detalle", tags=["Cursos"])
def obtener_detalle_curso(id_curso: int, usuario: dict = Depends(usuario_actual)):
    return curso_service.detalle_completo(id_curso)


@router.get("/cursos/{id_curso}/microcursos", response_model=listaCurso, tags=["Cursos"])
def obtener_microcursos(id_curso: int, usuario: dict = Depends(usuario_actual)):
    return {"items": curso_service.listar_microcursos(id_curso)}


# =====================================
# CRUD (solo admin)
# =====================================

@router.post("/cursos", response_model=recuperarCurso, tags=["Cursos"])
def crear_curso(datos: crearCurso, usuario: dict = Depends(solo_admin)):
    return curso_service.crear(datos.model_dump())


@router.put("/cursos/{id_curso}", response_model=recuperarCurso, tags=["Cursos"])
def actualizar_curso(id_curso: int, datos: actualizarCurso, usuario: dict = Depends(solo_admin)):
    actualizado = curso_service.actualizar(id_curso, datos.model_dump(exclude_unset=True))
    if not actualizado:
        raise HTTPException(status_code=404, detail="Curso no encontrado.")
    return actualizado


@router.delete("/cursos/{id_curso}", tags=["Cursos"])
def eliminar_curso(id_curso: int, usuario: dict = Depends(solo_admin)):
    eliminado = curso_service.eliminar(id_curso)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Curso no encontrado.")
    return eliminado