from fastapi import APIRouter
from app.routes import health, auth, usuario, curso, docente, sello, toma, otorga, requiere, constancia, categoria, curso_categoria

router = APIRouter()

# Registrar rutas de sub-módulos
router.include_router(health.router, tags=["Health"])
router.include_router(auth.router, tags=["Autenticación"])
router.include_router(usuario.router, tags=["Usuarios"])
router.include_router(curso.router, tags=["Cursos"])
router.include_router(docente.router, tags=["Docentes"])
router.include_router(sello.router, tags=["Sellos"])
router.include_router(toma.router, tags=["Tomas"])
router.include_router(otorga.router, tags=["Otorga"])
router.include_router(requiere.router, tags=["Requiere"])
router.include_router(constancia.router, tags=["Constancias"])
router.include_router(categoria.router, tags=["Categorias"])
router.include_router(curso_categoria.router, tags=["Curso-Categoria"])

@router.get("/", tags=["Root"])
def bienvenida():
    return {
        "message": "Bienvenido a la API de Pasaporte Didáctico",
        "docs": "/docs"
    }