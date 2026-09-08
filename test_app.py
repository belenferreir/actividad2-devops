import pytest
from fastapi.testclient import TestClient

import app


@pytest.fixture(autouse=True)
def datos_temporales(tmp_path, monkeypatch):
    """Aísla cada test en su propia carpeta temporal para no tocar data/notas.json real."""
    monkeypatch.setattr(app, "DATA_DIR", tmp_path)
    monkeypatch.setattr(app, "DATA_FILE", tmp_path / "notas.json")


@pytest.fixture
def client():
    # raise_server_exceptions=False para poder testear el 500 de "/" en vez de que explote el test
    return TestClient(app.app, raise_server_exceptions=False)


# --- Funciones de persistencia ---

def test_cargar_notas_sin_archivo_devuelve_lista_vacia():
    assert app.cargar_notas() == []


def test_guardar_y_cargar_notas():
    app.guardar_notas(["comprar pan", "estudiar devops"])
    assert app.cargar_notas() == ["comprar pan", "estudiar devops"]


def test_guardar_notas_crea_el_archivo():
    app.guardar_notas(["hola"])
    assert app.DATA_FILE.exists()


def test_guardar_notas_conserva_caracteres_especiales():
    app.guardar_notas(["áéí ñ üö"])
    contenido = app.DATA_FILE.read_text(encoding="utf-8")
    assert "áéí ñ üö" in contenido  # verifica ensure_ascii=False


# --- Endpoints ---

def test_listar_vacio(client):
    r = client.get("/list")
    assert r.status_code == 200
    assert r.json() == {"notas": [], "total": 0}


def test_agregar_nota(client):
    r = client.post("/add/hola")
    assert r.status_code == 200
    assert r.json() == {"mensaje": "Nota agregada", "nota": "hola", "total": 1}


def test_agregar_y_listar(client):
    client.post("/add/uno")
    client.post("/add/dos")
    r = client.get("/list")
    assert r.json() == {"notas": ["uno", "dos"], "total": 2}


def test_raiz_devuelve_500(client):
    r = client.get("/")
    assert r.status_code == 500