
const API_VAGAS = "http://127.0.0.1:8001";
const API_RESERVAS = "http://127.0.0.1:8002";
const API_MAPA = "http://127.0.0.1:8003";

// Função genérica para realizar requisições
async function requisicao(url, metodo = "GET", dados = null) {
    const configuracao = {
        method: metodo,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (dados !== null) {
        configuracao.body = JSON.stringify(dados);
    }

    const resposta = await fetch(url, configuracao);

    const resultado = await resposta.json();

    if (!resposta.ok) {
        throw new Error(resultado.detail || "Erro na requisição");
    }

    return resultado;
}

// ==================== VAGAS ====================

async function listarVagas() {
    try {
        const vagas = await requisicao(`${API_VAGAS}/vagas`);
        const lista = document.getElementById("lista-vagas");

        lista.replaceChildren();

        vagas.forEach(vaga => {
            const item = document.createElement("li");

            item.textContent =
                `${vaga.nome} | ${vaga.tipo_carregador} | ` +
                `${vaga.potencia_kw} kW | ${vaga.localizacao} | ` +
                `Disponível: ${vaga.disponivel ? "Sim" : "Não"}`;

            const botao = document.createElement("button");
            botao.textContent = "Excluir";

            botao.addEventListener("click", async () => {
                try {
                    await requisicao(
                        `${API_VAGAS}/vagas/${vaga.id}`,
                        "DELETE"
                    );
                    listarVagas();
                } catch (erro) {
                    alert(erro.message);
                }
            });

            item.appendChild(botao);
            lista.appendChild(item);
        });
    } catch (erro) {
        alert("Erro ao carregar vagas: " + erro.message);
    }
}

document.getElementById("form-vaga").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        nome: document.getElementById("vaga-nome").value,
        tipo_carregador: document.getElementById("vaga-tipo").value,
        potencia_kw: Number(document.getElementById("vaga-potencia").value),
        localizacao: document.getElementById("vaga-localizacao").value,
        coberta: document.getElementById("vaga-coberta").checked
    };

    try {
        await requisicao(`${API_VAGAS}/vagas`, "POST", dados);

        evento.target.reset();
        listarVagas();

    } catch (erro) {
        alert("Erro ao cadastrar vaga: " + erro.message);
    }
});


// ==================== RESERVAS ====================

async function listarReservas() {
    try {
        const reservas = await requisicao(`${API_RESERVAS}/reservas`);
        const lista = document.getElementById("lista-reservas");

        lista.replaceChildren();

        reservas.forEach(reserva => {
            const item = document.createElement("li");

            item.textContent =
                `${reserva.nome_cliente} | Vaga ${reserva.vaga_id} | ` +
                `${reserva.data} | ${reserva.horario_inicio} - ` +
                `${reserva.horario_fim} | ${reserva.status}`;

            const botao = document.createElement("button");
            botao.textContent = "Cancelar";

            botao.disabled = reserva.status === "cancelada";

            botao.addEventListener("click", async () => {
                try {
                    await requisicao(
                        `${API_RESERVAS}/reservas/${reserva.id}`,
                        "DELETE"
                    );
                    listarReservas();
                } catch (erro) {
                    alert(erro.message);
                }
            });

            item.appendChild(botao);
            lista.appendChild(item);
        });
    } catch (erro) {
        alert("Erro ao carregar reservas: " + erro.message);
    }
}

document.getElementById("form-reserva").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        vaga_id: Number(document.getElementById("reserva-vaga").value),
        nome_cliente: document.getElementById("reserva-cliente").value,
        data: document.getElementById("reserva-data").value,
        horario_inicio: document.getElementById("reserva-inicio").value,
        horario_fim: document.getElementById("reserva-fim").value
    };

    try {
        await requisicao(`${API_RESERVAS}/reservas`, "POST", dados);

        evento.target.reset();
        listarReservas();

    } catch (erro) {
        alert("Erro ao criar reserva: " + erro.message);
    }
});


// ==================== MAPA ====================

async function listarMapa() {
    try {
        const localizacoes = await requisicao(`${API_MAPA}/mapas`);
        const lista = document.getElementById("lista-mapa");

        lista.replaceChildren();

        localizacoes.forEach(localizacao => {
            const item = document.createElement("li");

            item.textContent =
                `${localizacao.nome} | Setor ${localizacao.setor} | ` +
                `Andar ${localizacao.andar} | Vaga ${localizacao.vaga_id} | ` +
                `X: ${localizacao.coordenada_x}, ` +
                `Y: ${localizacao.coordenada_y} | ${localizacao.tipo}`;

            const botao = document.createElement("button");
            botao.textContent = "Excluir";

            botao.addEventListener("click", async () => {
                try {
                    await requisicao(
                        `${API_MAPA}/mapas/${localizacao.id}`,
                        "DELETE"
                    );
                    listarMapa();
                } catch (erro) {
                    alert(erro.message);
                }
            });

            item.appendChild(botao);
            lista.appendChild(item);
        });
    } catch (erro) {
        alert("Erro ao carregar mapa: " + erro.message);
    }
}

document.getElementById("form-mapa").addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        nome: document.getElementById("mapa-nome").value,
        setor: document.getElementById("mapa-setor").value,
        andar: Number(document.getElementById("mapa-andar").value),
        vaga_id: Number(document.getElementById("mapa-vaga").value),
        coordenada_x: Number(document.getElementById("mapa-x").value),
        coordenada_y: Number(document.getElementById("mapa-y").value),
        tipo: document.getElementById("mapa-tipo").value
    };

    try {
        await requisicao(`${API_MAPA}/mapas`, "POST", dados);

        evento.target.reset();
        listarMapa();

    } catch (erro) {
        alert("Erro ao cadastrar localização: " + erro.message);
    }
});


// Carregar os dados ao abrir a página
listarVagas();
listarReservas();
listarMapa();
