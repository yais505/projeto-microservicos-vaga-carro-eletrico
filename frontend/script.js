const API_USUARIO_CARRO = "http://localhost:8080";
const API_PAGAMENTO     = "http://localhost:8081";
const API_VAGAS         = "http://127.0.0.1:8001";
const API_RESERVAS      = "http://127.0.0.1:8002";
const API_MAPA          = "http://127.0.0.1:8003";

function mostrarAviso(msg, erro = false) {
    const el = document.getElementById("aviso");
    el.textContent = msg;
    el.className = erro ? "erro" : "ok";
    el.hidden = false;
    clearTimeout(mostrarAviso.timer);
    mostrarAviso.timer = setTimeout(() => el.hidden = true, 4500);
}

async function requisicao(url, metodo = "GET", dados = null) {
    const config = {
        method: metodo,
        headers: { "Content-Type": "application/json" }
    };
    if (dados !== null) {
        config.body = JSON.stringify(dados);
    }
    try {
        const resp = await fetch(url, config);
        if (resp.status === 204) return null;
        const json = await resp.json();
        if (!resp.ok) {
            throw new Error(json.erro || json.detail || "Erro na requisição");
        }
        return json;
    } catch (err) {
        const msg = err.message === "Failed to fetch"
            ? "Serviço offline em " + url
            : err.message;
        mostrarAviso(msg, true);
        throw err;
    }
}

document.getElementById("abas").addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    const aba = btn.dataset.aba;
    document.querySelectorAll("nav button").forEach(b => b.classList.toggle("on", b.dataset.aba === aba));
    document.querySelectorAll("main section").forEach(s => s.hidden = s.id !== aba);

    if (aba === "usuarios") { listarUsuarios(); listarCarros(); }
    if (aba === "vagas") listarVagas();
    if (aba === "reservas") listarReservas();
    if (aba === "mapa") listarMapa();
    if (aba === "pagamentos") listarPagamentos();
});

async function listarUsuarios() {
    const usuarios = await requisicao(`${API_USUARIO_CARRO}/usuarios`);
    const tbody = document.getElementById("tabela-usuarios");
    tbody.innerHTML = usuarios.map(u => `
        <tr>
            <td>${u.id}</td>
            <td>${u.nome}</td>
            <td>${u.cpf}</td>
            <td>${u.email}</td>
            <td>${u.telefone || "-"}</td>
            <td><button onclick="excluirUsuario(${u.id})">Excluir</button></td>
        </tr>
    `).join("") || `<tr><td colspan="6">Nenhum usuário cadastrado.</td></tr>`;
}

async function excluirUsuario(id) {
    await requisicao(`${API_USUARIO_CARRO}/usuarios/${id}`, "DELETE");
    mostrarAviso("Usuário excluído.");
    listarUsuarios();
}

document.getElementById("form-usuario").addEventListener("submit", async (e) => {
    e.preventDefault();
    await requisicao(`${API_USUARIO_CARRO}/usuarios`, "POST", {
        nome: document.getElementById("usuario-nome").value,
        cpf: document.getElementById("usuario-cpf").value,
        email: document.getElementById("usuario-email").value,
        telefone: document.getElementById("usuario-telefone").value
    });
    e.target.reset();
    mostrarAviso("Usuário cadastrado com sucesso!");
    listarUsuarios();
});

async function listarCarros() {
    const carros = await requisicao(`${API_USUARIO_CARRO}/carros`);
    const tbody = document.getElementById("tabela-carros");
    tbody.innerHTML = carros.map(c => `
        <tr>
            <td>${c.id}</td>
            <td><strong>${c.placa}</strong></td>
            <td>${c.marca || ""} ${c.modelo}</td>
            <td>${c.tipoConector || "-"}</td>
            <td>${c.capacidadeBateriaKwh ? c.capacidadeBateriaKwh + " kWh" : "-"}</td>
            <td>${c.usuario ? c.usuario.nome + " (ID " + c.usuario.id + ")" : "-"}</td>
            <td><button onclick="excluirCarro(${c.id})">Excluir</button></td>
        </tr>
    `).join("") || `<tr><td colspan="7">Nenhum carro cadastrado.</td></tr>`;
}

async function excluirCarro(id) {
    await requisicao(`${API_USUARIO_CARRO}/carros/${id}`, "DELETE");
    mostrarAviso("Carro removido.");
    listarCarros();
}

document.getElementById("form-carro").addEventListener("submit", async (e) => {
    e.preventDefault();
    const usuarioId = document.getElementById("carro-usuario-id").value;
    await requisicao(`${API_USUARIO_CARRO}/usuarios/${usuarioId}/carros`, "POST", {
        placa: document.getElementById("carro-placa").value,
        marca: document.getElementById("carro-marca").value,
        modelo: document.getElementById("carro-modelo").value,
        tipoConector: document.getElementById("carro-conector").value,
        capacidadeBateriaKwh: Number(document.getElementById("carro-bateria").value) || null
    });
    e.target.reset();
    mostrarAviso("Carro vinculado ao usuário!");
    listarCarros();
});

async function listarPagamentos() {
    const pags = await requisicao(`${API_PAGAMENTO}/pagamentos`);
    const tbody = document.getElementById("tabela-pagamentos");
    tbody.innerHTML = pags.map(p => `
        <tr>
            <td>${p.id}</td>
            <td>${p.nomeUsuario} (ID ${p.usuarioId})</td>
            <td>#${p.reservaId}</td>
            <td>R$ ${Number(p.valor).toFixed(2)}</td>
            <td>${p.metodoPagamento}</td>
            <td><strong>${p.status}</strong></td>
            <td>${p.dataPagamento ? new Date(p.dataPagamento).toLocaleString("pt-BR") : "-"}</td>
            <td><button ${p.status === "ESTORNADO" ? "disabled" : ""} onclick="estornarPagamento(${p.id})">Estornar</button></td>
        </tr>
    `).join("") || `<tr><td colspan="8">Nenhum pagamento registrado.</td></tr>`;
}

async function estornarPagamento(id) {
    await requisicao(`${API_PAGAMENTO}/pagamentos/${id}/estornar`, "PATCH");
    mostrarAviso("Pagamento estornado.");
    listarPagamentos();
}

document.getElementById("form-pagamento").addEventListener("submit", async (e) => {
    e.preventDefault();
    await requisicao(`${API_PAGAMENTO}/pagamentos`, "POST", {
        usuarioId: Number(document.getElementById("pag-usuario-id").value),
        reservaId: Number(document.getElementById("pag-reserva-id").value),
        valor: Number(document.getElementById("pag-valor").value),
        metodoPagamento: document.getElementById("pag-metodo").value
    });
    e.target.reset();
    mostrarAviso("Pagamento aprovado e registrado!");
    listarPagamentos();
});

async function listarVagas() {
    const vagas = await requisicao(`${API_VAGAS}/vagas`);
    const lista = document.getElementById("lista-vagas");
    lista.replaceChildren();
    vagas.forEach(v => {
        const li = document.createElement("li");
        li.textContent = `ID ${v.id} | ${v.nome} | ${v.tipo_carregador} | ${v.potencia_kw} kW | ${v.localizacao} `;
        const btn = document.createElement("button");
        btn.textContent = "Excluir";
        btn.onclick = async () => { await requisicao(`${API_VAGAS}/vagas/${v.id}`, "DELETE"); listarVagas(); };
        li.appendChild(btn);
        lista.appendChild(li);
    });
}

document.getElementById("form-vaga").addEventListener("submit", async (e) => {
    e.preventDefault();
    await requisicao(`${API_VAGAS}/vagas`, "POST", {
        nome: document.getElementById("vaga-nome").value,
        tipo_carregador: document.getElementById("vaga-tipo").value,
        potencia_kw: Number(document.getElementById("vaga-potencia").value),
        localizacao: document.getElementById("vaga-localizacao").value,
        coberta: document.getElementById("vaga-coberta").checked
    });
    e.target.reset();
    mostrarAviso("Vaga cadastrada!");
    listarVagas();
});

async function listarReservas() {
    const reservas = await requisicao(`${API_RESERVAS}/reservas`);
    const lista = document.getElementById("lista-reservas");
    lista.replaceChildren();
    reservas.forEach(r => {
        const li = document.createElement("li");
        li.textContent = `ID ${r.id} | ${r.nome_cliente} | Vaga ${r.vaga_id} | ${r.data} (${r.horario_inicio} - ${r.horario_fim}) | ${r.status} `;
        const btn = document.createElement("button");
        btn.textContent = "Cancelar";
        btn.disabled = r.status === "cancelada";
        btn.onclick = async () => { await requisicao(`${API_RESERVAS}/reservas/${r.id}`, "DELETE"); listarReservas(); };
        li.appendChild(btn);
        lista.appendChild(li);
    });
}

document.getElementById("form-reserva").addEventListener("submit", async (e) => {
    e.preventDefault();
    await requisicao(`${API_RESERVAS}/reservas`, "POST", {
        vaga_id: Number(document.getElementById("reserva-vaga").value),
        nome_cliente: document.getElementById("reserva-cliente").value,
        data: document.getElementById("reserva-data").value,
        horario_inicio: document.getElementById("reserva-inicio").value,
        horario_fim: document.getElementById("reserva-fim").value
    });
    e.target.reset();
    mostrarAviso("Reserva criada!");
    listarReservas();
});

async function listarMapa() {
    const locs = await requisicao(`${API_MAPA}/mapas`);
    const lista = document.getElementById("lista-mapa");
    lista.replaceChildren();
    locs.forEach(l => {
        const li = document.createElement("li");
        li.textContent = `ID ${l.id} | ${l.nome} | Setor ${l.setor}, Andar ${l.andar} | Vaga ${l.vaga_id} (${l.coordenada_x}, ${l.coordenada_y}) `;
        const btn = document.createElement("button");
        btn.textContent = "Excluir";
        btn.onclick = async () => { await requisicao(`${API_MAPA}/mapas/${l.id}`, "DELETE"); listarMapa(); };
        li.appendChild(btn);
        lista.appendChild(li);
    });
}

document.getElementById("form-mapa").addEventListener("submit", async (e) => {
    e.preventDefault();
    await requisicao(`${API_MAPA}/mapas`, "POST", {
        nome: document.getElementById("mapa-nome").value,
        setor: document.getElementById("mapa-setor").value,
        andar: Number(document.getElementById("mapa-andar").value),
        vaga_id: Number(document.getElementById("mapa-vaga").value),
        coordenada_x: Number(document.getElementById("mapa-x").value),
        coordenada_y: Number(document.getElementById("mapa-y").value),
        tipo: document.getElementById("mapa-tipo").value
    });
    e.target.reset();
    mostrarAviso("Localização cadastrada!");
    listarMapa();
});

listarUsuarios().catch(() => {});
listarCarros().catch(() => {});
