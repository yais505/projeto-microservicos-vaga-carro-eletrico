@REM Licensed to the Apache Software Foundation (ASF) under one
@echo off
setlocal
set MAVEN_PROJECTBASEDIR=%~dp0
set WRAPPER_PROPERTIES=%MAVEN_PROJECTBASEDIR%.mvn\wrapper\maven-wrapper.properties
for /f "tokens=1,2 delims==" %%A in ('type "%WRAPPER_PROPERTIES%"') do (
  if "%%A"=="distributionUrl" set DISTRIBUTION_URL=%%B
)
set MAVEN_USER_HOME=%USERPROFILE%\.m2
set WRAPPER_DISTS=%MAVEN_USER_HOME%\wrapper\dists\apache-maven-3.9.9
set MVN_EXE=%WRAPPER_DISTS%\apache-maven-3.9.9\bin\mvn.cmd
if not exist "%MVN_EXE%" (
  echo Baixando Apache Maven 3.9.9...
  if not exist "%WRAPPER_DISTS%" mkdir "%WRAPPER_DISTS%"
  powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%DISTRIBUTION_URL%' -OutFile '%WRAPPER_DISTS%\maven.zip'; Expand-Archive -Path '%WRAPPER_DISTS%\maven.zip' -DestinationPath '%WRAPPER_DISTS%' -Force; Remove-Item '%WRAPPER_DISTS%\maven.zip'"
)
call "%MVN_EXE%" %*
endlocal
