from pydantic import BaseModel, Field
from typing import Literal


class VagaCreate(BaseModel):
    nome: str
    tipo_carregador: Literal["normal", "rapido"]
    potencia_kw: float = Field(gt=0)
    localizacao: str
    coberta: bool
    disponivel: bool = True


class Vaga(VagaCreate):
    id: int