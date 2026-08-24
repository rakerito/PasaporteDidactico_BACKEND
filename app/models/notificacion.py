from typing import Literal
from pydantic import BaseModel, Field

TipoNotificacion = Literal["sello", "curso", "constancia", "mantenimiento", "general"]

class crearNotificacionPersonal(BaseModel):
    id_usuario1: int = Field(ge=0)
    tipo: TipoNotificacion
    titulo: str = Field(max_length=150)
    mensaje: str = Field(max_length=300)

class crearNotificacionGeneral(BaseModel):
    tipo: TipoNotificacion
    titulo: str = Field(max_length=150)
    mensaje: str = Field(max_length=300)

class recuperarNotificacion(BaseModel):
    id_notificacion: int
    origen: str  # "personal" o "general"
    tipo: str
    titulo: str
    mensaje: str
    leida: bool
    creada_en: str

class listaNotificacion(BaseModel):
    items: list[recuperarNotificacion]

class resumenNotificaciones(BaseModel):
    sello: int
    curso: int
    constancia: int
    mantenimiento: int
    general: int
    total: int