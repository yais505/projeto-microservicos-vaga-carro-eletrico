from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import Localizacao, LocalizacaoCreate

DB_PATH = Path(__file__).resolve().parent.parent / "mapa.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS localizacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                setor TEXT NOT NULL,
                andar INTEGER NOT NULL,
                vaga_id INTEGER NOT NULL,
                coordenada_x REAL NOT NULL,
                coordenada_y REAL NOT NULL,
                tipo TEXT NOT NULL
            )
            """
        )
        conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Microserviço de Mapas",
    description="API para gerenciamento da localização das vagas",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def row_to_localizacao(row: sqlite3.Row) -> Localizacao:
    return Localizacao(
        id=row["id"],
        nome=row["nome"],
        setor=row["setor"],
        andar=row["andar"],
        vaga_id=row["vaga_id"],
        coordenada_x=row["coordenada_x"],
        coordenada_y=row["coordenada_y"],
        tipo=row["tipo"],
    )


@app.get("/")
def home():
    return {"mensagem": "Microserviço de mapas funcionando!"}


@app.get("/mapas", response_model=list[Localizacao])
def listar_localizacoes():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM localizacoes ORDER BY id").fetchall()
    return [row_to_localizacao(r) for r in rows]


@app.post("/mapas", response_model=Localizacao, status_code=201)
def criar_localizacao(dados: LocalizacaoCreate):
    payload = dados.model_dump()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO localizacoes (nome, setor, andar, vaga_id, coordenada_x, coordenada_y, tipo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["nome"],
                payload["setor"],
                payload["andar"],
                payload["vaga_id"],
                payload["coordenada_x"],
                payload["coordenada_y"],
                payload["tipo"],
            ),
        )
        conn.commit()
        nova_id = cur.lastrowid
        row = conn.execute("SELECT * FROM localizacoes WHERE id = ?", (nova_id,)).fetchone()
    return row_to_localizacao(row)


@app.get("/mapas/{localizacao_id}", response_model=Localizacao)
def buscar_localizacao(localizacao_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM localizacoes WHERE id = ?", (localizacao_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Localização não encontrada")
    return row_to_localizacao(row)


@app.put("/mapas/{localizacao_id}", response_model=Localizacao)
def atualizar_localizacao(
    localizacao_id: int,
    dados: LocalizacaoCreate,
):
    payload = dados.model_dump()
    with get_conn() as conn:
        cur = conn.execute(
            """
            UPDATE localizacoes
            SET nome = ?, setor = ?, andar = ?, vaga_id = ?, coordenada_x = ?, coordenada_y = ?, tipo = ?
            WHERE id = ?
            """,
            (
                payload["nome"],
                payload["setor"],
                payload["andar"],
                payload["vaga_id"],
                payload["coordenada_x"],
                payload["coordenada_y"],
                payload["tipo"],
                localizacao_id,
            ),
        )
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Localização não encontrada")
        row = conn.execute("SELECT * FROM localizacoes WHERE id = ?", (localizacao_id,)).fetchone()
    return row_to_localizacao(row)


@app.delete("/mapas/{localizacao_id}")
def excluir_localizacao(localizacao_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM localizacoes WHERE id = ?", (localizacao_id,))
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Localização não encontrada")
    return {"mensagem": "Localização excluída com sucesso"}