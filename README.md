# ⚡ Sistema de Gerenciamento de Estacionamento para Veículos Elétricos

> **Trabalho 4 — Construção de Algoritmos**  
> **Curso:** Ciência da Computação — Universidade de Fortaleza (UNIFOR)  
> **Professor:** Ronaldo Gonçalves

Projeto acadêmico estruturado em arquitetura de microserviços para administrar um estacionamento voltado a veículos elétricos, separando responsabilidades por domínio de negócio: cadastro e disponibilidade de vagas com carregadores, reservas, localização física no estacionamento, relacionamento entre usuários e veículos e gerenciamento de pagamentos.

---

## 👥 Integrantes e Contribuições

| Integrante | GitHub | Responsabilidades no Projeto |
| :--- | :--- | :--- |
| **Yasmin Miranda** | [@yais505](https://github.com/yais505) | Estrutura inicial do repositório monorepo; microserviços Python (`vaga`, `reserva`, `mapa`) com FastAPI; modelos de dados e rotas REST; interface web básica em HTML, CSS e JavaScript e integração com as APIs Python. |
| **Isabele Aragão** | [@InkoLHP](https://github.com/InkoLHP) | Microserviços Java com Spring Boot (`pagamento`, `usuario`, `carro_usuario`); configuração de bancos MySQL isolados; integração entre serviços Java, serviços Python e frontend. |

---

## 🏗️ Arquitetura e Diagrama dos Microserviços

O sistema é organizado em um **monorepo** dividido entre `frontend` e `backend`, com serviços independentes comunicando-se via requisições HTTP e dados em formato JSON.

```text
                    +------------------+
                    |     usuario      |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |    front-end     |
                    |   (JavaScript)   |
                    +--------+---------+
                             |
     +-------+-------+-------+-------+-------+
     |       |       |       |       |       |
     v       v       v       v       v       v
+--------+ +--------+ +--------+ +----------+ +---------+ +--------------+
|reserva | |  vaga  | |  mapa  | |pagamento | | usuario | | carro_usuario|
| (yas)  | | (yas)  | | (yas)  | |  (isa)   | |  (isa)  | |    (isa)     |
| python | | python | | python | |   java   | |  java   | |     java     |
+--------+ +--------+ +--------+ +----------+ +---------+ +--------------+
