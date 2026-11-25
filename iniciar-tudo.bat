@echo off
echo Iniciando todos os microsservicos (Java + Python) e o Frontend...

REM Microsservicos Java (Isa)
start "usuario-carro 8080" cmd /k "cd /d "%~dp0backend\java-api\usuario-carro" && mvnw.cmd spring-boot:run"
start "pagamento 8081"     cmd /k "cd /d "%~dp0backend\java-api\pagamento" && mvnw.cmd spring-boot:run"

REM Microsservicos Python (Yas)
start "vaga 8001"    cmd /k "cd /d "%~dp0backend\python-api\vaga" && python -m uvicorn app.main:app --reload --port 8001"
start "reserva 8002" cmd /k "cd /d "%~dp0backend\python-api\reserva" && python -m uvicorn app.main:app --reload --port 8002"
start "mapa 8003"    cmd /k "cd /d "%~dp0backend\python-api\mapa" && python -m uvicorn app.main:app --reload --port 8003"

REM Frontend (porta 5500)
start "frontend 5500" cmd /k "cd /d "%~dp0frontend" && npx serve -l 5500"

echo Aguardando os servicos subirem (12 segundos)...
timeout /t 12 /nobreak >nul
start "" "http://localhost:5500"