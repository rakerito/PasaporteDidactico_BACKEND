from pydantic import BaseModel, Field

class crearRequiere(BaseModel):
    id_curso2: int= Field(ge=0)
    id_sello1: int= Field(ge=0)


class actualizarRequiere(BaseModel):
    id_curso2: int | None= Field(ge=0)
    id_sello1: int | None= Field(ge=0)