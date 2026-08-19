from pydantic import BaseModel, Field

class crearUsuario(BaseModel):
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=100)
    correo: str = Field(min_length=10, pattern=r"^[\w\.-]+@utsjr\.edu\.mx$")
    contraseña: str = Field(min_length=6)
    categoria: str = Field(max_length=20)
    no_empleado: str = Field(min_length=1, max_length=6, pattern=r"^\d+$")

class actualizarUsuario(BaseModel):
    nombre: str | None = Field(default=None, max_length=100)
    apellidos: str | None = Field(default=None, max_length=100)
    correo: str | None = Field(default=None, min_length=10, pattern=r"^[\w\.-]+@utsjr\.edu\.mx$")
    categoria: str | None = Field(default=None, max_length=20)
    no_empleado: str | None = Field(default=None, min_length=1, max_length=6, pattern=r"^\d+$")

class recuperarUsuario(BaseModel):
    id_usuario: int
    nombre: str
    apellidos: str
    correo: str
    categoria: str
    no_empleado: str | None = None
    numero_usuario: str | None = None

class soloUsuario(BaseModel):
    item: recuperarUsuario

class listaUsuario(BaseModel):
    items: list[recuperarUsuario]

class iniciarUsuario(BaseModel):
    correo: str
    contraseña: str