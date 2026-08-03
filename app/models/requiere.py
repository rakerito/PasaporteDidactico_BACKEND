from pydantic import BaseModel, Field

class crearRequiere(BaseModel):
    id_curso2: int= Field(ge=0)
    id_sello1: int= Field(ge=0)


class actualizarRequiere(BaseModel):
    id_curso2: int | None= Field(ge=0)
    id_sello1: int | None= Field(ge=0)

class recuperarRequiere(BaseModel):
    id_curso2:int
    id_sello1:int
    

class soloRequiere(BaseModel):
    item:recuperarRequiere

class listaRequiere(BaseModel):
    items:list[recuperarRequiere]