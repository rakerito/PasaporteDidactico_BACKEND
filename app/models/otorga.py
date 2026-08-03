from pydantic import BaseModel, Field

class crearOtorga(BaseModel):
    id_sello2: int = Field(ge=0)
    id_constancia1: int = Field(ge=0)

class actualizarOtorga(BaseModel):
    id_sello2: int | None = Field(default=None, ge=0)
    id_constancia1: int | None = Field(default=None, ge=0)

class recuperarOtorga(BaseModel):
    id_otorga: int
    id_sello2: int
    id_constancia1: int

class soloOtorga(BaseModel):
    item: recuperarOtorga

class listaOtorga(BaseModel):
    items: list[recuperarOtorga]