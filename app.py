import json
from pathlib import Path
from fastapi import FastAPI
import os

API_TITLE = os.getenv("API_TITLE", "API de Notas")

app = FastAPI(title=API_TITLE)

# Carpeta/archivo donde se guardan las notas.
# La carpeta "data" es la que vas a mapear como volumen en Docker.
DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "notas.json"


def cargar_notas() -> list[str]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def guardar_notas(notas: list[str]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(notas, ensure_ascii=False), encoding="utf-8")


@app.get("/")
def raiz():
    raise Exception("error simulado en produccion")

@app.post("/add/{note}")
def agregar_nota(note: str):
    notas = cargar_notas()
    notas.append(note)
    guardar_notas(notas)
    return {"mensaje": "Nota agregada", "nota": note, "total": len(notas)}


@app.get("/list")
def listar_notas():
    notas = cargar_notas()
    return {"notas": notas, "total": len(notas)}