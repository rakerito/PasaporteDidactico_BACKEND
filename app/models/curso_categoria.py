from pydantic import BaseModel, Field

class crearCursoCategoria(BaseModel):
    id_curso: int = Field(ge=0)
    id_categoria: int = Field(ge=0)

class recuperarCursoCategoria(BaseModel):
    id_curso_categoria: int
    id_curso: int
    id_categoria: int

class listaCursoCategoria(BaseModel):
    items: list[recuperarCursoCategoria]