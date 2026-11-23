@echo off
echo Iniciando microsservicos Java (EV Parking) e Frontend...

start "usuario-carro 8080" cmd /k "cd /d "%~dp0backend\java-api\usuario-carro" && mvnw.cmd spring-boot:run"
start "pagamento 8081"     cmd /k "cd /d "%~dp0backend\java-api\pagamento" && mvnw.cmd spring-boot:run"
start "frontend 5500"      cmd /k "cd /d "%~dp0frontend" && python -m http.server 5500"

echo Aguardando os servicos iniciarem (12 segundos)...
timeout /t 12 /nobreak >nul
start "" "http://localhost:5500"
