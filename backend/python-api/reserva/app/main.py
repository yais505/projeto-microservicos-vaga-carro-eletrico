
from fastapi import FastAPI, HTTPException
from app.models import Reserva, ReservaCreate

app = FastAPI(
    title="Microserviço de Reservas",
    description="API para gerenciamento de reservas de vagas elétricas",
    version="1.0.0"
)

reservas: list[Reserva] = []
proximo_id = 1


@app.get("/")
def home():
    return {"mensagem": "Microserviço de reservas funcionando!"}


@app.get("/reservas", response_model=list[Reserva])
def listar_reservas():
    return reservas


@app.post("/reservas", response_model=Reserva, status_code=201)
def criar_reserva(dados: ReservaCreate):
    global proximo_id

    if dados.horario_fim <= dados.horario_inicio:
        raise HTTPException(
            status_code=400,
            detail="O horário final deve ser posterior ao inicial"
        )

    nova_reserva = Reserva(
        id=proximo_id,
        **dados.model_dump()
    )

    reservas.append(nova_reserva)
    proximo_id += 1

    return nova_reserva


@app.get("/reservas/{reserva_id}", response_model=Reserva)
def buscar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva.id == reserva_id:
            return reserva

    raise HTTPException(
        status_code=404,
        detail="Reserva não encontrada"
    )


@app.put("/reservas/{reserva_id}", response_model=Reserva)
def atualizar_reserva(reserva_id: int, dados: ReservaCreate):
    if dados.horario_fim <= dados.horario_inicio:
        raise HTTPException(
            status_code=400,
            detail="O horário final deve ser posterior ao inicial"
        )

    for indice, reserva in enumerate(reservas):
        if reserva.id == reserva_id:
            reserva_atualizada = Reserva(
                id=reserva_id,
                **dados.model_dump(),
                status=reserva.status
            )

            reservas[indice] = reserva_atualizada
            return reserva_atualizada

    raise HTTPException(
        status_code=404,
        detail="Reserva não encontrada"
    )


@app.delete("/reservas/{reserva_id}")
def cancelar_reserva(reserva_id: int):
    for indice, reserva in enumerate(reservas):
        if reserva.id == reserva_id:
            reservas[indice] = reserva.model_copy(
                update={"status": "cancelada"}
            )

            return {"mensagem": "Reserva cancelada com sucesso"}

    raise HTTPException(
        status_code=404,
        detail="Reserva não encontrada"
    )
