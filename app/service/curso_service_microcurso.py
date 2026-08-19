def listar_microcursos(id_curso_padre: int):
    """
    Regresa los microcursos que pertenecen a un curso normal dado.
    """
    try:
        res = (
            _table()
            .select("*")
            .eq("id_curso_padre", id_curso_padre)
            .execute()
        )
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar microcursos: {e}")


def validar_microcurso(datos: dict):
    """
    Verifica las reglas de negocio antes de crear/actualizar un microcurso:
    - El curso padre debe existir y ser de tipo 'normal'.
    - Un curso padre no puede tener más de 4 microcursos.
    Se usa solo cuando datos["tipo"] == "microcurso" y trae id_curso_padre.
    """
    id_padre = datos.get("id_curso_padre")

    if not id_padre:
        raise HTTPException(
            status_code=400,
            detail="Un microcurso debe indicar a qué curso (id_curso_padre) pertenece."
        )

    padre = obtener_por_id(id_padre)
    if not padre:
        raise HTTPException(status_code=400, detail="El curso padre indicado no existe.")

    if padre.get("tipo") != "normal":
        raise HTTPException(
            status_code=400,
            detail="Un microcurso solo puede pertenecer a un curso de tipo 'normal', no a otro microcurso."
        )

    hijos_actuales = listar_microcursos(id_padre)
    if len(hijos_actuales) >= 4:
        raise HTTPException(
            status_code=400,
            detail="Este curso ya tiene el máximo de 4 microcursos permitidos."
        )