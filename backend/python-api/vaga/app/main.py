from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import Vaga, VagaCreate

DB_PATH = Path(__file__).resolve().parent.parent / "vaga.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vagas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo_carregador TEXT NOT NULL,
                potencia_kw REAL NOT NULL,
                localizacao TEXT NOT NULL,
                coberta INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Microserviço de Vagas",
    description="API para gerenciamento de vagas de carregamento elétrico",
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


def row_to_vaga(row: sqlite3.Row) -> Vaga:
    return Vaga(
        id=row["id"],
        nome=row["nome"],
        tipo_carregador=row["tipo_carregador"],
        potencia_kw=row["potencia_kw"],
        localizacao=row["localizacao"],
        coberta=bool(row["coberta"]),
    )


@app.get("/")
def home():
    return {"mensagem": "Microserviço de vagas funcionando!"}


@app.get("/vagas", response_model=list[Vaga])
def listar_vagas():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM vagas ORDER BY id").fetchall()
    return [row_to_vaga(r) for r in rows]


@app.post("/vagas", response_model=Vaga, status_code=201)
def criar_vaga(dados: VagaCreate):
    payload = dados.model_dump()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO vagas (nome, tipo_carregador, potencia_kw, localizacao, coberta)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload["nome"],
                payload["tipo_carregador"],
                payload["potencia_kw"],
                payload["localizacao"],
                1 if payload.get("coberta") else 0,
            ),
        )
        conn.commit()
        nova_id = cur.lastrowid
        row = conn.execute("SELECT * FROM vagas WHERE id = ?", (nova_id,)).fetchone()
    return row_to_vaga(row)


@app.get("/vagas/{vaga_id}", response_model=Vaga)
def buscar_vaga(vaga_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM vagas WHERE id = ?", (vaga_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return row_to_vaga(row)


@app.put("/vagas/{vaga_id}", response_model=Vaga)
def atualizar_vaga(vaga_id: int, dados: VagaCreate):
    payload = dados.model_dump()
    with get_conn() as conn:
        cur = conn.execute(
            """
            UPDATE vagas
            SET nome = ?, tipo_carregador = ?, potencia_kw = ?, localizacao = ?, coberta = ?
            WHERE id = ?
            """,
            (
                payload["nome"],
                payload["tipo_carregador"],
                payload["potencia_kw"],
                payload["localizacao"],
                1 if payload.get("coberta") else 0,
                vaga_id,
            ),
        )
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vaga não encontrada")
        row = conn.execute("SELECT * FROM vagas WHERE id = ?", (vaga_id,)).fetchone()
    return row_to_vaga(row)


@app.delete("/vagas/{vaga_id}")
def excluir_vaga(vaga_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM vagas WHERE id = ?", (vaga_id,))
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return {"mensagem": "Vaga excluída com sucesso"}