from pydantic import BaseModel, Field

regexCorreo = r"^[a-zA-Z0-9._%-]+@utsjr\.edu\.mx$" 

class crearUsuario(BaseModel):
    nombre: str = Field(min_length=3, max_length=50)
    apellidos: str = Field(max_length=100)
    correo: str = Field(min_length=10, pattern=regexCorreo)
    contraseña: str = Field()
    categoria: str = Field(max_length=15)

class actualizarUsuario(BaseModel):
    nombre: str | None = Field(default=None, min_length=3, max_length=50)
    apellidos: str | None = Field(default=None, max_length=100)
    correo: str | None = Field(default=None, min_length=10, pattern=regexCorreo)
    categoria: str | None = Field(default=None, max_length=15)

class cambiarContraseña(BaseModel):
    contraseña: str | None = Field(default=None)
    nueva_contraseña: str | None = Field(default=None)

class recuperarUsuario(BaseModel):
    id_usuario: int
    nombre: str
    apellidos: str
    correo: str
    categoria: str
    contraseña: str

class iniciarUsuario(BaseModel):
    correo: str
    contraseña: str

class listaUsuario(BaseModel):
    items: list[recuperarUsuario]

class soloUsuario(BaseModel):
    item: recuperarUsuario