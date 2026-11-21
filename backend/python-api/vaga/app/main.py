
from fastapi import FastAPI, HTTPException
from app.models import Vaga, VagaCreate

app = FastAPI(
    title="Microserviço de Vagas",
    description="API para gerenciamento de vagas de carregamento elétrico",
    version="1.0.0"
)

vagas: list[Vaga] = []
proximo_id = 1


@app.get("/")
def home():
    return {"mensagem": "Microserviço de vagas funcionando!"}


@app.get("/vagas", response_model=list[Vaga])
def listar_vagas():
    return vagas


@app.post("/vagas", response_model=Vaga, status_code=201)
def criar_vaga(dados: VagaCreate):
    global proximo_id

    nova_vaga = Vaga(
        id=proximo_id,
        **dados.model_dump()
    )

    vagas.append(nova_vaga)
    proximo_id += 1

    return nova_vaga


@app.get("/vagas/{vaga_id}", response_model=Vaga)
def buscar_vaga(vaga_id: int):
    for vaga in vagas:
        if vaga.id == vaga_id:
            return vaga

    raise HTTPException(status_code=404, detail="Vaga não encontrada")


@app.put("/vagas/{vaga_id}", response_model=Vaga)
def atualizar_vaga(vaga_id: int, dados: VagaCreate):
    for indice, vaga in enumerate(vagas):
        if vaga.id == vaga_id:
            vaga_atualizada = Vaga(
                id=vaga_id,
                **dados.model_dump()
            )

            vagas[indice] = vaga_atualizada
            return vaga_atualizada

    raise HTTPException(status_code=404, detail="Vaga não encontrada")


@app.delete("/vagas/{vaga_id}")
def excluir_vaga(vaga_id: int):
    for indice, vaga in enumerate(vagas):
        if vaga.id == vaga_id:
            vagas.pop(indice)
            return {"mensagem": "Vaga excluída com sucesso"}

    raise HTTPException(status_code=404, detail="Vaga não encontrada")
