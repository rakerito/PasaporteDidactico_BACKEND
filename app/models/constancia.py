from pydantic import BaseModel, Field

class crearConstancia(BaseModel):
    nombre: str = Field(max_length=100)
    descripcion: str = Field(max_length=300)
    estatus: str = Field(max_length=15)
    imagen: str = Field(max_length=200)

class actualizarConstancia(BaseModel):
    nombre: str | None = Field(default=None, max_length=100)
    descripcion: str | None = Field(default=None, max_length=300)
    estatus: str | None = Field(default=None, max_length=15)
    imagen: str | None = Field(default=None, max_length=200)

class recuperarConstancia(BaseModel):
    id_constancia: int
    nombre: str
    descripcion: str
    estatus: str
    imagen: str

class soloConstancia(BaseModel):
    item: recuperarConstancia

class listaConstancia(BaseModel):
    items: list[recuperarConstancia]