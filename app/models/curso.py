from typing import Literal
from pydantic import BaseModel, Field

class crearCurso(BaseModel):
    nombre: str = Field(max_length=100)
    descripcion: str = Field(max_length=300)
    duracion: int = Field(ge=0, lt=10000)
    estatus: str = Field(max_length=10)
    id_sello1: int = Field(ge=0)
    tipo: Literal["normal", "microcurso"] = "normal"
    id_curso_padre: int | None = Field(default=None, ge=0)

class actualizarCurso(BaseModel):
    nombre: str | None = Field(default=None, max_length=100)
    descripcion: str | None = Field(default=None, max_length=300)
    duracion: int | None = Field(default=None, ge=0, lt=10000)
    estatus: str | None = Field(default=None, max_length=10)
    id_sello1: int | None = Field(default=None, ge=0)
    tipo: Literal["normal", "microcurso"] | None = Field(default=None)
    id_curso_padre: int | None = Field(default=None, ge=0)

class recuperarCurso(BaseModel):
    id_curso: int
    nombre: str
    descripcion: str
    duracion: int
    estatus: str
    id_sello1: int
    tipo: str
    id_curso_padre: int | None = None

class soloCurso(BaseModel):
    item: recuperarCurso

class listaCurso(BaseModel):
    items: list[recuperarCurso]