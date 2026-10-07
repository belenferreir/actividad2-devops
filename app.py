import json
import time
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import Response
import os
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

API_TITLE = os.getenv("API_TITLE", "API de Notas")

app = FastAPI(title=API_TITLE)

# Carpeta donde se guardan las notas.
# La carpeta "data" es la que vas a mapear como volumen en Docker.
DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "notas.json"

notas_creadas = Counter("notas_creadas", "Cantidad total de notas creadas")
notas_totales = Gauge("notas_totales", "Cantidad actual de notas guardadas")
llamadas_por_endpoint = Histogram(
    "llamadas_por_endpoint_segundos",
    "Duración de las llamadas por endpoint",
    ["endpoint"],
)

def cargar_notas() -> list[str]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []

def guardar_notas(notas: list[str]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(notas, ensure_ascii=False), encoding="utf-8")

@app.middleware("http")
async def medir_llamadas(request: Request, call_next):
    inicio = time.perf_counter()
    try:
        return await call_next(request)
    finally:
        llamadas_por_endpoint.labels(endpoint=request.url.path).observe(
            time.perf_counter() - inicio
        )

@app.on_event("startup")
def init_medidor():
    notas_totales.set(len(cargar_notas()))

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

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)