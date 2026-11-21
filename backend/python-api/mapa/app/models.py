
from pydantic import BaseModel
from typing import Literal


class LocalizacaoCreate(BaseModel):
    nome: str
    setor: str
    andar: int
    vaga_id: int
    coordenada_x: float
    coordenada_y: float
    tipo: Literal["coberta", "descoberta"]


class Localizacao(LocalizacaoCreate):
    id: int
