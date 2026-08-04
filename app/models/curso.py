from pydantic import BaseModel, Field

class crearCurso(BaseModel):
    nombre: str = Field(max_length=100)
    descripcion: str = Field(max_length=300)
    duracion: int = Field(max_digits=4)
    estatus: str = Field(max_length=10)
    id_sello1: int = Field(max_length=8)

class actualizarCurso(BaseModel):
    nombre: str | None = Field(default=None, max_length=100)
    descripcion: str | None = Field(default=None, max_length=300)
    duracion: int | None = Field(default=None, max_digits=4)
    estatus: str | None = Field(default=None, max_length=10)
    id_sello1: int | None = Field(default=None, max_length=8)

class recuperarCurso(BaseModel):
    id_curso: int
    nombre: str
    descripcion: str
    duracion: int
    estatus: str
    id_sello1: int

class soloCurso(BaseModel):
    item: recuperarCurso

class listaCurso(BaseModel):
    items: list[recuperarCurso]