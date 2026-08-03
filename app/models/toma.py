from pydantic import BaseModel, Field
from datetime import date

class crearToma(BaseModel):
    progreso: str = Field(max_length=25)
    estatus: str = Field(max_length=15)
    fecha_lim: date
    id_curso1: int = Field(ge=0)
    id_docente1: int = Field(ge=0)

class actualizarToma(BaseModel):
    progreso: str | None = Field(default=None, max_length=25)
    estatus: str | None = Field(default=None, max_length=15)
    fecha_lim: date | None = None
    id_curso1: int | None = Field(default=None, ge=0)
    id_docente1: int | None = Field(default=None, ge=0)

class recuperarToma(BaseModel):
    id_toma: int
    progreso: str
    estatus: str
    fecha_lim: date
    id_curso1: int
    id_docente1: int

class soloToma(BaseModel):
    item: recuperarToma

class listaToma(BaseModel):
    items: list[recuperarToma]
