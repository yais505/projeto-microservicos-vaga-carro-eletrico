from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import Reserva, ReservaCreate

DB_PATH = Path(__file__).resolve().parent.parent / "reserva.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vaga_id INTEGER NOT NULL,
                nome_cliente TEXT NOT NULL,
                data TEXT NOT NULL,
                horario_inicio TEXT NOT NULL,
                horario_fim TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'confirmada'
            )
            """
        )
        conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Microserviço de Reservas",
    description="API para gerenciamento de reservas de vagas elétricas",
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


def row_to_reserva(row: sqlite3.Row) -> Reserva:
    return Reserva(
        id=row["id"],
        vaga_id=row["vaga_id"],
        nome_cliente=row["nome_cliente"],
        data=row["data"],
        horario_inicio=row["horario_inicio"],
        horario_fim=row["horario_fim"],
        status=row["status"],
    )


def validar_horarios(horario_inicio, horario_fim):
    if horario_fim <= horario_inicio:
        raise HTTPException(
            status_code=400,
            detail="O horário final deve ser posterior ao inicial",
        )


@app.get("/")
def home():
    return {"mensagem": "Microserviço de reservas funcionando!"}


@app.get("/reservas", response_model=list[Reserva])
def listar_reservas():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM reservas ORDER BY id").fetchall()
    return [row_to_reserva(r) for r in rows]


@app.post("/reservas", response_model=Reserva, status_code=201)
def criar_reserva(dados: ReservaCreate):
    validar_horarios(dados.horario_inicio, dados.horario_fim)
    payload = dados.model_dump()
    status_inicial = payload.get("status") or "confirmada"

    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO reservas (vaga_id, nome_cliente, data, horario_inicio, horario_fim, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload["vaga_id"],
                payload["nome_cliente"],
                str(payload["data"]),
                str(payload["horario_inicio"]),
                str(payload["horario_fim"]),
                status_inicial,
            ),
        )
        conn.commit()
        nova_id = cur.lastrowid
        row = conn.execute("SELECT * FROM reservas WHERE id = ?", (nova_id,)).fetchone()
    return row_to_reserva(row)


@app.get("/reservas/{reserva_id}", response_model=Reserva)
def buscar_reserva(reserva_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return row_to_reserva(row)


@app.put("/reservas/{reserva_id}", response_model=Reserva)
def atualizar_reserva(reserva_id: int, dados: ReservaCreate):
    validar_horarios(dados.horario_inicio, dados.horario_fim)
    payload = dados.model_dump()

    with get_conn() as conn:
        existente = conn.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
        if not existente:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")

        conn.execute(
            """
            UPDATE reservas
            SET vaga_id = ?, nome_cliente = ?, data = ?, horario_inicio = ?, horario_fim = ?
            WHERE id = ?
            """,
            (
                payload["vaga_id"],
                payload["nome_cliente"],
                str(payload["data"]),
                str(payload["horario_inicio"]),
                str(payload["horario_fim"]),
                reserva_id,
            ),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
    return row_to_reserva(row)


@app.delete("/reservas/{reserva_id}")
def cancelar_reserva(reserva_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE reservas SET status = 'cancelada' WHERE id = ?",
            (reserva_id,),
        )
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return {"mensagem": "Reserva cancelada com sucesso"}