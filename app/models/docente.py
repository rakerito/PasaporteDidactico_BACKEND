from pydantic import BaseModel, Field

class crearDocente(BaseModel):
    id_usuario1:int=Field(ge=0)
    division:str=Field(min_length=10, max_length=150)

class actualizarDocente(BaseModel):
    division:str | None= Field(max_length=150)

class recuperarDocente(BaseModel):
    id_docente:int
    division:str
    id_usuario1:int

class soloDocente(BaseModel):
    item:recuperarDocente

class listaDocente(BaseModel):
    items:list[recuperarDocente]