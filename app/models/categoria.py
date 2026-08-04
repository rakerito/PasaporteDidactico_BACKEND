from pydantic import BaseModel, Field

class crearCategoria(BaseModel):
    nombre: str = Field(max_length=50)

class actualizarCategoria(BaseModel):
    nombre: str | None = Field(default=None, max_length=50)

class recuperarCategoria(BaseModel):
    id_categoria: int
    nombre: str

class soloCategoria(BaseModel):
    item: recuperarCategoria

class listaCategoria(BaseModel):
    items: list[recuperarCategoria]