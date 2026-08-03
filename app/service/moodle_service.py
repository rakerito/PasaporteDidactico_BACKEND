import pandas as pd
import requests
from app.core.supabase_client import get_supabase
from app.core.config import config

MOODLE_URL = "http://localhost"
USERNAME = "TuUsuarioMoodle"
PASSWORD = "TuContraseñaMoodle"
REPORT_ID = "3"


def _tabla(nombre_tabla: str):
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(nombre_tabla)


def descargar_reporte() -> pd.DataFrame:
    session = requests.Session()
    login_url = f"{MOODLE_URL}/login/index.php"
    session.get(login_url)
    session.post(login_url, data={"username": USERNAME, "password": PASSWORD})

    download_url = f"{MOODLE_URL}/reportbuilder/download.php?id={REPORT_ID}&format=excel"
    resp = session.get(download_url)

    if resp.status_code != 200 or len(resp.content) < 1000:
        raise Exception("No se pudo descargar el reporte de Moodle.")

    # Leemos directo desde memoria, sin guardar Excel temporal en disco
    from io import BytesIO
    return pd.read_excel(BytesIO(resp.content))


def _buscar_id_docente(correo: str) -> int | None:
    res = _tabla(config.supabase_usuario).select("id_usuario").eq("correo", correo).execute()
    return res.data[0]["id_usuario"] if res.data else None


def _buscar_id_curso(idnumber_o_nombre: str) -> int | None:
    res = _tabla("curso").select("id_curso").eq("nombre", idnumber_o_nombre).execute()
    return res.data[0]["id_curso"] if res.data else None


def sincronizar_progreso():
    df = descargar_reporte()

    if "Student progress" in df.columns:
        df["progreso_num"] = (
            df["Student progress"].astype(str).str.replace("%", "").str.strip()
        )
        df["progreso_num"] = pd.to_numeric(df["progreso_num"], errors="coerce").fillna(0)
    else:
        df["progreso_num"] = 0

    resultados = []

    for _, fila in df.iterrows():
        id_docente = _buscar_id_docente(fila.get("Email address", ""))
        id_curso = _buscar_id_curso(fila.get("Course full name", ""))

        if id_docente is None or id_curso is None:
            # Aquí decides: ¿lo omites, o lo reportas como "sin match"?
            continue

        datos_toma = {
            "progreso": f"{fila['progreso_num']}%",
            "estatus": "en curso" if fila["progreso_num"] < 100 else "completado",
            "fecha_lim": None,  # define tu regla de negocio aquí
            "id_curso1": id_curso,
            "id_docente1": id_docente,
        }

        # UPSERT manual: buscamos si ya existe una toma para ese curso+docente
        existente = (
            _tabla("toma")
            .select("id_toma")
            .eq("id_curso1", id_curso)
            .eq("id_docente1", id_docente)
            .execute()
        )

        if existente.data:
            res = (
                _tabla("toma")
                .update(datos_toma)
                .eq("id_toma", existente.data[0]["id_toma"])
                .execute()
            )
        else:
            res = _tabla("toma").insert(datos_toma).execute()

        resultados.append(res.data)

    return resultados