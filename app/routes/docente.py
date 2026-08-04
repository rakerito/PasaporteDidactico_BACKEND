from fastapi import APIRouter, Depends

from app.core.dependencias import usuario_actual
from app.models.docente import crearDocente, actualizarDocente, recuperarDocente, soloDocente, listaDocente
from app.service import docente_service

router = APIRouter()


@router.get("/docentes", response_model=listaDocente, tags=["Docentes"])
def listar_docentes(usuario: dict = Depends(usuario_actual)):
    return {"items": docente_service.listar()}


@router.get("/docentes/{id_docente}", response_model=soloDocente, tags=["Docentes"])
def obtener_docente(id_docente: int, usuario: dict = Depends(usuario_actual)):
    return {"item": docente_service.obtener_por_id(id_docente)}


@router.post("/docentes", response_model=recuperarDocente, tags=["Docentes"])
def crear_docente(datos: crearDocente, usuario: dict = Depends(usuario_actual)):
    return docente_service.crear(datos.model_dump())


@router.put("/docentes/{id_docente}", response_model=recuperarDocente, tags=["Docentes"])
def actualizar_docente(id_docente: int, datos: actualizarDocente, usuario: dict = Depends(usuario_actual)):
    return docente_service.actualizar(id_docente, datos.model_dump(exclude_unset=True))


@router.delete("/docentes/{id_docente}", tags=["Docentes"])
def eliminar_docente(id_docente: int, usuario: dict = Depends(usuario_actual)):
    return docente_service.eliminar(id_docente)