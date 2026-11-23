@echo off
echo Encerrando portas 8080, 8081 e 5500...
for %%P in (8080 8081 5500) do (
  for /f "tokens=5" %%I in ('netstat -ano ^| findstr /R /C:":%%P .*LISTENING"') do (
    taskkill /PID %%I /T /F >nul 2>&1
  )
)
echo Servicos encerrados.
pause
