
from fastapi import FastAPI, HTTPException
from app.models import Localizacao, LocalizacaoCreate

app = FastAPI(
    title="Microserviço de Mapas",
    description="API para gerenciamento da localização das vagas",
    version="1.0.0"
)

localizacoes: list[Localizacao] = []
proximo_id = 1


@app.get("/")
def home():
    return {"mensagem": "Microserviço de mapas funcionando!"}


@app.get("/mapas", response_model=list[Localizacao])
def listar_localizacoes():
    return localizacoes


@app.post("/mapas", response_model=Localizacao, status_code=201)
def criar_localizacao(dados: LocalizacaoCreate):
    global proximo_id

    nova_localizacao = Localizacao(
        id=proximo_id,
        **dados.model_dump()
    )

    localizacoes.append(nova_localizacao)
    proximo_id += 1

    return nova_localizacao


@app.get("/mapas/{localizacao_id}", response_model=Localizacao)
def buscar_localizacao(localizacao_id: int):
    for localizacao in localizacoes:
        if localizacao.id == localizacao_id:
            return localizacao

    raise HTTPException(
        status_code=404,
        detail="Localização não encontrada"
    )


@app.put("/mapas/{localizacao_id}", response_model=Localizacao)
def atualizar_localizacao(
    localizacao_id: int,
    dados: LocalizacaoCreate
):
    for indice, localizacao in enumerate(localizacoes):
        if localizacao.id == localizacao_id:
            localizacao_atualizada = Localizacao(
                id=localizacao_id,
                **dados.model_dump()
            )

            localizacoes[indice] = localizacao_atualizada
            return localizacao_atualizada

    raise HTTPException(
        status_code=404,
        detail="Localização não encontrada"
    )


@app.delete("/mapas/{localizacao_id}")
def excluir_localizacao(localizacao_id: int):
    for indice, localizacao in enumerate(localizacoes):
        if localizacao.id == localizacao_id:
            localizacoes.pop(indice)

            return {"mensagem": "Localização excluída com sucesso"}

    raise HTTPException(
        status_code=404,
        detail="Localização não encontrada"
    )
