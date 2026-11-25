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
| **Isabele Aragão** | [@InkoLHP](https://github.com/InkoLHP) | Microserviços Java com Spring Boot (`pagamento`, `usuario-carro` contemplando `usuario` e `carro_usuario`); configuração de bancos MySQL isolados; integração entre serviços Java, serviços Python e frontend; scripts de automação de inicialização. |

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
```

### 🌐 Mapa de Serviços e Portas

| Serviço | Tecnologia | Porta Local | Descrição |
| :--- | :--- | :--- | :--- |
| **Frontend** | HTML, CSS, JS (`npx serve`) | `5500` | Interface web principal que conecta todos os microserviços |
| **usuario-carro** | Java (Spring Boot) | `8080` | Cadastro e consulta de usuários e veículos elétricos |
| **pagamento** | Java (Spring Boot) | `8081` | Processamento e histórico de pagamentos das reservas |
| **vaga** | Python (FastAPI) | `8001` | Gerenciamento de vagas e tipos de carregadores |
| **reserva** | Python (FastAPI) | `8002` | Criação e controle de reservas de vagas |
| **mapa** | Python (FastAPI) | `8003` | Localização física das vagas no estacionamento |

---

### 📂 Estrutura do Repositório

```text
projeto-microservicos-vaga-carro-eletrico/
├── backend/
│   ├── java-api/
│   │   ├── pagamento/          # Microserviço Spring Boot (Porta 8081)
│   │   └── usuario-carro/      # Microserviço Spring Boot (Porta 8080)
│   └── python-api/
│       ├── mapa/               # Microserviço FastAPI (Porta 8003)
│       ├── reserva/            # Microserviço FastAPI (Porta 8002)
│       └── vaga/               # Microserviço FastAPI (Porta 8001)
├── frontend/                   # Interface web (HTML, CSS e JS - Porta 5500)
├── iniciar-tudo.bat            # Inicializa todos os serviços (Java, Python e Frontend)
└── parar-tudo.bat              # Encerra todos os serviços ativos nas portas do projeto
```

---

## 🛠️ Pré-requisitos para Execução Local

Antes de iniciar os serviços, certifique-se de ter instalado em sua máquina:

* **Git** (para clonar o repositório e gerenciar o controle de versão)
* **Java JDK 17+** e **Maven** (ou utilizar o Maven Wrapper `./mvnw` / `mvnw.cmd` já incluso nos projetos)
* **Python 3.10+** e **pip** (com as dependências de cada `requirements.txt` instaladas)
* **Node.js** (necessário para o comando `npx serve` que hospeda o frontend na porta `5500`)
* **MySQL Server** ativo localmente (para os bancos de dados isolados dos microserviços Java)

---

## 🚀 Tutorial: Como Inicializar o Projeto

### 1. Clonar o Repositório
Abra o terminal (PowerShell, Git Bash ou terminal integrado do VS Code) e execute:

```bash
git clone https://github.com/yais505/projeto-microservicos-vaga-carro-eletrico.git
cd projeto-microservicos-vaga-carro-eletrico
```

---

### 2. Configurar os Bancos de Dados e Dependências (Primeira Execução)
1. **MySQL (Serviços Java):**
   * Certifique-se de que o seu servidor **MySQL** está em execução.
   * Verifique as credenciais (`spring.datasource.username` e `spring.datasource.password`) e os nomes dos bancos nos arquivos:
     * `backend/java-api/usuario-carro/src/main/resources/application.properties`
     * `backend/java-api/pagamento/src/main/resources/application.properties`
2. **Dependências Python:**
   * Instale os pacotes necessários em cada serviço Python antes da primeira execução:
   ```bash
   pip install -r backend/python-api/vaga/requirements.txt
   pip install -r backend/python-api/reserva/requirements.txt
   pip install -r backend/python-api/mapa/requirements.txt
   ```

---

### 3. Inicialização Rápida (Recomendado — Windows)

Para subir toda a arquitetura de uma só vez:

1. Dê um duplo clique no arquivo **`iniciar-tudo.bat`** na raiz do projeto (ou execute `.\iniciar-tudo.bat` pelo terminal).
2. O script abrirá terminais individuais para cada microserviço (**Java** nas portas `8080` e `8081`, **Python** nas portas `8001`, `8002` e `8003` e **Frontend** na porta `5500`).
3. Aguarde os 12 segundos configurados no script; o navegador abrirá automaticamente em **`http://localhost:5500`**.

> 🛑 **Para encerrar todos os serviços:** Execute o arquivo **`parar-tudo.bat`** na raiz do projeto para finalizar automaticamente os processos de todas as portas utilizadas.

---

### 4. Inicialização Manual (Alternativa / Linux / macOS)

Caso prefira iniciar cada serviço manualmente em terminais separados:

* **Terminal 1 — Java (`usuario-carro` | Porta 8080):**
```bash
cd backend/java-api/usuario-carro
./mvnw spring-boot:run
```

* **Terminal 2 — Java (`pagamento` | Porta 8081):**
```bash
cd backend/java-api/pagamento
./mvnw spring-boot:run
```

* **Terminal 3 — Python (`vaga` | Porta 8001):**
```bash
cd backend/python-api/vaga
uvicorn app.main:app --reload --port 8001
```

* **Terminal 4 — Python (`reserva` | Porta 8002):**
```bash
cd backend/python-api/reserva
uvicorn app.main:app --reload --port 8002
```

* **Terminal 5 — Python (`mapa` | Porta 8003):**
```bash
cd backend/python-api/mapa
uvicorn app.main:app --reload --port 8003
```

* **Terminal 6 — Frontend (Porta 5500):**
```bash
cd frontend
npx serve -l 5500
```
Depois, acesse **`http://localhost:5500`** no seu navegador.
