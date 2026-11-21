
from pydantic import BaseModel
from datetime import date, time
from typing import Literal


class ReservaCreate(BaseModel):
    vaga_id: int
    nome_cliente: str
    data: date
    horario_inicio: time
    horario_fim: time


class Reserva(ReservaCreate):
    id: int
    status: Literal["confirmada", "cancelada"] = "confirmada"
