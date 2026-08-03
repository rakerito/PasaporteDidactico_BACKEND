from pydantic import BaseModel, Field

class crearSello(BaseModel):
    nombre: str= Field(max_length=100)
    descripcion: str= Field(max_length=300)
    estatus: str= Field(max_length=15)
    imagen: str= Field(max_length=200)

class actualizarSello(BaseModel):
    nombre: str | None= Field(max_length=100)
    descripcion: str | None= Field(max_length=300)
    estatus: str | None= Field(max_length=15)
    imagen: str | None= Field(max_length=200)

class recuperarSello(BaseModel):
    id_sello:int
    nombre:str
    descripcion:str
    estatus:str
    imagen:str

class soloSello(BaseModel):
    item:recuperarSello

class listaSello(BaseModel):
    items:list[recuperarSello]