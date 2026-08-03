from pydantic import BaseModel, Field
from datetime import date

class crearOtorga(BaseModel):
    id_usuario1: int = Field(ge=0)
    id_sello2: int = Field(ge=0)
    fecha_obtencion: date

class actualizarOtorga(BaseModel):
    id_usuario1: int | None = Field(default=None, ge=0)
    id_sello2: int | None = Field(default=None, ge=0)
    fecha_obtencion: date | None = None

class recuperarOtorga(BaseModel):
    id_otorgar: int
    id_usuario1: int
    id_sello2: int
    fecha_obtencion: date

class soloOtorga(BaseModel):
    item: recuperarOtorga

class listaOtorga(BaseModel):
    items: list[recuperarOtorga]
